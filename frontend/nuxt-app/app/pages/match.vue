<template>
    <div class="page-wrapper cupid-background">
        <div class="title-wrapper">
            <h1 class="page-title">
                <template v-if="matchData">
                    <span class="group-id">#{{ matchData.match_info.id }}</span> <span class="group-name"
                        :style="{ fontSize: matchData.match_info.name.length < 10 ? 'var(--fs-700)' : 'var(--fs-600)' }">{{
                            matchData.match_info.name }}</span>
                </template>
                <template v-else>
                    <span class="group-name">我的CP组合</span>
                </template>
            </h1>
            <LogoSm />
        </div>


        <template v-if="error">
            <div class="state-card error">
                <div class="state-icon">❌</div>
                <p class="state-title">加载失败</p>
                <p class="state-message">{{ error }}</p>
            </div>
            <div class="button-group">
                <button class="btn primary" @click="loadMatchData">重试</button>
                <button class="btn" @click="navigateTo('/')">返回首页</button>
            </div>
        </template>

        <div v-else-if="matchData" class="match-content">
            <section class="cp-info-section">
                <div class="cp-info-item">
                    <div class="polaroid-frame">
                        <img :src="getImageUrl(matchData.user_info.head_image)" alt="">
                    </div>
                    <div class="name-info">
                        <p class="name">{{ matchData.user_info.name }}</p>
                    </div>
                </div>
                <div class="cp-info-item">
                    <div class="polaroid-frame">
                        <img :src="getImageUrl(matchData.partner_info.head_image)" alt="">
                    </div>
                    <div class="name-info">
                        <p class="name">{{ matchData.partner_info.name }}</p>
                        <p class="wxid">{{ matchData.partner_info.wxid }}</p>
                    </div>
                </div>
                <div class="cp-emoji">
                    <span class="emoji">{{ getConnectorEmoji(matchData.match_info.total_score) }}</span>
                </div>
            </section>

            <section class="score-section">
                <h2 class="section-title">当前状态</h2>
                <div class="score-card">
                    <div class="score-stats">
                        <div class="stat-item">
                            <div class="stat-label">天数</div>
                            <div v-if="matchData.match_info.current_day === 8" class="stat-value">结束</div>
                            <div v-else class="stat-value">Day {{ matchData.match_info.current_day }}</div>
                        </div>
                        <div class="stat-divider"></div>
                        <div class="stat-item">
                            <div class="stat-label">总分</div>
                            <div class="stat-value score-value">{{ matchData.match_info.total_score }}</div>
                        </div>
                        <div class="stat-divider"></div>
                        <div class="stat-item">
                            <div class="stat-label">排名</div>
                            <div class="stat-value rank-value">
                                <span class="rank-number">#{{ matchData.match_info.rank }}</span>
                                <span class="rank-badge" v-if="matchData.match_info.rank === 1">👑</span>
                                <span class="rank-badge" v-else-if="matchData.match_info.rank === 2">🥈</span>
                                <span class="rank-badge" v-else-if="matchData.match_info.rank === 3">🥉</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="actions-section">
                <button class="btn primary" @click="openMentorModal">
                    Mentor信息
                </button>
                <button class="btn primary" @click="openRulesModal">
                    查看活动规则
                </button>
                <button class="btn primary" @click="openNameModal">
                    修改组名
                </button>

                <button v-if="userState === UserStates.EXIT_QUESTIONNAIRE_RELEASE" class="btn dark"
                    @click="navigateTo('/exit-questionnaire')">
                    填写结束问卷
                </button>
            </section>

            <section class="tasks-section">
                <h2 class="section-title">任务进度</h2>
                <div class="tasks-grid">
                    <button class="task-card link-uni" @click="linkUNI"
                        :class="{ completed: matchData.user_info.linked_uni }">
                        <img src="/imgs/tripleuni-logo.webp" alt="绑定triple uni" class="task-icon">
                    </button>

                    <button v-for="day in 7" :key="day" class="task-card" :class="{
                        'completed': matchData.match_info.basic_complete[day - 1],
                        'disabled': day > matchData.match_info.current_day,
                        'past': day < matchData.match_info.current_day
                    }" :disabled="day > matchData.match_info.current_day" @click="navigateTo(`/tasks/${day}`)">
                        <div class="task-day">Day {{ day }}</div>
                        <div class="task-status">
                            <span v-if="matchData.match_info.basic_complete[day - 1]">✓</span>
                            <span v-else-if="day < matchData.match_info.current_day">✗</span>
                            <span v-else-if="day > matchData.match_info.current_day">🔒</span>
                            <span v-else>→</span>
                        </div>
                    </button>
                    <button class="task-card secret-mission" @click="navigateTo('/tasks/secret')">
                        <div class="task-day">秘密任务</div>
                    </button>
                </div>
            </section>

            <section class="exit-section">
                <button class="btn primary" @click="navigateTo('/')">
                    返回首页
                </button>
            </section>
        </div>

        <!-- Name Change Modal -->
        <Modal v-model="showNameModal">
            <h2 class="modal-title">修改组名</h2>
            <div class="modal-form">
                <label for="name-input" class="form-label">新组名</label>
                <input id="name-input" v-model="newMatchName" type="text" class="form-input" maxlength="30"
                    placeholder="请输入新的组名" @keyup.enter="saveMatchName" />
                <p class="form-hint">最多30个字符</p>
                <div class="modal-actions">
                    <button class="btn dark" @click="saveMatchName">保存</button>
                </div>
            </div>
        </Modal>

        <!-- Mentor Info Modal -->
        <Modal v-model="showMentorModal">
            <h2 class="modal-title">Mentor信息</h2>
            <div class="mentor-info">
                <div class="mentor-detail">
                    <span class="detail-label">姓名:</span>
                    <span class="detail-value">{{ matchData.mentor_info.name }}</span>
                </div>
                <div class="mentor-detail">
                    <span class="detail-label">微信号:</span>
                    <span class="detail-value">{{ matchData.mentor_info.wxid }}</span>
                </div>
            </div>
            <div class="mentor-qrcode">
                <img :src="getImageUrl(matchData.mentor_info.qrcode)" alt="Mentor微信二维码" class="qrcode-image" />
            </div>
            <div class="modal-actions">
                <button class="btn dark" @click="() => { showMentorModal = false }">完成</button>
            </div>

        </Modal>

        <!-- Rules Help Modal -->
        <Modal v-model="showRulesModal">
            <h2 class="modal-title">📋 活动规则</h2>
            <div class="rules-content">
                <ul class="rules-list">
                    <li>在刚刚添加你的CP时, 请<strong>向对方屏蔽你的朋友圈</strong></li>
                    <li>活动为期<strong>7天</strong>，每天都有新任务解锁</li>
                    <li>完成任务可以获得<strong>积分</strong>，积分越高排名越靠前</li>
                    <li>任务分为基础任务、支线任务与每日任务, <strong>基础任务为每日必做</strong>, 支线任务与每日任务为可选任务</li>
                    <li>每天任务提交截止时间为下一天<strong>05:59 AM</strong></li>
                    <li>提交的任务将在截止后由AI模型自动评分, <strong>请不要遮挡/ 拼接/ 模糊你提交的图片</strong>以确保评分准确</li>
                    <li>如有问题请及时联系 Mentor 获取帮助</li>
                    <li>预祝你享受这段美好时光 💖</li>
                </ul>
            </div>
            <div class="rules-checkbox" v-if="!getDoNotShowHelpModal()">
                <label class="checkbox-label">
                    <input type="checkbox" v-model="doNotShowAgain" />
                    <span>不再提示</span>
                </label>
            </div>
            <div class="modal-actions">
                <button class="btn dark" @click="closeRulesModal">知道了</button>
            </div>
        </Modal>

        <!-- Link Uni Modal -->
        <Modal v-model="showLinkUniModal">
            <h2 class="modal-title">绑定Triple Uni账户</h2>
            <div class="link-uni-content">
                <p class="link-uni-message">
                    我们将使用你填写的教育邮箱来关联Triple Uni账户。
                </p>
                <p class="link-uni-desc">
                    部分任务包含 Triple Uni 的一周CP板块中参与互动。为确保你拥有发言权限以及自动记分, 请授权并绑定Triple Uni账户。
                </p>
                <p class="link-uni-hint">
                    如果绑定失败，请先注册Triple Uni账户，或联系 Mentor 修改你注册的邮箱。
                </p>
            </div>
            <div class="modal-actions">
                <button class="btn dark" @click="linkUniAccount">授权并绑定</button>
                <div class="row">
                    <a href="https://login.tripleuni.com/TripleUni?callback=%2Fhome" target="_blank" class="btn">
                        去注册
                    </a>
                    <button class="btn" @click="() => { showLinkUniModal = false }">取消</button>
                </div>
            </div>
        </Modal>
    </div>
</template>

<script setup lang="ts">
const { get, post } = useRequest();
const { setDoNotShowHelpModal, getDoNotShowHelpModal } = useStore();
const matchData = ref<any>(null);
const error = ref<string | null>(null);
const showNameModal = ref(false);
const showMentorModal = ref(false);
const showRulesModal = ref(false);
const showLinkUniModal = ref(false);
const doNotShowAgain = ref(false);
const newMatchName = ref("");

useHead({
    title: computed(() => matchData.value
        ? `一周CP 2026 | ${matchData.value.match_info.name}`
        : "一周CP 2026 | 我的CP组合"),
});

const getConnectorEmoji = (score: number): string => {
    // Emoji progression representing relationship stages based on score
    if (score === 0) {
        return '👋';
    } else if (score <= 50) {
        return '💬';
    } else if (score <= 100) {
        return '👥';
    } else if (score <= 200) {
        return '🥰';
    } else if (score <= 300) {
        return '💕';
    } else if (score <= 400) {
        return '💖';
    } else if (score <= 500) {
        return '💌';
    } else {
        return '❤️‍🔥';
    }
};

const loadMatchData = async () => {
    error.value = null;

    try {
        const res = await get("match/");
        if (res.ok) {
            const data = await res.json();
            matchData.value = data.data;
            newMatchName.value = data.data.match_info.name;
        } else {
            const errorData = await res.json();
            throw new Error(errorData.detail || res.statusText);
        }
    } catch (err: any) {
        error.value = err.message || '加载匹配详情失败';
        console.error(err);
    }
};

const linkUNI = () => {
    if (matchData.value.user_info.linked_uni) {
        alert("已绑定Triple Uni账户");
        return;
    }
    showLinkUniModal.value = true;
};

const linkUniAccount = async () => {
    try {
        const res = await post("link-uni/");
        if (res.ok) {
            if (matchData.value) {
                matchData.value.user_info.linked_uni = true;
            }
            showLinkUniModal.value = false;
            alert("成功绑定Triple Uni账户！");
        } else {
            const errorData = await res.json();
            const errorMessage = errorData.detail || res.statusText;
            alert(`绑定失败：${errorMessage}\n\n请先注册Triple Uni账户，或联系 Mentor 修改你注册的邮箱。`);
        }
    } catch (err: any) {
        alert(`绑定失败：${err.message || '网络错误'}\n\n请先注册Triple Uni账户，或联系 Mentor 修改你注册的邮箱。`);
        console.error(err);
    }
};

const openNameModal = () => {
    if (matchData.value) {
        newMatchName.value = matchData.value.match_info.name;
        showNameModal.value = true;
    }
};

const openMentorModal = () => {
    showMentorModal.value = true;
};

const openRulesModal = () => {
    showRulesModal.value = true;
};

const saveMatchName = async () => {
    if (!newMatchName.value.trim()) {
        alert('组名不能为空');
        return;
    }

    if (newMatchName.value.length > 30) {
        alert('组名不能超过30个字符');
        return;
    }

    try {
        const res = await post("match/", { name: newMatchName.value.trim() });
        if (res.ok) {
            const data = await res.json();
            if (matchData.value) {
                matchData.value.match_info.name = newMatchName.value.trim();
            }
            showNameModal.value = false;
        } else {
            const errorData = await res.json();
            throw new Error(errorData.detail || res.statusText);
        }
    } catch (err: any) {
        alert(err.message || '更新组名失败');
        console.error(err);
    }
};

const closeRulesModal = () => {
    if (doNotShowAgain.value) {
        setDoNotShowHelpModal(true);
    }
    showRulesModal.value = false;
};

onMounted(() => {
    loadMatchData();

    // Show rules modal unless user has opted out
    if (!getDoNotShowHelpModal()) {
        showRulesModal.value = true;
    }
});
</script>

<style scoped>
.page-wrapper {
    height: var(--height);
    overflow-y: scroll;
}

.title-wrapper {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.group-id {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    top: -1.5rem;
    color: #6e6e6e;
    font-size: var(--fs-600);
}

.group-name {
    display: inline-block;
    text-wrap: balance;
}

h1 {
    position: relative;
    font-size: var(--fs-700);
    width: 100%;
}

section {
    padding-inline: 0.75rem;
}

.cp-info-section {
    margin-top: 3rem;
    display: flex;
    flex-direction: row;
    align-items: start;
    justify-content: center;
    gap: 5rem;
    position: relative;
}

.cp-info-item {
    width: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.polaroid-frame {
    position: relative;
    width: 100%;
    aspect-ratio: 1/1.15;
    background: white;
    padding: 5%;
    box-shadow: 1px 1px 10px 0 rgba(0, 0, 0, 0.2);
}

.polaroid-frame img {
    object-fit: cover;
    background: var(--clr-text--muted);
}

.name-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: -0.25rem;
    backdrop-filter: blur(1px);
    -webkit-backdrop-filter: blur(1px);
    padding: 0.125rem 0.5rem;
    border-radius: 0.5rem;

}

.name {
    font-size: var(--fs-400);
    font-weight: bold;
}

.wxid {
    font-size: var(--fs-300);
    font-weight: bold;
}

.cp-emoji {
    position: absolute;
    top: 40%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: var(--fs-700);
    font-weight: bold;
    animation: pulse 3s infinite ease-in-out;
}

@keyframes pulse {
    0% {
        transform: translate(-50%, -50%) scale(1);
    }

    50% {
        transform: translate(-50%, -50%) scale(1.1);
    }

    100% {
        transform: translate(-50%, -50%) scale(1);
    }
}

.score-section {
    margin-top: 2rem;
}

.score-card {
    background: #FFFFFF;
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.score-stats {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-around;
    gap: 1rem;
}

.stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    flex: 1;
}

.stat-label {
    font-size: var(--fs-300);
    color: var(--clr-text--muted);
    font-weight: 600;
    letter-spacing: 0.05em;
}

.stat-value {
    font-size: var(--fs-600);
    color: var(--clr-text);
    font-weight: 900;
}

.score-value {
    color: var(--clr-primary);
}

.rank-value {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 0.25rem;
}

.rank-number {
    color: var(--clr-primary-dark);
}

.rank-badge {
    font-size: var(--fs-500);
}

.stat-divider {
    width: 1px;
    height: 3rem;
    background: var(--clr-text--muted);
    opacity: 0.3;
}

.actions-section {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
    width: 100%;
    margin-top: 2rem;
}

.actions-section>button {
    flex-grow: 1;
}

.tasks-section {
    margin-top: 3rem;
}

.section-title {
    font-size: var(--fs-600);
    color: var(--clr-primary-dark);
    font-weight: 900;
    text-align: left;
    margin-bottom: .5rem;
    padding-inline: 0.5rem;
}

.tasks-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(70px, 1fr));
    gap: 1rem;
}

.task-card {
    background: #FBFBFB80;
    backdrop-filter: blur(2px);
    -webkit-backdrop-filter: blur(2px);
    border-radius: 1rem;
    padding: 1rem 1rem;
    text-align: center;
    box-shadow: 1px 1px 10px 0 rgba(0, 0, 0, 0.15);
    border: 0.75px solid #FAFAFA80;
    cursor: pointer;
    transition: var(--transition);
    color: var(--clr-text);
    font-weight: bold;
}

.task-card:not(.disabled):hover {
    transform: translateY(-4px);
    box-shadow: 2px 4px 16px 0 rgba(0, 0, 0, 0.2);
}

.task-card:not(.disabled):active {
    transform: translateY(-2px);
}

.task-card.link-uni img {
    scale: 1.2;
}

.task-card.secret-mission {
    background: #faedcf96
}

.task-card.secret-mission .task-day {
    text-wrap: balance;
    line-height: 1.2;

}

.past:not(.completed) {
    background: #6e6e6e7c;
    border-color: #6e6e6e7c;
}

.task-card.completed {
    background: var(--clr-primary-light);
    border-color: var(--clr-primary);
}

.task-card.disabled {
    opacity: 0.5;
    cursor: not-allowed;
    filter: grayscale(0.6);
}

.task-day {
    font-size: var(--fs-400);
    margin-bottom: 0.5rem;
}

.task-status {
    font-size: var(--fs-600);
}

.exit-section {
    margin-block: 3rem 5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

/* Modal Specific Styles */
.modal-title {
    font-size: var(--fs-600);
    color: var(--clr-primary-dark);
    font-weight: 900;
    margin-bottom: 1.5rem;
    text-align: center;
}

.modal-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.form-label {
    font-size: var(--fs-400);
    font-weight: 600;
    color: var(--clr-text);
}

.form-input {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid var(--clr-text--muted);
    border-radius: 0.5rem;
    font-size: var(--fs-400);
    background: var(--clr-background);
    color: var(--clr-text);
    font-family: inherit;
    box-sizing: border-box;
}

.form-input:focus {
    outline: none;
    border-color: var(--clr-primary);
}

.form-hint {
    font-size: var(--fs-300);
    color: var(--clr-text--muted);
    margin-top: -0.5rem;
}

.modal-actions {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-top: 1rem;
}

.btn.dark {
    text-shadow: none;
    background: var(--clr-primary-dark);
    color: #EFEFEF;
}

.mentor-info {
    display: flex;
    flex-direction: row;
    gap: 1rem;
}

.mentor-detail {
    position: relative;
    min-width: 4rem;
    padding: 0.5rem 0.75rem;
    background: var(--clr-background--muted);
    border-radius: 0.5rem;
}

.detail-label {
    position: absolute;
    left: 0;
    top: -0.75rem;
    display: inline-block;
    font-size: var(--fs-200);
    color: var(--clr-text--muted);
}

.detail-value {
    font-size: var(--fs-400);
    color: var(--clr-text);
}

.mentor-qrcode {
    width: 100%;
    margin-top: 1rem;
    text-align: center;
}

.qrcode-image {
    margin-inline: auto;
    width: 80%;
    max-width: 250px;
    height: auto;
    border-radius: 0.5rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.rules-content {
    margin-top: 1rem;
}

.rules-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.rules-list li {
    position: relative;
    padding: 0.5rem;
    background: var(--clr-background--muted);
    border-radius: 0.5rem;
    font-size: var(--fs-300);
}

.rules-list li strong {
    color: var(--clr-primary-dark);
    font-weight: 700;
}

.rules-checkbox {
    margin-block: 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid var(--clr-text--muted);
}

.checkbox-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    font-size: var(--fs-400);
    color: var(--clr-text);
}

.checkbox-label input[type="checkbox"] {
    width: 1.25rem;
    height: 1.25rem;
    cursor: pointer;
    accent-color: var(--clr-primary);
}

.checkbox-label span {
    user-select: none;
}

.link-uni-content {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.link-uni-message {
    font-size: var(--fs-300);
    color: var(--clr-text);
    line-height: 1.6;
    padding: 0.5rem 1rem;
    background: var(--clr-background--muted);
    border-radius: 0.5rem;
}

.link-uni-desc,
.link-uni-hint {
    padding: 0 1rem;
}

.link-uni-hint {
    font-size: var(--fs-200);
    color: var(--clr-text--muted);
    margin-bottom: 1rem;
}

.row {
    display: flex;
    flex-direction: row;
    gap: 0.75rem;
}

.row>* {
    flex: 1;
    background: #bbbbbb8a;
    color: #EEEEEE;
    text-align: center;
}
</style>
