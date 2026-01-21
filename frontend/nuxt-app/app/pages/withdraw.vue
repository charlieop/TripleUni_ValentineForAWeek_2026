<template>
    <div class="page-wrapper">
        <h1>撤销申请</h1>

        <div class="info-section">
            <div class="warning-card">
                <p class="warning-title">⚠️ 重要提示</p>
                <p class="warning-text">
                    撤销申请后，押金将会退还给您，但您将<strong>无法再次参加</strong>本次活动。
                </p>
                <p class="warning-subtext">
                    请确认您真的想要撤销申请。此操作不可撤销。
                </p>
            </div>
        </div>

        <div class="button-group">
            <button v-if="!clicked" @click="confirmWithdraw" class="btn primary">
                撤销申请
            </button>
            <button v-else @click="confirmWithdraw" class="btn danger">
                再次点击以确认撤销
            </button>
            <button @click="navigateTo('/')" class="btn secondary">返回首页</button>
        </div>
    </div>
</template>

<script setup lang="ts">
useHead({
    title: "一周CP 2026 | 取消申请",
});

const clicked = ref(false);
const { del } = useRequest();

function confirmWithdraw() {
    if (!clicked.value) {
        clicked.value = true;
        return;
    }

    del("applicants/")
        .then((res) => {
            if (res.ok) {
                navigateTo("/");
            } else {
                throw new Error("撤销申请失败");
            }
        })
        .catch((err) => {
            alert(err.message || "撤销申请失败");
            console.error(err);
            clicked.value = false;
        });
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

.info-section {
    margin-bottom: 2rem;
    padding: 1.5rem;
    background: var(--clr-background--muted);
    border-radius: 0.5rem;
}

.warning-card {
    padding: 1.5rem;
    background: var(--clr-failed);
    border-radius: 0.5rem;
    border-left: 4px solid var(--clr-danger);
}

.warning-title {
    font-size: var(--fs-500);
    color: var(--clr-danger);
    font-weight: 600;
    margin-bottom: 1rem;
}

.warning-text {
    font-size: var(--fs-400);
    color: var(--clr-text);
    line-height: 1.6;
    margin-bottom: 0.75rem;
}

.warning-text strong {
    color: var(--clr-danger);
    font-weight: 700;
}

.warning-subtext {
    font-size: var(--fs-300);
    color: var(--clr-text--muted);
    line-height: 1.5;
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

.btn.primary {
    background: var(--clr-primary);
    color: var(--clr-text);
}

.btn.primary:hover {
    background: var(--clr-primary-dark);
}

.btn.danger {
    background: var(--clr-danger);
    color: white;
}

.btn.danger:hover {
    background: hsl(0, 87%, 40%);
}

.btn.secondary {
    background: var(--clr-secondary);
    color: var(--clr-text);
}

.btn.secondary:hover {
    background: var(--clr-secondary-dark);
}
</style>