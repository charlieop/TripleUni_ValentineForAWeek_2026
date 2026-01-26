<template>
    <div class="page-wrapper heart-background">
        <LogoSm />
        <h1 class="page-title">第{{ round }}轮匹配结果</h1>
        <template v-if="error">
            <div class="state-card error">
                <div class="state-icon">❌</div>
                <p class="state-title">加载失败</p>
                <p class="state-message">{{ error }}</p>
            </div>
            <div class="button-group">
                <button class="btn primary" @click="loadMatchResult">重试</button>
                <button class="btn" @click="navigateTo('/')">返回首页</button>
            </div>
        </template>

        <template v-else-if="no_match || (matchData?.match_info?.discarded && round === 2)">
            <div class="state-card empty" v-if="round === 1">
                <div class="state-icon">💌</div>
                <p class="state-title">暂未匹配成功</p>
                <p class="state-message">
                    很遗憾, 在第一轮中我们未能为你找到一个合适的人选.
                </p>
                <p class="state-message">
                    请耐心等候, 我们将在一天后再次启动匹配, 为你寻找合适的那个ta.
                </p>
                <p class="state-message">
                    <br>
                    祝你好运, 我们明天不见不散.
                </p>
            </div>
            <div class="state-card empty" v-else>
                <div class="state-icon">😔</div>
                <p class="state-title"> 未能匹配成功</p>
                <p class="state-message">
                    很遗憾, 在第二轮中我们未能为你找到一个合适的人选.
                </p>
                <p class="state-message">
                    我们理解这可能让你感到失望, 但请相信, 缘分需要时间与耐心. 你的爱情或许就在不经意间悄然降临, 愿你在未来的日子中遇见那个对的人!
                </p>
                <p class="state-message">
                    感谢你对TripleUni 一周CP 2026活动的关注与支持. 我们将在活动结束后统一处理退款.
                </p>
                <p class="state-message">
                    <br>祝你一切顺利,<br>幸福常在!
                </p>
            </div>
            <div class="button-group">
                <button class="btn primary" @click="navigateTo('/')">返回首页</button>
            </div>
        </template>

        <template v-else-if="matchData">
            <section class="partner-info">
                <div class="partner-info-item">
                    <div class="polaroid-frame">
                        <div class="partner-name">
                            {{ matchData.partner_info.nickname }}
                        </div>
                        <div class="polaroid-frame-img">
                            <img :src="getImageUrl(matchData.partner_info.head_image)" alt="">
                            <div v-if="!isUserAccepted" class="blur-img-overlay">
                                同意匹配后可见
                            </div>
                        </div>
                    </div>
                    <div class="partner-detail">
                        <h2>你的CP♥</h2>
                        <ul class="list">
                            <li class="list-item">
                                <span class="item-label">性别：</span>
                                <span class="item-value">{{ matchData.partner_info.sex === 'M' ? '男' :
                                    '女' }}</span>
                            </li>
                            <li class="list-item">
                                <span class="item-label">学校：</span>
                                <span class="item-value">{{ matchData.partner_info.school }}</span>
                            </li>
                            <li class="list-item">
                                <span class="item-label">年级：</span>
                                <span class="item-value">{{
                                    getGradeText(matchData.partner_info.grade) }}</span>
                            </li>
                            <li class="list-item">
                                <span class="item-label">MBTI：</span>
                                <span class="item-value">{{
                                    getMBTIType(matchData.partner_info.mbti) }}</span>
                            </li>
                            <li class="list-item">
                                <span class="item-label">位置：</span>
                                <span class="item-value">{{
                                    getLocationText(matchData.partner_info.location) }}</span>
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="partner-message">
                    <span class="hint-text">{{ matchData.partner_info.sex === 'M' ? '他' : '她' }}说:</span>
                    <span class="message-text">
                        {{ matchData.partner_info.message_to_partner }}
                    </span>
                </div>
            </section>

            <section class="mentor-info">
                <div class="mentor-info-item">
                    <div class="mentor-detail">
                        <h2>你的Mentor</h2>
                        <ul class="list">
                            <li class="list-item">
                                <span class="item-label">姓名：</span>
                                <span class="item-value">{{ matchData.mentor_info.name }}</span>
                            </li>
                            <li class="list-item">
                                <span class="item-label">微信号：</span>
                                <span class="item-value">{{ matchData.mentor_info.wxid }}</span>
                            </li>
                            <li class="list-item">
                                <span class="item-value">请添加并备注你的姓名与组号:「{{ matchData.match_info.id }}」</span>
                            </li>
                        </ul>
                    </div>
                    <div class="mentor-qr">
                        <img :src="getImageUrl(matchData.mentor_info.qrcode)" alt="">
                        <p class="mentor-qr-hint">长按可识别二维码</p>
                    </div>
                </div>
            </section>

            <section class="match-info">
                <div class="match-info-item">
                    <h2>CP组 #{{ matchData.match_info.id }} 状态</h2>
                    <div v-if="matchData.match_info.discarded" class="discarded">
                        <div class="discarded-title">本轮匹配已废弃</div>
                        <p class="discarded-reason">
                            {{ matchData.match_info.discard_reason || '匹配已被取消，请关注后续通知。' }} <br>
                            <template v-if="round === 1">
                                双方将进入第二轮匹配
                            </template>
                            <template v-else>
                                活动结束, 退款将在活动结束后统一处理。
                            </template>
                        </p>
                    </div>
                    <div v-else class="not-discarded">
                        <ul class="status-list">
                            <li class="status-item">
                                <span class="status-label">你的状态</span>
                                <span class="status-value" :class="getStatusClass(matchData.match_info.user_status)">
                                    {{ getStatusText(matchData.match_info.user_status) || '待确认' }}
                                </span>
                            </li>
                            <li class="status-item">
                                <span class="status-label">对方状态</span>
                                <span class="status-value" :class="getStatusClass(matchData.match_info.partner_status)">
                                    {{ getStatusText(matchData.match_info.partner_status) || '待确认' }}
                                </span>
                            </li>
                        </ul>

                        <div v-if="round === 1 && matchData.match_info.user_status === 'P'" class="status-actions">
                            <p class="status-hint">
                                请在截止前选择接受或拒绝。
                            </p>
                            <div class="button-row">
                                <button class="btn primary" @click="updateStatus('A')">
                                    接受匹配
                                </button>
                                <button class="btn danger" @click="updateStatus('R')">
                                    拒绝匹配
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <div class="button-group">
                <button class="btn primary" @click="navigateTo('/')">返回首页</button>
            </div>
        </template>

    </div>
</template>

<script setup lang="ts">
useHead({
    title: "一周CP 2026 | 匹配结果",
});

const { get, post } = useRequest();
const matchData = ref<any>(null);
const no_match = ref(false);
const error = ref<string | null>(null);
const isUserAccepted = computed(() => matchData.value?.match_info?.user_status === 'A');

const round = computed(() => {
    if (userState.value === UserStates.FIRST_MATCH_RESULT_RELEASE || userState.value === UserStates.FIRST_MATCH_CONFIRM_END) {
        return 1;
    }
    else {
        return 2;
    }
});

const getGradeText = (grade: string | null) => {
    if (!grade) return '';
    const gradeMap: Record<string, string> = {
        'UG1': '大一',
        'UG2': '大二',
        'UG3': '大三',
        'UG4': '大四',
        'UG5': '大五',
        'MS': '硕士',
        'PHD': '博士',
        'PROF': '教授'
    };
    return gradeMap[grade] || grade;
};

const getMBTIType = (mbti: { ei: number; sn: number; tf: number; jp: number } | null) => {
    if (!mbti) return '';
    const ei = mbti.ei >= 50 ? 'E' : 'I';
    const sn = mbti.sn >= 50 ? 'N' : 'S';
    const tf = mbti.tf >= 50 ? 'T' : 'F';
    const jp = mbti.jp >= 50 ? 'J' : 'P';
    return `${ei}${sn}${tf}${jp}`;
};

const getLocationText = (location: string | null) => {
    if (!location) return '';
    const locationMap: Record<string, string> = {
        'HK': '香港',
        'SZ': '深圳',
        'GD': '广东省',
        'TW': '台湾',
        'CN': '中国',
        'JP_KR': '日韩',
        'ASIA': '亚洲',
        'UK': '英国',
        'EU': '欧洲',
        'US': '美国',
        'CA': '加拿大',
        'NA': '北美洲',
        'OTHER': '其他',
    };
    return locationMap[location] || location;
};

const getStatusText = (status: string | null) => {
    if (!status) return '';
    const statusMap: Record<string, string> = {
        'P': '待确认',
        'A': '已接受',
        'R': '已拒绝'
    };
    return statusMap[status] || status;
};

const getStatusClass = (status: string | null | undefined) => {
    return {
        'status-pending': status === 'P',
        'status-accepted': status === 'A',
        'status-rejected': status === 'R'
    };
};

const loadMatchResult = async () => {
    error.value = null;
    no_match.value = false;

    try {
        const res = await get("match-result/");
        if (res.ok) {
            const data = await res.json();
            if (!data?.data) {
                matchData.value = null;
                no_match.value = true;
                return;
            }
            matchData.value = data.data;
        }
        else if (res.status === 404) {
            matchData.value = null;
            no_match.value = true;
        }
        else {
            const errorData = await res.json();
            throw new Error(errorData.detail || res.statusText);
        }
    } catch (err: any) {
        error.value = err.message || '加载匹配结果失败';
        console.error(err);
    }
};

const updateStatus = async (status: 'A' | 'R') => {
    const confirmed = window.confirm(
        status === 'A'
            ? '确认接受匹配？提交后无法修改。'
            : '确认拒绝匹配？提交后无法修改。'
    );
    if (!confirmed) return;

    try {
        const res = await post("match-result/", { status });
        if (res.ok) {
            const data = await res.json();
            // Reload match result to get updated status
            await loadMatchResult();
            alert(status === 'A' ? '已接受匹配' : '已拒绝匹配');
        } else {
            const errorData = await res.json();
            throw new Error(errorData.detail || res.statusText);
        }
    } catch (err: any) {
        alert(err.message || '更新状态失败');
        console.error(err);
    }
};

onMounted(() => {
    loadMatchResult();
});
</script>

<style scoped>
h1 {
    margin-bottom: 1rem;
}

h2 {
    font-size: var(--fs-600);
    font-weight: bold;
    margin-block: 0.25rem;
    text-align: center;
}

section {
    background: hsla(356, 100%, 98%, 0.3);

    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    margin-bottom: 2rem;
}

.partner-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 0.225rem;
}

.partner-info-item,
.mentor-info-item {
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.5rem;
}

.polaroid-frame {
    position: relative;
    width: 55%;
    aspect-ratio: 1/1.15;
    background: white;
    padding: 3.5%;
    box-shadow: 1px 1px 10px 0 rgba(0, 0, 0, 0.2);
}

.partner-name {
    position: absolute;
    min-width: 50%;
    text-align: center;
    background: var(--clr-accent);
    padding: 0.125rem 0.625rem 0.125rem 0.25rem;
    border-radius: 0 0.5rem 0 0;
    top: 10%;
    left: 19%;
    transform: translate(-50%, -50%) rotate(-30deg);
    z-index: 2;
}

.polaroid-frame-img {
    position: relative;
    overflow: hidden;
    width: 100%;
    aspect-ratio: 1/1;
}

.polaroid-frame img {
    object-fit: cover;
    background: var(--clr-text--muted);
}

.blur-img-overlay {
    background: rgba(0, 0, 0, 0.6);
    position: absolute;
    inset: 0;
    z-index: 1;
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: var(--fs-200);
    color: var(--clr-text--muted);
}

.partner-detail {
    flex: 1;
}

.list {
    display: flex;
    flex-direction: column;
    padding-inline: 0.5rem;
    gap: 0.5rem;
}

.item-label {
    font-size: var(--fs-300);
}

.item-value {
    font-size: var(--fs-300);
    color: var(--clr-text);
}

.partner-message {
    width: calc(100% - 1rem);
    margin-inline: auto;
    padding: 1rem 1rem;
    background: var(--clr-background);
    font-size: var(--fs-400);
    min-height: calc(3lh + 2rem);
    line-height: 1.75;


}

.hint-text {
    font-size: var(--fs-400);
    color: var(--clr-text--muted);
    margin-right: 1ch;
}

.message-text {
    font-size: var(--fs-400);
    color: var(--clr-text);
    font-family: var(--ff-accent);
    text-decoration: underline;
    text-underline-offset: 0.25rem;

}

.mentor-qr {
    width: 50%;
}

.mentor-qr img {
    user-select: all;

}

.mentor-qr-hint {
    width: 100%;
    font-size: var(--fs-200);
    color: var(--clr-text--muted);
    text-align: center;
}

.match-info-item {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 0.75rem 1rem 1rem;
}

.status-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    padding: 0;
    margin: 0;
    list-style: none;
}

.status-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    background: rgba(255, 255, 255, 0.55);
    border-radius: 0.75rem;
    padding: 0.75rem 1rem;
}

.status-label {
    font-size: var(--fs-300);
    color: var(--clr-text--muted);
}

.status-value {
    font-size: var(--fs-300);
    font-weight: 800;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.6);
}

.status-pending {
    color: #b87400;
    background: rgba(255, 216, 160, 0.35);
}

.status-accepted {
    color: var(--clr-success);
    background: rgba(120, 200, 120, 0.2);
}

.status-rejected {
    color: red;
    background: rgba(255, 128, 128, 0.2);
}

.status-actions {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.status-hint {
    margin-top: 1rem;
    font-size: var(--fs-300);
    color: var(--clr-text--muted);
    text-align: center;
}

.status-note {
    text-align: center;
    font-size: var(--fs-300);
    color: var(--clr-text--muted);
}

.button-row {
    display: flex;
    gap: 0.75rem;
}

.button-row .btn {
    flex: 1;
}

.discarded {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
    padding: 0.75rem 0.5rem;
}

.discarded-title {
    font-size: var(--fs-500);
    font-weight: 700;
    color: var(--clr-primary-dark);
}

.discarded-reason {
    font-size: var(--fs-300);
    color: var(--clr-text--muted);
}

.button-group {
    margin-block: 3rem 5rem;
}
</style>