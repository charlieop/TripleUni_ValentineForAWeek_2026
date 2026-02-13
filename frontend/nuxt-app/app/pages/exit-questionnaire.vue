<template>
  <div>
    <div class="exit-questionnaire-wrapper page-wrapper">
      <LogoSm />
      <ExitQuestionareForm />
    </div>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: "一周CP 2026 | 活动结束问卷",
});
</script>

<style scoped>
.exit-questionnaire-wrapper {
  height: var(--height);
  padding: 3rem 2rem;
  overflow: scroll;
  overflow-x: clip;
}

.logo-sm {
  margin-bottom: 1rem;
}
</style>
