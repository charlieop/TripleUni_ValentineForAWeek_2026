<template>
  <div class="page-wrapper">
    <h1>一周CP 2026</h1>
    <p class="info-text">当前状态: {{ userState }}</p>
    <p class="info-text">截止时间: {{ nextStatusChange }}</p>

    <div class="button-group" v-if="userState === UserStates.NOT_STARTED">
      <button class="btn primary" disabled>活动报名暂未开始</button>
      <p class="info-text">报名开始倒计时: {{ nextStatusCountdown }}</p>
    </div>
    <div class="button-group" v-else-if="userState === UserStates.APPLICATION_START">
      <button @click="navigateTo('/apply')" class="btn primary">参加一周CP</button>
      <p class="info-text">报名截止倒计时: {{ nextStatusCountdown }}</p>
    </div>
    <div class="button-group" v-else-if="userState === UserStates.APPLIED">
      <button @click="navigateTo('/apply')" class="btn primary">修改报名内容</button>
      <button @click="navigateTo('/payment')" class="btn primary">支付押金</button>
      <button @click="navigateTo('/withdraw')" class="btn secondary">取消报名</button>
      <p class="info-text">押金支付倒计时: {{ nextStatusCountdown }}</p>
    </div>
    <div class="button-group" v-else-if="userState === UserStates.PAID">
      <button @click="navigateTo('/apply')" class="btn primary">修改报名内容</button>
      <button @click="navigateTo('/withdraw')" class="btn secondary">取消报名</button>
      <p class="info-text">匹配开始倒计时: {{ nextStatusCountdown }}</p>
    </div>
    <div class="button-group" v-else-if="userState === UserStates.QUITTED">
      <button class="btn secondary" disabled>你已退出活动</button>
    </div>
    <div class="button-group" v-else-if="userState === UserStates.APPLICATION_END">
      <button class="btn primary" disabled>报名已截止</button>
    </div>
    <div class="button-group" v-else-if="userState === UserStates.WAITING_FOR_FIRST_MATCH_RESULT">
      <button class="btn primary" disabled>第一轮匹配中...</button>
      <p class="info-text">第一轮匹配结果放出倒计时: {{ nextStatusCountdown }}</p>
    </div>
    <div class="button-group" v-else-if="userState === UserStates.FIRST_MATCH_RESULT_RELEASE">
      <button class="btn primary" @click="navigateTo('/match-result')">查看我的匹配</button>
      <p class="info-text">第一轮匹配结果确认截止倒计时: {{ nextStatusCountdown }}</p>
    </div>
    <div class="button-group" v-else-if="userState === UserStates.FIRST_MATCH_CONFIRM_END">
      <button class="btn primary" @click="navigateTo('/match-result')">查看我的匹配</button>
      <p class="info-text">第二轮匹配结果放出倒计时: {{ nextStatusCountdown }}</p>
    </div>
    <div class="button-group" v-else-if="userState === UserStates.SECOND_MATCH_RESULT_RELEASE">
      <button class="btn primary" @click="navigateTo('/match-result')">查看我的匹配</button>
      <p class="info-text">活动开始倒计时: {{ nextStatusCountdown }}</p>
    </div>
    <div class="button-group" v-else-if="userState === UserStates.ACTIVITY_START">
      <button class="btn primary" @click="navigateTo('/match')">开启CP之旅</button>
    </div>
    <div class="button-group" v-else-if="userState === UserStates.EXIT_QUESTIONNAIRE_RELEASE">
      <button class="btn primary" @click="navigateTo('/match')">开启CP之旅</button>
      <button class="btn secondary" @click="navigateTo('/exit-questionnaire')">填写结束问卷</button>
      <p class="info-text">问卷填写截止倒计时: {{ nextStatusCountdown }}</p>
    </div>
    <div class="button-group" v-else-if="userState === UserStates.EXIT_QUESTIONNAIRE_END">
      <button class="btn primary" @click="navigateTo('/match')">查看我的一周CP</button>
      <button class="btn secondary" disabled>问卷填写已截止</button>
    </div>
    <div class="button-group" v-else>
      <button class="btn primary" disabled>出现了一个错误</button>
      <p class="info-text">请稍后再试, 如果问题持续出现, 请联系管理员</p>
    </div>
    <button @click="clearCache" class="btn">清除缓存</button>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: "一周CP 2026 | 首页",
});

watch(nextStatusDeadlineReached, (newVal) => {
  if (newVal) {
    fetchUserState();
  }
});

function clearCache() {
  localStorage.clear();
  window.location.reload();
}
</script>

<style scoped>
.page-wrapper {
  padding: 1.5rem;
  max-width: 100%;
  margin: 0 auto;
}

h1 {
  font-size: var(--fs-700);
  color: var(--clr-primary);
  margin-bottom: 2rem;
  text-align: center;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
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
}

.btn.primary {
  background: var(--clr-primary);
  color: var(--clr-text);
}

.btn.primary:hover {
  background: var(--clr-primary-dark);
}

.btn.secondary {
  background: var(--clr-secondary);
  color: var(--clr-text);
}

.btn.secondary:hover {
  background: var(--clr-secondary-dark);
}
</style>