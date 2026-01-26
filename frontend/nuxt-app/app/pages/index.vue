<template>
  <div class="page-wrapper paper-background">
    <LogoLg />

    <div class="button-group" v-if="userState === UserStates.NOT_STARTED">
      <button class="btn primary" disabled>活动报名暂未开始</button>

      <div class="info-block">
        <span class="info-text">距开始还有</span>
        <span class="countdown">{{ nextStatusCountdown }}</span>
      </div>

    </div>
    <div class="button-group" v-else-if="userState === UserStates.APPLICATION_START">
      <button @click="navigateTo('/apply')" class="btn primary">参加一周CP</button>

      <div class="info-block">
        <span class="info-text">距报名截止还有</span>
        <span class="countdown">{{ nextStatusCountdown }}</span>
      </div>

    </div>
    <div class="button-group" v-else-if="userState === UserStates.APPLIED">
      <button @click="navigateTo('/payment')" class="btn primary">支付押金</button>
      <div class="row">
        <button @click="navigateTo('/apply')" class="btn">修改报名</button>
        <button @click="navigateTo('/withdraw')" class="btn danger">取消报名</button>
      </div>

      <div class="info-block">
        <span class="info-text">距报名截止还有</span>
        <span class="countdown">{{ nextStatusCountdown }}</span>
      </div>

    </div>
    <div class="button-group" v-else-if="userState === UserStates.PAID">
      <button @click="navigateTo('/apply')" class="btn primary">修改报名内容</button>
      <button @click="navigateTo('/withdraw')" class="btn danger">取消报名</button>

      <div class="info-block">
        <span class="info-text">距匹配开始还有</span>
        <span class="countdown">{{ nextStatusCountdown }}</span>
      </div>

    </div>
    <div class="button-group" v-else-if="userState === UserStates.QUITTED">
      <button class="btn secondary" disabled>你已退出活动</button>

      <div class="info-block">
        <span class="info-text">押金将在活动结束后退还, 期待与你的下次相遇</span>
      </div>

    </div>
    <div class="button-group" v-else-if="userState === UserStates.APPLICATION_END">
      <button class="btn primary" disabled>报名已截止</button>

      <div class="info-block">
        <span class="info-text">感谢你的关注, 期待与你的下次相遇</span>
      </div>

    </div>
    <div class="button-group" v-else-if="userState === UserStates.WAITING_FOR_FIRST_MATCH_RESULT">
      <button class="btn primary" disabled>第一轮匹配中...</button>

      <div class="info-block">
        <span class="info-text">距发布第一轮还有</span>
        <span class="countdown">{{ nextStatusCountdown }}</span>
      </div>

    </div>
    <div class="button-group" v-else-if="userState === UserStates.FIRST_MATCH_RESULT_RELEASE">
      <button class="btn primary" @click="navigateTo('/match-result')">查看我的匹配</button>

      <div class="info-block">
        <span class="info-text">距第一轮确认截止还有</span>
        <span class="countdown">{{ nextStatusCountdown }}</span>
      </div>

    </div>
    <div class="button-group" v-else-if="userState === UserStates.FIRST_MATCH_CONFIRM_END">
      <button class="btn primary" @click="navigateTo('/match-result')">查看我的匹配</button>

      <div class="info-block">
        <span class="info-text">距发布第二轮还有</span>
        <span class="countdown">{{ nextStatusCountdown }}</span>
      </div>

    </div>
    <div class="button-group" v-else-if="userState === UserStates.SECOND_MATCH_RESULT_RELEASE">
      <button class="btn primary" @click="navigateTo('/match-result')">查看我的匹配</button>

      <div class="info-block">
        <span class="info-text">距活动开始还有</span>
        <span class="countdown">{{ nextStatusCountdown }}</span>
      </div>

    </div>
    <div class="button-group" v-else-if="userState === UserStates.ACTIVITY_START">
      <button class="btn primary" @click="navigateTo('/match')">开启CP之旅</button>
    </div>
    <div class="button-group" v-else-if="userState === UserStates.EXIT_QUESTIONNAIRE_RELEASE">
      <button class="btn primary" @click="navigateTo('/match')">开启CP之旅</button>
      <button class="btn" @click="navigateTo('/exit-questionnaire')">填写结束问卷</button>

      <div class="info-block">
        <span class="info-text">距问卷填写截止还有</span>
        <span class="countdown">{{ nextStatusCountdown }}</span>
      </div>

    </div>
    <div class="button-group" v-else-if="userState === UserStates.EXIT_QUESTIONNAIRE_END">
      <button class="btn primary" @click="navigateTo('/match')">查看我的一周CP</button>
      <button class="btn secondary" disabled>问卷填写已截止</button>
    </div>
    <div class="button-group" v-else-if="userState === UserStates.MAINTENANCE">
      <button class="btn primary" disabled>维护中...</button>

      <div class="info-block">
        <span class="info-text">我们正在对服务器进行必要的维护，预计维护结束时间：{{ nextStatusChange?.toLocaleString() }}</span>
      </div>

    </div>
    <div class="button-group" v-else>
      <button class="btn primary" disabled>出现了一个错误</button>

      <div class="info-block">
        <span class="info-text">请稍后再试, 如果问题持续出现, 请联系管理员</span>
      </div>

    </div>

    <div class="decor" id="decor">
      <img src="@/assets/imgs/cupid.png" alt="decor" class="decor-img">
    </div>
    <div class="help-button">
      <button @click="openHelpModal">
        <IconQuestionMark size="2rem" color="#EEEEEE" />
      </button>
    </div>

    <Modal v-model="showHelpModal" class="help-modal">
      <div class="help-modal-content">
        <h2 class="help-modal-title">帮助与缓存</h2>
        <p class="help-modal-text">如果遇到显示异常或状态不更新，可以先尝试清理缓存自助解决。</p>
        <p class="help-modal-text">如果问题仍未解决，请添加管理员微信号并说明问题:</p>
        <ul class="help-modal-list">
          <li class="mentor-info">
            <span class="mentor-info-label">网站技术负责人: </span>
            <span class="mentor-info-value">charlieop_</span>
          </li>
          <li class="mentor-info">
            <span class="mentor-info-label">活动负责人: </span>
            <span class="mentor-info-value">Azzhleon2</span>
          </li>
        </ul>

        <div class="help-modal-actions">
          <button class="btn danger" @click="clearCache">清理缓存</button>
          <button class="btn secondary" @click="showHelpModal = false">返回</button>
        </div>
      </div>
    </Modal>
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

const showHelpModal = ref(false);

function openHelpModal() {
  showHelpModal.value = true;
}

function clearCache() {
  localStorage.clear();
  window.location.reload();
}
</script>

<style scoped>
.page-wrapper {
  overflow: hidden;
}

.help-button {
  position: absolute;
  top: 1rem;
  left: 1rem;
}

.help-button button {
  background: none;
  border: none;
  cursor: pointer;
}

.help-modal :deep(.modal-content) {
  max-width: min(420px, 90vw);
}

.help-modal-content {
  text-align: left;
  display: grid;
  gap: 0.75rem;
}

.help-modal-title {
  font-size: var(--fs-600);
  font-weight: 600;
  margin: 0;
}

.help-modal-text {
  font-size: var(--fs-300);
  color: var(--clr-text);
  margin: 0;
}

.help-modal-actions {
  margin-top: 2rem;
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

.help-modal-actions .btn {
  font-size: var(--fs-400);
  padding-inline: 1.5rem;
}

.secondary {
  background: #BBBBBB;
}

.help-modal-list {
  list-style: disc;
  padding: 0;
  margin-top: -0.5rem;
  margin-left: 1.5rem;
}

.row {
  width: 100%;
  display: flex;
  flex-direction: row;
  gap: 0.5rem;
  justify-content: center;
  align-items: center;
}

.row>* {
  flex: 1;
}

.info-block {
  display: flex;
  flex-direction: row;
  gap: 0.25rem;
  justify-content: center;
  align-items: center;
}

.info-text {
  font-size: var(--fs-300);
}

.countdown {
  font-size: var(--fs-300);
  font-weight: bold;
  color: var(--clr-primary-fixed);
}

.decor {
  position: absolute;
  bottom: 0;
  left: -3%;
  width: 66%;
  animation: float 3s ease-in-out infinite alternate;
}

@keyframes float {
  0% {
    transform: translate(-3px, 2px);
  }

  100% {
    transform: translate(3px, -2px);
  }

}

.decor-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>