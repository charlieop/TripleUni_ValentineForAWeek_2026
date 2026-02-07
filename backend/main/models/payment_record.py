import uuid
from django.db import models


class PaymentRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    out_trade_no = models.CharField(
        max_length=33, verbose_name="商户订单号", null=True, blank=True
    )
    transaction_id = models.CharField(
        max_length=30, verbose_name="微信支付订单号", null=True, blank=True
    )

    handle_by = models.CharField(max_length=10, verbose_name="处理人")

    refunded = models.BooleanField(default=False, verbose_name="已退款")

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"付款人: {self.applicant.name if hasattr(self, 'applicant') else '未知'} - {self.handle_by} - {self.transaction_id}"

    class Meta:
        verbose_name = "付款记录"
        verbose_name_plural = "付款记录"
        db_table = "payment_record"
        ordering = ["created_at"]
