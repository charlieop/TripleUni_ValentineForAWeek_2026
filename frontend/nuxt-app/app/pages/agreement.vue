<template>
  <div class="page-wrapper paper-background">
    <LogoSm />

    <div class="content-wrapper">
      <div class="agreement-card">
        <h1 class="agreement-title">一周CP 2026 协议书</h1>

        <div class="agreement-content">
          <div class="party-section">
            <p><strong>甲方：</strong>Triple Uni（下称"甲方"）</p>
            <p><strong>乙方：</strong>活动参与者（下称"乙方"）</p>
          </div>

          <p class="intro-text">
            欢迎各位参加Triple Uni举办的本次"一周CP 2026"活动(下称"活动")，因活动需要，甲、乙双方均应对本协议各项条款知情并遵守。
          </p>

          <p class="section-intro">现就有关事项协议如下：</p>

          <div class="agreement-item">
            <div class="item-number">第一条</div>
            <p class="item-content">
              乙方在活动开始时应已在报名网站（<span
                class="link">https://valentine.tripleuni.com/</span>）上缴纳押金99元人民币（包括每日任务押金70元，完成3日主线任务押金20元，结束反馈问卷押金9元）。该笔款项会根据乙方完成情况在活动结束后退还。如乙方中途退出活动，需征得同组参与者同意。甲方将在扣除未完成任务之押金后，依据乙方参与活动之数目退还款项。例如乙方完成三日任务后中途退出，则甲方依协议退还50元人民币（10
              * 3 + 20)，剩余押金不予返还。
            </p>
          </div>

          <div class="agreement-item">
            <div class="item-number">第二条</div>
            <p class="item-content">
              乙方在报名时已详细阅读并理解上述报名网站上所提及的活动规则，如出现由于乙方未理解规则而导致的活动无法正常进行的情况，造成的相应损失，包括但不限于押金损失，由乙方承担。
            </p>
          </div>

          <div class="agreement-item">
            <div class="item-number">第三条</div>
            <p class="item-content">
              因活动需要，甲方邀请特邀mentor(下称"第三人")出任日常维系工作，第三人已根据甲方与其协议承诺：
            </p>
            <p class="item-subcontent">
              不得以任何形式向任何与活动无关之第三方泄漏其所负责协调之活动参与者的任何个人信息及本次活动相关资料，包括但不限于：姓名、联系方式等资料。
            </p>
            <p class="item-content">
              如违反上述承诺，则：
            </p>
            <ol class="item-list">
              <li>甲方将撤销第三人协助资格</li>
              <li>甲方对第三人行为不承担任何责任</li>
              <li>乙方有权保留其追究第三人对甲方侵权行为之责任的权利，如乙方有意愿追究第三人责任，甲方将为其提供第三人提交予甲方的相关个人信息。</li>
            </ol>
          </div>

          <div class="agreement-item">
            <div class="item-number">第四条</div>
            <p class="item-content">
              鉴于甲方未来工作的需要，乙方承诺在活动期间及其后，不得以任何形式向第三方透露甲方工作人员的个人信息，包括但不限于：姓名、联系方式，亦不得向第三方透露本次活动相关内容资料。
            </p>
          </div>

          <div class="agreement-item">
            <div class="item-number">第五条</div>
            <p class="item-content">
              本协议不须乙方当面签署，但乙方在报名参与时应当截屏活动规则以及本协议书自行保存。乙方报名的同时，自动默认其对文件全部内容知情且认可。
            </p>
          </div>

          <div class="signature-section">
            <p class="signature-text"><strong>甲方：</strong>Triple Uni</p>
            <p class="disclaimer">本次活动Triple Uni保有最终解释权。</p>
          </div>
        </div>
      </div>

      <div class="button-group">
        <button @click="navigateTo('/apply')" class="btn primary">
          返回报名页面
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: "一周CP 2026 | 活动协议",
});
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  padding: 2rem 1.5rem;
  overflow-y: auto;
}

.content-wrapper {
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.agreement-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 1.5rem;
  padding: 2rem 1.75rem;
  box-shadow:
    0 12px 32px rgba(0, 0, 0, 0.12),
    0 0 0 1px rgba(255, 255, 255, 0.8) inset;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.agreement-title {
  font-size: var(--fs-700);
  font-weight: 900;
  color: var(--clr-primary-dark);
  text-align: center;
  margin: 0 0 1.5rem 0;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--clr-primary-light);
}

.agreement-content {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  font-size: var(--fs-300);
  line-height: 1.7;
  color: var(--clr-text);
  text-align: justify;
}

.party-section p {
  margin: 0.5rem 0;
  font-size: var(--fs-350);
}

.party-section strong {
  font-weight: 900;
  color: var(--clr-primary-dark);
}

.intro-text {
  margin: 0;
  padding: 0.75rem 0;
  font-size: var(--fs-350);
  line-height: 1.8;
}

.section-intro {
  margin: 0.5rem 0 0 0;
  font-weight: 700;
  font-size: var(--fs-400);
  color: var(--clr-primary-dark);
}

.agreement-item {
  padding: 1rem 0;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.item-number {
  display: inline-block;
  background: var(--clr-primary);
  color: white;
  font-weight: 900;
  padding: 0.25rem 0.75rem;
  border-radius: 99rem;
  margin-bottom: 0.75rem;
  font-size: var(--fs-300);
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

.item-content {
  margin: 0 0 0.5rem 0;
  font-size: var(--fs-350);
  line-height: 1.8;
}



.item-list {
  margin: 0.75rem 0 0 2rem;
  padding: 0;
  list-style: decimal;
}

.item-list li {
  margin: 0.5rem 0;
  padding-left: 0.5rem;
  font-size: var(--fs-325);
  line-height: 1.7;
}

.link {
  color: var(--clr-primary-dark);
  text-decoration: underline;
  font-weight: 600;
  transition: var(--transition);
}

.signature-section {
  margin-top: 1.5rem;
  padding: 1.25rem;
  background: var(--clr-background--muted);
  border-radius: 0.75rem;
  border: 2px solid var(--clr-primary-light);
}

.signature-text {
  margin: 0 0 0.75rem 0;
  font-size: var(--fs-400);
  font-weight: 700;
}

.disclaimer {
  margin: 0;
  font-size: var(--fs-350);
  color: var(--clr-text--muted);
  font-style: italic;
  text-align: center;
}

.button-group {
  max-width: 19rem;
  margin: 0 auto;
  width: 100%;
}

.btn {
  width: 100%;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .agreement-card {
    padding: 1.5rem 1.25rem;
    border-radius: 1rem;
  }

  .agreement-title {
    font-size: var(--fs-600);
  }

  .agreement-content {
    font-size: var(--fs-250);
  }

  .party-section p,
  .intro-text,
  .item-content {
    font-size: var(--fs-300);
  }

  .item-subcontent,
  .item-list li {
    font-size: var(--fs-275);
  }
}

/* Smooth scrolling */
.page-wrapper {
  scroll-behavior: smooth;
}

/* Print styles for screenshot */
@media print {
  .button-group {
    display: none;
  }

  .page-wrapper {
    background: white;
  }

  .agreement-card {
    box-shadow: none;
  }
}
</style>
