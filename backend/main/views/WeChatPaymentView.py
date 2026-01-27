from wechatpayv3 import WeChatPay, WeChatPayType
from datetime import datetime, timedelta
from uuid import uuid4

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from ..mixin import UtilMixin
from ..models import PaymentRecord
from ..logger import CustomLogger
from ..configs import AvtivityDates

from django.conf import settings
import json

with open(settings.BASE_DIR / "SECRETS.json") as f:
    secrets = json.load(f)
    APPID = secrets["WECHAT_APP_ID"]
    CERT_SERIAL_NO = secrets["WECHAT_CERT_SERIAL_NO"]
    APIV3_KEY = secrets["WECHAT_APIV3_KEY"]
    MCHID = secrets["WECHAT_MCHID"]
with open(settings.BASE_DIR / "apiclient_key.pem") as f:
    PRIVATE_KEY = f.read()

# XXX: change this to 99 * 100
PRICE = 1
# PRICE = 99 * 100

EXPIRES_IN = 7 * 60
DESCRIPTION = "Triple Uni 一周CP 2026 活动押金"
NOTIFY_URL = "https://api.charlieop.com/v1/payment/wechat/"
CERT_DIR = str(settings.BASE_DIR / "cert")
PARTNER_MODE = False
TIMEOUT = (7, 20)

logger = CustomLogger("wechatpay")
wxpay = WeChatPay(
    wechatpay_type=WeChatPayType.NATIVE,
    mchid=MCHID,
    private_key=PRIVATE_KEY,
    cert_serial_no=CERT_SERIAL_NO,
    apiv3_key=APIV3_KEY,
    appid=APPID,
    notify_url=NOTIFY_URL,
    cert_dir=CERT_DIR,
    partner_mode=PARTNER_MODE,
    timeout=TIMEOUT,
    logger=logger,
)

# XXX: change this to use the actual out_trade_no
def generate_out_trade_no(openid):
    return "TEST-0001-" + str(uuid4())[:10]
    return "CP26-" + openid[6:] + "-" + str(uuid4())[:4]


class WeChatPaymentView(APIView, UtilMixin):

    def get(self, request):
        AvtivityDates.assert_valid_application_period()
        
        token = self.get_token(request)
        applicant = self.get_applicant_by_token(token)

        if applicant.payment is not None:
            logger.warning(f"GET payment: {applicant.wechat_info.openid}, already paid")
            raise ValidationError({"detail": "you have already paid"})

        wechat_info = applicant.wechat_info
        openid = wechat_info.openid
        out_trade_no = generate_out_trade_no(openid)
        expire_time = datetime.now() + timedelta(seconds=EXPIRES_IN)
        expire_time_str = expire_time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
        attach = f"{openid}-{datetime.now().strftime("%m-%d %H:%M:%S")}"

        logger.info(f"GET payment: {openid}, out_trade_no: {out_trade_no}")
        code, message = wxpay.pay(
            description=DESCRIPTION,
            out_trade_no=out_trade_no,
            amount={"total": PRICE},
            pay_type=WeChatPayType.JSAPI,
            payer={"openid": openid},
            time_expire=expire_time_str,
            attach=attach,
        )
        result = json.loads(message)
        if code == 200:
            prepay_id = result.get("prepay_id")
            timestamp = str(int(datetime.now().timestamp()))
            noncestr = str(uuid4()).replace("-", "")
            package = "prepay_id=" + prepay_id
            sign = wxpay.sign([APPID, timestamp, noncestr, package])
            data = {
                "appId": APPID,
                "timeStamp": timestamp,
                "nonceStr": noncestr,
                "package": f"prepay_id={prepay_id}",
                "signType": "RSA",
                "paySign": sign,
            }
            logger.info(f"Payment initiated for: {openid}, prepay_id: {prepay_id}")
            return Response({"data": data}, status=status.HTTP_200_OK)
        else:
            logger.error(f"Payment failed for {openid}: code {code}, {result}")
            return Response(
                {"detail": f"failed to initialize payment: {result}, code: {code}"},
                status=status.HTTP_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        logger.info("POST payment callback from WeChat")
        result = wxpay.callback(headers=request.META, body=request.body)
        if not (result and result.get("event_type") == "TRANSACTION.SUCCESS"):
            logger.error("Payment callback failed: invalid event type")
            raise AuthenticationFailed({"detail": "payment failed"})

        resource = result.get("resource")
        out_trade_no = resource.get("out_trade_no")
        transaction_id = resource.get("transaction_id")
        payer = resource.get("payer")
        openid = payer.get("openid")

        logger.info(
            f"Payment callback for: {openid}, out_trade_no: {out_trade_no}, transaction_id: {transaction_id}"
        )
                
        existing_payment = PaymentRecord.objects.filter(out_trade_no=out_trade_no).first()
        if existing_payment is not None:
            logger.warning(f"Payment callback for: {openid}, out_trade_no: {out_trade_no}, already exists, skipping")
            return Response({"detail": "payment already exists"}, status=status.HTTP_200_OK)

        try:
            payment = PaymentRecord.objects.create(
                out_trade_no=out_trade_no, transaction_id=transaction_id, handle_by="system"
            )
            payment.save()
        except Exception as e:
            logger.error(f"Error creating payment: {e}")
            return Response({"detail": "error creating payment"}, status=status.HTTP_INTERNAL_SERVER_ERROR)

        try:
            applicant = self.get_applicant_by_openid(openid)
            if applicant is None:
                logger.error(
                    f"Payment callback: cannot find applicant for openid: {openid}"
                )
                return Response(
                    {"detail": "cannot find corresponding applicant"},
                    status=status.HTTP_200_OK,
                )
            applicant.payment = payment
            applicant.save()
        except Exception as e:
            logger.error(f"Error updating applicant: {e}")
            return Response({"detail": "error updating applicant"}, status=status.HTTP_INTERNAL_SERVER_ERROR)

        logger.info(f"Payment successful for: {openid}")
        return Response({"detail": "payment successful"}, status=status.HTTP_200_OK)
