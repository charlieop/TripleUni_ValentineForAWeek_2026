<template>
    <div class="page-wrapper">
        <h1>支付押金</h1>

        <div class="info-section">
            <div class="message-card">
                <p class="message-text">此功能尚未实现</p>
                <p class="message-subtext">支付功能正在开发中，敬请期待</p>
            </div>
        </div>

        <div class="button-group">
            <button @click="navigateTo('/')" class="btn secondary">返回首页</button>
        </div>
    </div>
</template>

<script setup lang="ts">
useHead({
    title: "一周CP 2026 | 支付押金",
});
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

.message-card {
    text-align: center;
    padding: 2rem 1rem;
}

.message-text {
    font-size: var(--fs-500);
    color: var(--clr-text);
    margin-bottom: 1rem;
    font-weight: 600;
}

.message-subtext {
    font-size: var(--fs-400);
    color: var(--clr-text--muted);
    line-height: 1.6;
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

.btn.secondary {
    background: var(--clr-secondary);
    color: var(--clr-text);
}

.btn.secondary:hover {
    background: var(--clr-secondary-dark);
}
</style>