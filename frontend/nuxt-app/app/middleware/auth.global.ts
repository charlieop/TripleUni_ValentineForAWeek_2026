export default defineNuxtRouteMiddleware(async (to) => {
  const { getToken } = useStore();
  const token = getToken();
  if (to.path === "/login" || to.path === "/login/") {
    if (token) {
      await lazyFetchUserState();
      return navigateTo("/");
    }
    return;
  }

  if (!token) {
    return navigateTo("/login");
  }
  await lazyFetchUserState();
});
