<template>
  <div class="page-wrapper paper-background">

    <LogoLg />

    <div class="content-wrapper">
      <div class="button-group">
        <button class="btn primary" @click="refresh">刷新</button>
      </div>
      <div class="notes">
        <img src="@/assets/imgs/login-text-bg.png" alt="" class="note-bg">
        <div class="note-content">
          <h1><strong>维护中...</strong></h1>
          <div class="info-section">
            <p class="info-text">
              我们正在对服务器进行必要的维护，预计维护结束时间：<strong>{{ nextStatusChange?.toLocaleString() }}</strong>
            </p>
          </div>
        </div>
      </div>
    </div>


  </div>
</template>

<script setup lang="ts">
useHead({
  title: "一周CP 2026 | 维护中...",
});

function refresh() {
  window.location.reload();
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