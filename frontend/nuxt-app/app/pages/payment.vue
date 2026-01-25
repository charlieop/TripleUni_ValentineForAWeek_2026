<template>
    <div class="page-wrapper paper-background">
        <LogoSm />
        <h1 class="page-title">押金支付</h1>

        <div v-if="loading" class="loading">
            <p>正在处理支付...</p>
        </div>

        <template v-else-if="error">

            <div class="error">
                <div class="error-icon">❌</div>
                <p class="error-title">支付失败</p>
                <p class="error-message">错误信息: {{ error }}</p>
            </div>
            <div class="button-group">
                <button @click="retryPayment" class="btn primary">重试</button>
                <button @click="navigateTo('/')" class="btn">返回首页</button>
            </div>
        </template>

        <template v-else-if="paymentSuccess">
            <div class="success">
                <div class="success-icon">✓</div>
                <p class="success-message">支付成功！</p>
                <p class="success-subtext">押金已支付完成，报名成功</p>
            </div>
            <div class="button-group">
                <button @click="navigateTo('/')" class="btn primary">返回首页</button>
            </div>
        </template>
        <div v-else class="payment-content">
            <!-- Payment Info Section -->
            <section class="info-section">
                <div class="payment-info-card">
                    <h2>押金信息</h2>
                    <div class="info-item">
                        <span class="label">押金金额:</span>
                        <span class="value amount">¥99.00</span>
                    </div>
                    <div class="info-item">
                        <span class="label">支付方式:</span>
                        <span class="value">微信支付</span>
                    </div>
                </div>
            </section>

            <!-- Instructions Section -->
            <section class="info-section instructions-section">
                <h2>支付说明</h2>
                <ul class="instructions-list">
                    <li>点击"支付押金"按钮后将跳转至微信支付</li>
                    <li>请在5分钟内完成支付</li>
                    <li>如需使用其他支付方式, 请联系主办方</li>
                </ul>
            </section>

            <!-- Action Buttons -->
            <div class="button-group">
                <button @click="initiatePayment" class="btn primary" :disabled="processing">
                    {{ processing ? '处理中...' : '支付押金' }}
                </button>
                <button @click="navigateTo('/')" class="btn" :disabled="processing">
                    返回首页
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
useHead({
    title: "一周CP 2026 | 押金支付",
});

const { get } = useRequest();
const loading = ref(false);
const processing = ref(false);
const error = ref<string | null>(null);
const paymentSuccess = ref(false);

interface PaymentData {
    appId: string;
    timeStamp: string;
    nonceStr: string;
    package: string;
    signType: string;
    paySign: string;
}

declare const WeixinJSBridge: {
    invoke: (
        method: string,
        paymentDetails: PaymentData,
        callback: (res: { err_msg: string }) => void
    ) => void;
}

const getPaymentData = async () => {
    try {
        const response = await get("payment/wechat/");
        if (!response.ok) {
            const errorData = await response.json();
            console.error(errorData);
            throw new Error(errorData.detail || "获取支付信息失败");
        }
        const res = await response.json();
        return res.data as PaymentData;
    } catch (err: any) {
        throw new Error(err.message || "网络错误，请检查连接");
    }
}

const requestPayment = async (paymentData: PaymentData) => {
    return new Promise<void>((resolve, reject) => {
        WeixinJSBridge.invoke("getBrandWCPayRequest", paymentData, (res: { err_msg: string, errMsg?: string }) => {
            if (res.err_msg === "get_brand_wcpay_request:ok") {
                console.log("Payment successful");
                paymentSuccess.value = true;
                resolve();
            } else if (res.err_msg === "get_brand_wcpay_request:cancel") {
                reject(new Error("支付已取消"));
            } else {
                console.error("Payment error:", res);
                reject(new Error(`支付失败: ${res.err_msg || res.errMsg || "未知错误"}`));
            }
        });
    });
}

const initiatePayment = async () => {
    error.value = null;
    processing.value = true;
    loading.value = true;

    try {
        // Check if in WeChat environment
        if (typeof WeixinJSBridge === "undefined") {
            // Wait for WeixinJSBridge to be ready
            await new Promise<void>((resolve, reject) => {
                const timeout = setTimeout(() => {
                    reject(new Error("请在微信中打开此页面"));
                }, 5000);

                document.addEventListener("WeixinJSBridgeReady", () => {
                    clearTimeout(timeout);
                    resolve();
                }, { once: true });

                // Check if WeixinJSBridge becomes available immediately
                if (typeof WeixinJSBridge !== "undefined") {
                    clearTimeout(timeout);
                    resolve();
                }
            });
        }

        const paymentData = await getPaymentData();
        console.log("Payment data received:", paymentData);

        await requestPayment(paymentData);

        // If successful, wait a moment then redirect
        setTimeout(() => {
            navigateTo("/");
        }, 2000);
    } catch (err: any) {
        console.error("Payment error:", err);
        error.value = err.message || "支付失败，请重试";
    } finally {
        loading.value = false;
        processing.value = false;
    }
}

const retryPayment = () => {
    error.value = null;
    paymentSuccess.value = false;
    initiatePayment();
}
</script>

<style scoped>
.payment-content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    max-width: 520px;
    margin: 0 auto;
    width: 100%;
}

h1 {
    margin-bottom: 1.5rem;
}

h2 {
    font-size: var(--fs-500);
    font-weight: bold;
    color: var(--clr-primary-dark);
    text-align: left;
    padding-left: 0.25rem;
}

.info-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
}

.value {
    font-weight: bold;
}

.value.amount {
    color: var(--clr-primary-dark);
    font-size: var(--fs-500);
}

.instructions-section,
.payment-info-card {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    background: rgba(255, 255, 255, 0.55);
    border-radius: 1rem;
    padding: 1rem 1.25rem;
    box-shadow:
        0 8px 20px rgba(0, 0, 0, 0.06),
        0 0 0 1px rgba(255, 255, 255, 0.55) inset;
}

.instructions-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-left: 1.25rem;
    font-size: var(--fs-300);
    list-style-type: disc;
}

.loading,
.error,
.success {
    max-width: 520px;
    margin: 1.5rem auto;
    width: 100%;
    padding: 1.25rem 1.5rem;
    border-radius: 1rem;
    text-align: center;
    font-size: var(--fs-400);
    background: rgba(255, 255, 255, 0.75);
    box-shadow:
        0 12px 26px rgba(0, 0, 0, 0.08),
        0 0 0 1px rgba(255, 255, 255, 0.6) inset;
}

.loading p {
    font-weight: 700;
    font-size: var(--fs-500);
}

.error {
    border: 1px solid rgba(255, 128, 128, 0.4);
    color: red;
}

.success {
    border: 1px solid rgba(120, 200, 120, 0.4);
}

.success-icon,
.error-icon {
    width: 3rem;
    height: 3rem;
    border-radius: 999px;
    background: rgba(120, 200, 120, 0.2);
    color: var(--clr-success);
    display: grid;
    place-items: center;
    font-size: 1.5rem;
    font-weight: 900;
    margin: 0 auto 0.75rem;
}

.error-icon {
    color: red;
    background: rgba(255, 128, 128, 0.2);
}

.success-message,
.error-title {
    font-size: var(--fs-600);
    font-weight: 800;
}

.success-subtext,
.error-message {
    margin-top: 0.25rem;
    font-size: var(--fs-400);
}

.button-group {
    width: 100%;
    margin-top: 0.5rem;
}
</style>