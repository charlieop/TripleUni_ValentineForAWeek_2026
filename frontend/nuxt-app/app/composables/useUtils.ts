export const API_HOST = "http://10.0.0.77:8000";
export const API_URL = API_HOST + "/v1";

export const APPID = "wx09ec18a3cf830379";

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