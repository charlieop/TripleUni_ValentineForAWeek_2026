export const isWechat = computed(() => {
  var ua = window.navigator.userAgent.toLowerCase();
  if (ua.match(/MicroMessenger/i) !== null) {
    return true;
  } else {
    return false;
  }
});

export const isDarkMode = ref(false);
isDarkMode.value =
  window.matchMedia &&
  window.matchMedia("(prefers-color-scheme: dark)").matches;
window
  .matchMedia("(prefers-color-scheme: dark)")
  .addEventListener("change", (e) => {
    isDarkMode.value = e.matches;
  });


export interface VueformInstance {
  data: Record<string, any>;
  load(data: Record<string, any>): void;
  submitting: boolean;
}

export const getImageUrl = (path: string | null) => {
  if (!path) return '';
  if (path.startsWith('/')) {
    return `${API_HOST}${path}`;
  }
  return `${API_HOST}/media/${path}`;
};