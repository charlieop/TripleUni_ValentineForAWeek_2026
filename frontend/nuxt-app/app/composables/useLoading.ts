// Global loading state
const isLoading = ref(false);
const loadingCount = ref(0);

export const useLoading = () => {
  const startLoading = () => {
    loadingCount.value++;
    isLoading.value = true;
  };

  const stopLoading = () => {
    loadingCount.value = Math.max(0, loadingCount.value - 1);
    if (loadingCount.value === 0) {
      isLoading.value = false;
    }
  };

  return {
    isLoading: readonly(isLoading),
    startLoading,
    stopLoading,
  };
};
