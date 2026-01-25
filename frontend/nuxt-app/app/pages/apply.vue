<template>
  <div>
    <div class="application-form-wrapper">
      <ApplicationForm />
    </div>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: "一周CP 2026 | 活动报名",
});
</script>

<style scoped>
.application-form-wrapper {
  height: var(--height);
  padding: 3rem 2rem;
  overflow: scroll;
  overflow-x: clip;
}
</style>
