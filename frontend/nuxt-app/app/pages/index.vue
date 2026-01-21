<template>
  <div class="page-wrapper">
    <h1>一周CP 2026</h1>
    <div class="button-group">
      <button @click="navigateTo('/apply')" class="btn primary">活动报名</button>
      <button @click="navigateTo('/payment')" class="btn primary">支付押金</button>
      <button @click="navigateTo('/withdraw')" class="btn secondary">撤销申请</button>
      <button @click="navigateTo('/match-result')" class="btn secondary">匹配结果</button>
      <button @click="navigateTo('/match')" class="btn secondary">匹配详情</button>
    </div>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: "一周CP 2026 | 首页",
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

.button-group {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
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

.btn.secondary {
  background: var(--clr-secondary);
  color: var(--clr-text);
}

.btn.secondary:hover {
  background: var(--clr-secondary-dark);
}
</style>