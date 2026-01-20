<template>
  <div class="login-wrapper">
    <div class="logo"></div>
    <div class="content-wrapper" v-if="!hasCode">
      <h1>请使用真实账户授权</h1>
      <p>注意: 请 <strong>不要使用虚拟账户 </strong> (momo)</p>
      <p class="push">
        我们需要获取你的 <strong>真实</strong> 用户昵称及头像用作匹配目的,
        虚拟账号将被<strong>取消资格</strong>
      </p>
      <a :href="url">
        <button class="btn primary">登录微信授权</button>
      </a>
    </div>
    <div class="content-wrapper" v-else>
      <h1>正在获取OpenId...</h1>
      <p class="push">请稍候...</p>
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
.login-wrapper {
  width: 100%;
  height: 100%;
  padding: 0.5rem 1rem;
  position: relative;
  overflow: hidden;
}

.content-wrapper {
  line-height: 1.5;
  padding: 0 1.5rem;
}

h1 {
  font-size: var(--fs-700);
  color: var(--clr-primary);
  text-align: center;
  margin-bottom: 0.5em;
  letter-spacing: 2px;
}
.push {
  padding-left: 4ch;
}
strong {
  color: var(--clr-accent);
  text-decoration: underline;
  text-underline-position: under;
  text-decoration-thickness: 1px;
  font-size: 1.1em;
}
button {
  position: relative;
  z-index: 1;
  display: block;
  width: 90%;
  margin: 2vh auto;
  font-size: var(--fs-500);
}

.decor-couple {
  position: absolute;
  width: 80%;
  left: 10%;
  bottom: -0.5rem;
}
.decor-heart {
  position: absolute;
  width: 40%;
  left: 27%;
  bottom: 14%;
  animation: updown 7s infinite ease-in-out;
}
@keyframes updown {
  0% {
    transform: translateY(0.25rem);
  }
  50% {
    transform: translateY(-0.25rem) scale(1.05);
  }
  100% {
    transform: translateY(0.25rem);
  }
}
</style>
