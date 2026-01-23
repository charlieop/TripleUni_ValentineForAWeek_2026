<template>
    <div class="page-wrapper">
        <h1>支付押金</h1>

        <div v-if="loading" class="loading">
            <p>正在处理支付...</p>
        </div>

        <div v-else-if="error" class="error">
            <p>{{ error }}</p>
            <div class="button-group">
                <button @click="retryPayment" class="btn primary">重试</button>
                <button @click="navigateTo('/')" class="btn secondary">返回首页</button>
            </div>
        </div>

        <div v-else-if="paymentSuccess" class="success">
            <div class="success-icon">✓</div>
            <p class="success-message">支付成功！</p>
            <p class="success-subtext">您的押金已成功支付，请继续完成报名</p>
            <div class="button-group">
                <button @click="navigateTo('/')" class="btn primary">返回首页</button>
            </div>
        </div>

        <div v-else class="payment-content">
            <!-- Payment Info Section -->
            <section class="info-section">
                <h2>押金信息</h2>
                <div class="payment-info-card">
                    <div class="info-item">
                        <span class="label">押金金额:</span>
                        <span class="value amount">¥99.00</span>
                    </div>
                    <div class="info-item">
                        <span class="label">支付方式:</span>
                        <span class="value">微信支付</span>
                    </div>
                    <div class="info-description">
                        <p>押金用于确保活动参与承诺。活动结束后，完成所有任务的参与者将获得全额退款。</p>
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
                <button @click="navigateTo('/')" class="btn secondary" :disabled="processing">
                    返回首页
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
useHead({
    title: "一周CP 2026 | 支付押金",
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
.page-wrapper {
    padding: 1.5rem;
    max-width: 100%;
    margin: 0 auto;
}

h1 {
    font-size: var(--fs-700);
    color: var(--clr-primary);
    margin-bottom: 2rem;
    text-align: center;
}

h2 {
    font-size: var(--fs-600);
    color: var(--clr-primary-dark);
    margin-bottom: 1rem;
}

.loading,
.error,
.success {
    text-align: center;
    padding: 2rem;
}

.loading {
    color: var(--clr-text);
}

.error {
    color: var(--clr-danger);
}

.success {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}

.success-icon {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: var(--clr-success);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    font-weight: bold;
    margin-bottom: 1rem;
}

.success-message {
    font-size: var(--fs-600);
    color: var(--clr-success);
    font-weight: 600;
    margin: 0;
}

.success-subtext {
    font-size: var(--fs-400);
    color: var(--clr-text--muted);
    margin: 0;
    line-height: 1.6;
}

.payment-content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.info-section {
    margin-bottom: 1rem;
    padding: 1.5rem;
    background: var(--clr-background--muted);
    border-radius: 0.5rem;
}

.payment-info-card {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.info-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    background: var(--clr-background);
    border-radius: 0.5rem;
}

.info-item .label {
    font-size: var(--fs-400);
    color: var(--clr-text--muted);
}

.info-item .value {
    font-size: var(--fs-400);
    color: var(--clr-text);
    font-weight: 600;
}

.info-item .value.amount {
    font-size: var(--fs-600);
    color: var(--clr-primary);
}

.info-description {
    padding: 1rem;
    background: var(--clr-background);
    border-radius: 0.5rem;
    border-left: 3px solid var(--clr-primary);
}

.info-description p {
    font-size: var(--fs-400);
    color: var(--clr-text--muted);
    line-height: 1.6;
    margin: 0;
}

.instructions-section {
    background: linear-gradient(135deg, var(--clr-primary-light), var(--clr-secondary-light));
}

.instructions-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.instructions-list li {
    padding: 0.75rem;
    background: var(--clr-background);
    border-radius: 0.5rem;
    font-size: var(--fs-400);
    color: var(--clr-text);
    line-height: 1.5;
    position: relative;
    padding-left: 2rem;
}

.instructions-list li::before {
    content: "•";
    position: absolute;
    left: 0.75rem;
    color: var(--clr-primary);
    font-weight: bold;
    font-size: var(--fs-500);
}

.button-group {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 2rem;
}

.btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.5rem;
    font-size: var(--fs-400);
    font-weight: 600;
    cursor: pointer;
    transition: var(--transition);
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn.primary {
    background: var(--clr-primary);
    color: var(--clr-text);
}

.btn.primary:hover:not(:disabled) {
    background: var(--clr-primary-dark);
}

.btn.secondary {
    background: var(--clr-secondary);
    color: var(--clr-text);
}

.btn.secondary:hover:not(:disabled) {
    background: var(--clr-secondary-dark);
}
</style>