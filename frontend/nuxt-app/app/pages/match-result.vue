<template>
    <div class="match-result-wrapper">
        <h1>匹配结果</h1>

        <div v-if="loading" class="loading">
            <p>加载中...</p>
        </div>

        <div v-else-if="error" class="error">
            <p>{{ error }}</p>
            <div class="button-group">

                <button @click="loadMatchResult" class="btn primary">重试</button>
                <button @click="navigateTo('/')" class="btn secondary">
                    返回首页
                </button>
            </div>
        </div>

        <div v-else-if="matchData" class="match-content">
            <!-- Partner Info Section -->
            <section class="info-section partner-section">
                <h2>匹配对象信息</h2>
                <div class="partner-card">
                    <div v-if="matchData.partner_info.head_image" class="avatar">
                        <img :src="getImageUrl(matchData.partner_info.head_image)"
                            :alt="matchData.partner_info.nickname || '头像'" />
                    </div>
                    <div class="partner-details">
                        <h3>{{ matchData.partner_info.nickname || '未设置昵称' }}</h3>
                        <div class="info-grid">
                            <div class="info-item">
                                <span class="label">学校:</span>
                                <span class="value">{{ matchData.partner_info.school }}</span>
                            </div>
                            <div class="info-item">
                                <span class="label">年级:</span>
                                <span class="value">{{ getGradeText(matchData.partner_info.grade) }}</span>
                            </div>
                            <div class="info-item">
                                <span class="label">性别:</span>
                                <span class="value">{{ matchData.partner_info.sex === 'M' ? '男' : '女' }}</span>
                            </div>
                            <div class="info-item">
                                <span class="label">MBTI:</span>
                                <span class="value">{{ getMBTIType(matchData.partner_info.mbti) }}</span>
                            </div>
                        </div>
                        <div v-if="matchData.partner_info.message_to_partner" class="message">
                            <p class="message-label">留言:</p>
                            <p class="message-content">{{ matchData.partner_info.message_to_partner }}</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Mentor Info Section -->
            <section class="info-section mentor-section">
                <h2>Mentor信息</h2>
                <div class="mentor-card">
                    <div v-if="matchData.mentor_info.qrcode" class="mentor-qr">
                        <img :src="getImageUrl(matchData.mentor_info.qrcode)" alt="Mentor二维码" />
                    </div>
                    <div class="mentor-details">
                        <div class="info-item">
                            <span class="label">姓名:</span>
                            <span class="value">{{ matchData.mentor_info.name }}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">微信号:</span>
                            <span class="value">{{ matchData.mentor_info.wxid }}</span>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Match Info Section -->
            <section class="info-section match-section">
                <h2>匹配状态</h2>
                <div class="match-status-card">
                    <div class="info-item">
                        <span class="label">匹配ID:</span>
                        <span class="value">#{{ matchData.match_info.id }}</span>
                    </div>
                    <div class="info-item">
                        <span class="label">你的状态:</span>
                        <span class="value status-badge" :class="getStatusClass(matchData.match_info.user_status)">
                            {{ getStatusText(matchData.match_info.user_status) }}
                        </span>
                    </div>
                    <div class="info-item">
                        <span class="label">对方状态:</span>
                        <span class="value status-badge" :class="getStatusClass(matchData.match_info.partner_status)">
                            {{ getStatusText(matchData.match_info.partner_status) }}
                        </span>
                    </div>
                    <div v-if="matchData.match_info.discarded" class="discarded-warning">
                        <p class="warning-text">此匹配已被废弃</p>
                        <p v-if="matchData.match_info.discard_reason" class="discard-reason">
                            {{ matchData.match_info.discard_reason }}
                        </p>
                    </div>
                </div>
            </section>

            <!-- Action Buttons -->
            <div v-if="matchData.match_info.user_status === 'P' && !matchData.match_info.discarded"
                class="action-buttons">
                <button @click="updateStatus('A')" class="btn primary accept-btn" :disabled="submitting">
                    {{ submitting ? '提交中...' : '接受匹配' }}
                </button>
                <button @click="updateStatus('R')" class="btn danger reject-btn" :disabled="submitting">
                    {{ submitting ? '提交中...' : '拒绝匹配' }}
                </button>
            </div>

            <div class="button-group">
                <button @click="navigateTo('/')" class="btn secondary">返回首页</button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { API_HOST } from "@/app/composables/useConfigs";

useHead({
    title: "一周CP 2026 | 匹配结果",
});

const { get, post } = useRequest();
const matchData = ref<any>(null);
const loading = ref(true);
const error = ref<string | null>(null);
const submitting = ref(false);

const getImageUrl = (path: string | null) => {
    if (!path) return '';
    return `${API_HOST}/media/${path}`;
};

const getGradeText = (grade: string) => {
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

const getMBTIType = (mbti: { ei: number; sn: number; tf: number; jp: number }) => {
    const ei = mbti.ei >= 50 ? 'E' : 'I';
    const sn = mbti.sn >= 50 ? 'N' : 'S';
    const tf = mbti.tf >= 50 ? 'T' : 'F';
    const jp = mbti.jp >= 50 ? 'J' : 'P';
    return `${ei}${sn}${tf}${jp}`;
};

const getStatusText = (status: string) => {
    const statusMap: Record<string, string> = {
        'P': '待确认',
        'A': '已接受',
        'R': '已拒绝'
    };
    return statusMap[status] || status;
};

const getStatusClass = (status: string) => {
    return {
        'status-pending': status === 'P',
        'status-accepted': status === 'A',
        'status-rejected': status === 'R'
    };
};

const loadMatchResult = async () => {
    loading.value = true;
    error.value = null;

    try {
        const res = await get("match-result/");
        if (res.ok) {
            const data = await res.json();
            matchData.value = data.data;
        } else {
            const errorData = await res.json();
            throw new Error(errorData.detail || res.statusText);
        }
    } catch (err: any) {
        error.value = err.message || '加载匹配结果失败';
        console.error(err);
    } finally {
        loading.value = false;
    }
};

const updateStatus = async (status: 'A' | 'R') => {
    if (submitting.value) return;

    submitting.value = true;
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
    } finally {
        submitting.value = false;
    }
};

onMounted(() => {
    loadMatchResult();
});
</script>

<style scoped>
.match-result-wrapper {
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

h2 {
    font-size: var(--fs-600);
    color: var(--clr-primary-dark);
    margin-bottom: 1rem;
}

.loading,
.error {
    text-align: center;
    padding: 2rem;
}

.error {
    color: var(--clr-danger);
}

.info-section {
    margin-bottom: 2rem;
    padding: 1.5rem;
    background: var(--clr-background--muted);
    border-radius: 0.5rem;
}

.partner-card,
.mentor-card,
.match-status-card {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.avatar {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    overflow: hidden;
    margin: 0 auto;
    border: 3px solid var(--clr-primary);
}

.avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.partner-details h3 {
    font-size: var(--fs-500);
    color: var(--clr-text);
    margin-bottom: 1rem;
    text-align: center;
}

.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    margin-bottom: 1rem;
}

.info-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.info-item .label {
    font-size: var(--fs-300);
    color: var(--clr-text--muted);
}

.info-item .value {
    font-size: var(--fs-400);
    color: var(--clr-text);
    font-weight: 500;
}

.message {
    margin-top: 1rem;
    padding: 1rem;
    background: var(--clr-background);
    border-radius: 0.5rem;
    border-left: 3px solid var(--clr-primary);
}

.message-label {
    font-size: var(--fs-300);
    color: var(--clr-text--muted);
    margin-bottom: 0.5rem;
}

.message-content {
    font-size: var(--fs-400);
    color: var(--clr-text);
    line-height: 1.6;
}

.mentor-qr {
    width: 200px;
    height: 200px;
    margin: 0 auto;
    border-radius: 0.5rem;
    overflow: hidden;
    border: 2px solid var(--clr-secondary);
}

.mentor-qr img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.mentor-details {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.status-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: var(--fs-300);
    font-weight: 600;
}

.status-badge.status-pending {
    background: var(--clr-accent-light);
    color: var(--clr-text);
}

.status-badge.status-accepted {
    background: var(--clr-success);
    color: white;
}

.status-badge.status-rejected {
    background: var(--clr-danger);
    color: white;
}

.discarded-warning {
    margin-top: 1rem;
    padding: 1rem;
    background: var(--clr-failed);
    border-radius: 0.5rem;
    border-left: 3px solid var(--clr-danger);
}

.warning-text {
    color: var(--clr-danger);
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.discard-reason {
    color: var(--clr-text);
    font-size: var(--fs-400);
}

.action-buttons {
    display: flex;
    gap: 1rem;
    margin: 2rem 0;
}

.btn {
    flex: 1;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.5rem;
    font-size: var(--fs-400);
    font-weight: 600;
    cursor: pointer;
    transition: var(--transition);
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn.primary {
    background: var(--clr-primary);
    color: var(--clr-text);
}

.btn.primary:hover:not(:disabled) {
    background: var(--clr-primary-dark);
}

.btn.danger {
    background: var(--clr-danger);
    color: white;
}

.btn.danger:hover:not(:disabled) {
    background: hsl(0, 87%, 40%);
}

.btn.secondary {
    background: var(--clr-secondary);
    color: var(--clr-text);
}

.btn.secondary:hover {
    background: var(--clr-secondary-dark);
}

.button-group {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 2rem;
}
</style>