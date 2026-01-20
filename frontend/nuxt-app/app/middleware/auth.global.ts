export default defineNuxtRouteMiddleware((to) => {
  const { getToken } = useStore();
  const token = getToken();
  if (to.path === "/login" || to.path === "/login/") {
    if (token) {
      return navigateTo("/");
    }
    return;
  }

  if (!token) {
    return navigateTo("/login");
  }
});
