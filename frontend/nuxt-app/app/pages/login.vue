<template>
  <div class="page-wrapper">
    <div class="content-wrapper" v-if="!hasCode">
      <h1>请使用真实账户授权</h1>
      <div class="info-section">
        <p class="info-text">注意: 请 <strong>不要使用虚拟账户</strong> (momo)</p>
        <p class="info-text">
          我们需要获取你的 <strong>真实</strong> 用户昵称及头像用作匹配目的,
          虚拟账号将被<strong>取消资格</strong>
        </p>
      </div>
      <div class="button-group">
        <a :href="url">
          <button class="btn primary">登录微信授权</button>
        </a>
      </div>
    </div>
    <div class="content-wrapper" v-else>
      <h1>正在获取OpenId...</h1>
      <div class="info-section">
        <p class="info-text">请稍候...</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: "一周CP 2026 | 微信授权",
});
const route = useRoute();
const router = useRouter();
const hasCode = computed(() => queryParams.code != null);
const { setToken } = useStore();
const { post } = useRequest();

const queryParams = route.query;
const requestURL = "https://wechat-oauth.uuunnniii.com";

let url =
  requestURL +
  "?appid=" +
  APPID +
  "&redirect_uri=" +
  encodeURIComponent(window.location.href) +
  "&response_type=code&scope=snsapi_userinfo#wechat_redirect";

onMounted(() => {
  const code = queryParams.code;

  console.log(code);

  if (code) {
    post("oauth/wechat/", {
      code: code,
    })
      .then((res) => res.json())
      .then((data) => {
        const token = data?.data?.token;
        if (token) {
          setToken(token);
          router.push("/");
        } else {
          alert("获取登录凭证失败: " + data?.detail);
        }
      })
      .catch((error) => {
        alert("获取登录凭证失败: " + error.message);
      });
  }

});
</script>

<style scoped>
.page-wrapper {
  padding: 1.5rem;
  max-width: 100%;
  margin: 0 auto;
  min-height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.content-wrapper {
  width: 100%;
  max-width: 500px;
}

h1 {
  font-size: var(--fs-700);
  color: var(--clr-primary);
  margin-bottom: 2rem;
  text-align: center;
}

.info-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--clr-background--muted);
  border-radius: 0.5rem;
}

.info-text {
  font-size: var(--fs-400);
  color: var(--clr-text);
  line-height: 1.6;
  margin-bottom: 1rem;
}

.info-text:last-child {
  margin-bottom: 0;
}

strong {
  color: var(--clr-accent);
  font-weight: 600;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-size: var(--fs-400);
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
  text-decoration: none;
  display: block;
  text-align: center;
  width: 100%;
}

.btn.primary {
  background: var(--clr-primary);
  color: var(--clr-text);
}

.btn.primary:hover {
  background: var(--clr-primary-dark);
}
</style>
