<template>
  <div class="app-wrapper">
    <NuxtRouteAnnouncer />
    <div class="app">
      <NuxtPage />
    </div>
    <LoadingOverlay />
    <!-- XXX: 暂时关闭微信授权 -->
    <!-- <RequireWeChat /> -->
  </div>
</template>

<script setup lang="ts">
const displayScreenSizeWarning = ref(false);

onMounted(() => {
  if (window.innerWidth < 375 || window.innerHeight < 650) {
    displayScreenSizeWarning.value = true;
  }
});
</script>

<style scoped>
.app-wrapper {
  background-color: rgb(238, 235, 235);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  height: 100svh;
}

.app {
  background-color: var(--clr-background);
  height: 100%;
  width: 100%;
  max-width: var(--max-width);
}
</style>
