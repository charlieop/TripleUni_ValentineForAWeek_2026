<template>
  <div class="page-wrapper paper-background">

    <LogoLg />

    <div class="content-wrapper">
      <a :href="url" v-if="!hasCode">
        <button class="btn primary">登录微信授权</button>
      </a>
      <button class="btn primary" v-else @click="reloadPage">重试</button>


      <div class="notes">
        <img src="/imgs/login-text-bg.webp" alt="" class="note-bg">
        <div class="note-content">
          <template v-if="!hasCode">
            <h1>请使用<strong>真实账户</strong>授权</h1>
            <div class="info-section">
              <p class="info-text">注意: 请 <strong>不要使用虚拟账户</strong> (momo)</p>
              <p class="info-text">
                我们需要获取你的 <strong>真实</strong> 用户昵称及头像用作匹配目的,
                虚拟账号将被<strong>取消资格</strong>
              </p>
            </div>
          </template>
          <template v-else>
            <h1>正在获取OpenId...</h1>
            <div class="info-section">
              <p class="info-text">请稍候...</p>
            </div>
          </template>

        </div>
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
const requestURL = "https://wechat-oauth.tripleuuunnniii.com";

let url =
  requestURL +
  "?appid=" +
  APPID +
  "&redirect_uri=" +
  encodeURIComponent(window.location.href) +
  "&response_type=code&scope=snsapi_userinfo#wechat_redirect";

onMounted(() => {
  const code = queryParams.code;

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

function reloadPage() {
  const url = new URL(window.location.href);
  window.location.href = url.origin;
}
</script>

<style scoped>
.content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.notes {
  margin-top: 3.5rem;
  position: relative;
  width: 100%;
}

.note-bg {
  width: 100%;
  height: 100%;
  z-index: 1;
  object-fit: contain;
  scale: 1.2;
}

a {
  width: 100%;
}

button {
  display: block;
  width: 80%;
  margin: 0 auto;
}

.note-content {
  position: absolute;
  inset: -8% 7% 30% 12%;
  z-index: 1;
  padding: 1.25rem 0.25rem;
}

h1 {
  margin-left: 1rem;
  text-align: center;
  font-size: var(--fs-500)
}

h1 strong {
  font-size: 1.25em;
}

.info-section {
  margin-top: 1rem;
}
</style>