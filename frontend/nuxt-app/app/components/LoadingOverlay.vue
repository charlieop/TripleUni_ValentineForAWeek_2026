<template>
  <Transition name="fade">
    <div v-if="isLoading" class="modal-overlay">
      <div class="loading-content">
        <div class="spinner"></div>
        <p class="loading-text">加载中...</p>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
const { isLoading } = useLoading();
</script>

<style scoped>
.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 80%;
  gap: 1.5rem;
  padding: 2rem;
  background: var(--clr-background);
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid var(--clr-background--muted);
  border-top: 4px solid var(--clr-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  font-size: var(--fs-500);
  color: var(--clr-text);
  margin: 0;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
