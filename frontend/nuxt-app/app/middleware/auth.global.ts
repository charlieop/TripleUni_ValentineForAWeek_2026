export default defineNuxtRouteMiddleware(async (to) => {
  // Leaderboard is public, no login required
  if (to.path === "/leaderboard" || to.path === "/leaderboard/") {
    return;
  }

  const { getToken } = useStore();
  await lazyFetchUserState();

  if (to.path === "/maintaince/" || to.path === "/maintaince") {
    if (userState.value !== UserStates.MAINTENANCE) {
      return navigateTo("/");
    }
    return;
  } else if (userState.value === UserStates.MAINTENANCE) {
    return navigateTo("/maintaince");
  }

  const token = getToken();
  if (to.path === "/login/" || to.path === "/login") {
    if (token) {
      return navigateTo("/");
    }
    return;
  }

  if (!token) {
    return navigateTo("/login");
  }
});
