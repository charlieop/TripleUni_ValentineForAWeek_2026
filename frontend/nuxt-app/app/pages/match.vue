<template>
    <div class="page-wrapper">
        <h1>匹配详情</h1>

        <div v-if="loading" class="loading">
            <p>加载中...</p>
        </div>

        <div v-else-if="error" class="error">
            <p>{{ error }}</p>
            <div class="button-group">
                <button @click="loadMatchData" class="btn primary">重试</button>
                <button @click="navigateTo('/')" class="btn secondary">
                    返回首页
                </button>
            </div>
        </div>

        <div v-else-if="matchData" class="match-content">
            <!-- Match Name Section -->
            <section class="info-section match-name-section">
                <div class="match-name-card">
                    <div class="match-name-display" v-if="!isEditingName">
                        <h2 class="match-name">{{ matchData.match_info.name }}</h2>
                        <p class="match-id">组号 #{{ matchData.match_info.id }}</p>
                        <button @click="startEditingName" class="btn-edit-name">点击更改组名</button>
                    </div>
                    <div class="match-name-edit" v-else>
                        <input v-model="newMatchName" type="text" class="name-input" :maxlength="30" placeholder="输入组名"
                            @keyup.enter="saveMatchName" @keyup.esc="cancelEditingName" />
                        <div class="edit-actions">
                            <button @click="saveMatchName" class="btn primary" :disabled="savingName">
                                {{ savingName ? '保存中...' : '保存' }}
                            </button>
                            <button @click="cancelEditingName" class="btn secondary" :disabled="savingName">
                                取消
                            </button>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Score Section - Emphasized -->
            <section class="info-section score-section">
                <div class="score-card">
                    <h2 class="score-label">总积分</h2>
                    <div class="score-value">{{ matchData.match_info.total_score }}</div>
                    <p class="score-description">完成每日任务可获得积分</p>
                </div>
            </section>

            <!-- CP Group Section -->
            <section class="info-section cp-section">
                <h2>我的CP组</h2>
                <div class="cp-group">
                    <div class="cp-member user-member">
                        <div class="cp-avatar">
                            <img v-if="matchData.user_info.head_image"
                                :src="getImageUrl(matchData.user_info.head_image)" :alt="matchData.user_info.name" />
                            <div v-else class="avatar-placeholder">{{ matchData.user_info.name[0] }}</div>
                        </div>
                        <p class="cp-name">{{ matchData.user_info.name }}</p>
                        <p class="cp-label">你</p>
                    </div>

                    <div class="cp-connector">{{ getConnectorEmoji(matchData.match_info.total_score) }}</div>

                    <div class="cp-member partner-member">
                        <div class="cp-avatar">
                            <img v-if="matchData.partner_info.head_image"
                                :src="getImageUrl(matchData.partner_info.head_image)"
                                :alt="matchData.partner_info.name" />
                            <div v-else class="avatar-placeholder">{{ matchData.partner_info.name[0] }}</div>
                        </div>
                        <p class="cp-name">{{ matchData.partner_info.name }}</p>
                        <p class="cp-label">CP</p>
                        <p class="cp-wxid">微信号: {{ matchData.partner_info.wxid }}</p>
                    </div>
                </div>
            </section>

            <!-- Daily Missions Section -->
            <section class="info-section missions-section">
                <h2>每日任务</h2>
                <div class="missions-grid">
                    <div v-for="day in 7" :key="day" class="mission-card"
                        :class="{ 'mission-completed': matchData.match_info.basic_complete && matchData.match_info.basic_complete[day - 1] }"
                        @click="navigateTo(`/tasks/${day}`)">
                        <div class="mission-day">Day {{ day }}</div>
                        <div class="mission-status">
                            <span
                                v-if="matchData.match_info.basic_complete && matchData.match_info.basic_complete[day - 1]"
                                class="status-icon completed">✓</span>
                            <span v-else class="status-icon pending">○</span>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Mentor Info Button -->
            <div class="button-group">
                <button @click="showMentorModal = true" class="btn secondary">
                    查看Mentor信息
                </button>
                <button @click="navigateTo('/')" class="btn secondary">
                    返回首页
                </button>
            </div>
        </div>

        <!-- Mentor Modal -->
        <Transition name="modal">
            <div v-if="showMentorModal" class="modal-overlay" @click="showMentorModal = false">
                <div class="modal-content" @click.stop>
                    <div class="modal-header">
                        <h2>Mentor信息</h2>
                        <button @click="showMentorModal = false" class="modal-close">×</button>
                    </div>
                    <div class="modal-body" v-if="matchData">
                        <div class="mentor-modal-info">
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
                    </div>
                    <div class="modal-footer">
                        <button @click="showMentorModal = false" class="btn primary">关闭</button>
                    </div>
                </div>
            </div>
        </Transition>
    </div>
</template>

<script setup lang="ts">
import { API_HOST } from "@/app/composables/useConfigs";

useHead({
    title: "一周CP 2026 | 匹配详情",
});

const { get, post } = useRequest();
const matchData = ref<any>(null);
const loading = ref(true);
const error = ref<string | null>(null);
const showMentorModal = ref(false);
const isEditingName = ref(false);
const newMatchName = ref("");
const savingName = ref(false);

const getImageUrl = (path: string | null) => {
    if (!path) return '';
    return `${API_HOST}/media/${path}`;
};

const getConnectorEmoji = (score: number): string => {
    // Emoji progression representing relationship stages based on score
    if (score === 0) {
        return '👋'; // Just meeting - waving
    } else if (score <= 50) {
        return '🤝'; // Getting acquainted - handshake
    } else if (score <= 100) {
        return '👥'; // Getting to know each other - people together
    } else if (score <= 200) {
        return '💬'; // Talking and connecting - speech bubbles
    } else if (score <= 300) {
        return '💕'; // Growing closer - two hearts
    } else if (score <= 400) {
        return '💖'; // Falling in love - sparkling heart
    } else if (score <= 500) {
        return '💑'; // In love - couple with heart
    } else {
        return '💗'; // Deeply in love - growing heart
    }
};

const loadMatchData = async () => {
    loading.value = true;
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
    } finally {
        loading.value = false;
    }
};

const startEditingName = () => {
    if (matchData.value) {
        newMatchName.value = matchData.value.match_info.name;
        isEditingName.value = true;
    }
};

const cancelEditingName = () => {
    isEditingName.value = false;
    if (matchData.value) {
        newMatchName.value = matchData.value.match_info.name;
    }
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

    savingName.value = true;
    try {
        const res = await post("match/", { name: newMatchName.value.trim() });
        if (res.ok) {
            const data = await res.json();
            if (matchData.value) {
                matchData.value.match_info.name = data.data.name;
            }
            isEditingName.value = false;
            alert('组名已更新');
        } else {
            const errorData = await res.json();
            throw new Error(errorData.detail || res.statusText);
        }
    } catch (err: any) {
        alert(err.message || '更新组名失败');
        console.error(err);
    } finally {
        savingName.value = false;
    }
};

onMounted(() => {
    loadMatchData();
});
</script>

<style scoped>
.page-wrapper {
    padding: 1.5rem;
    max-width: 100%;
    margin: 0 auto;
    padding-bottom: 3rem;
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

/* Match Name Section */
.match-name-card {
    text-align: center;
}

.match-name-display {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.match-name {
    font-size: var(--fs-600);
    color: var(--clr-text);
    margin: 0;
    word-break: break-word;
}

.match-id {
    font-size: var(--fs-300);
    color: var(--clr-text--muted);
    margin: 0;
}

.btn-edit-name {
    margin-top: 0.5rem;
    padding: 0.5rem 1rem;
    background: transparent;
    border: 1px solid var(--clr-primary);
    color: var(--clr-primary);
    border-radius: 0.5rem;
    font-size: var(--fs-300);
    cursor: pointer;
    transition: var(--transition);
}

.btn-edit-name:hover {
    background: var(--clr-primary-light);
}

.match-name-edit {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.name-input {
    padding: 0.75rem;
    border: 2px solid var(--clr-primary);
    border-radius: 0.5rem;
    font-size: var(--fs-400);
    background: var(--clr-background);
    color: var(--clr-text);
    text-align: center;
}

.name-input:focus {
    outline: none;
    border-color: var(--clr-primary-dark);
}

.edit-actions {
    display: flex;
    gap: 0.75rem;
}

.edit-actions .btn {
    flex: 1;
}

/* Score Section - Emphasized */
.score-section {
    background: linear-gradient(135deg, var(--clr-primary-light), var(--clr-secondary-light));
    border: 2px solid var(--clr-primary);
}

.score-card {
    text-align: center;
}

.score-label {
    font-size: var(--fs-500);
    color: var(--clr-text);
    margin-bottom: 1rem;
}

.score-value {
    font-size: 4rem;
    font-weight: 700;
    color: var(--clr-primary-dark);
    line-height: 1;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.score-description {
    font-size: var(--fs-300);
    color: var(--clr-text--muted);
    margin: 0;
}

/* CP Group Section */
.cp-group {
    display: flex;
    align-items: center;
    justify-content: space-around;
    gap: 1rem;
    padding: 1rem 0;
}

.cp-member {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
}

.cp-avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid var(--clr-primary);
    background: var(--clr-background--muted);
}

.cp-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    color: var(--clr-primary);
    font-weight: 600;
}

.cp-name {
    font-size: var(--fs-400);
    color: var(--clr-text);
    font-weight: 600;
    margin: 0;
    word-break: break-word;
    text-align: center;
}

.cp-label {
    font-size: var(--fs-300);
    color: var(--clr-primary);
    font-weight: 600;
    margin: 0;
}

.cp-wxid {
    font-size: var(--fs-300);
    color: var(--clr-text--muted);
    margin: 0;
    word-break: break-all;
    text-align: center;
}

.cp-connector {
    font-size: 2rem;
    flex-shrink: 0;
    animation: pulse 2s ease-in-out infinite;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

@keyframes pulse {

    0%,
    100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.1);
    }
}

/* Missions Section */
.missions-grid {
    margin-top: 1rem;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 1rem;
}

.mission-card {
    background: var(--clr-background);
    border: 2px solid var(--clr-text--muted);
    border-radius: 0.75rem;
    padding: 1.25rem 1rem;
    text-align: center;
    cursor: pointer;
    transition: var(--transition);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    min-height: 100px;
    justify-content: center;
}

.mission-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border-color: var(--clr-primary);
}

.mission-card.mission-completed {
    background: linear-gradient(135deg, var(--clr-primary-light), var(--clr-secondary-light));
    border-color: var(--clr-primary);
    border-width: 2px;
}

.mission-day {
    font-size: var(--fs-500);
    font-weight: 600;
    color: var(--clr-text);
}

.mission-status {
    display: flex;
    align-items: center;
    justify-content: center;
}

.status-icon {
    font-size: 1.5rem;
    font-weight: bold;
}

.status-icon.completed {
    color: var(--clr-primary-dark);
}

.status-icon.pending {
    color: var(--clr-text--muted);
}

/* Button Group */
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

.btn.secondary {
    background: var(--clr-secondary);
    color: var(--clr-text);
}

.btn.secondary:hover {
    background: var(--clr-secondary-dark);
}

/* Modal Styles */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 1rem;
    backdrop-filter: blur(4px);
}

.modal-content {
    background: var(--clr-background);
    border-radius: 1rem;
    max-width: 400px;
    width: 100%;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid var(--clr-background--muted);
}

.modal-header h2 {
    margin: 0;
    font-size: var(--fs-600);
    color: var(--clr-primary);
}

.modal-close {
    background: none;
    border: none;
    font-size: 2rem;
    color: var(--clr-text--muted);
    cursor: pointer;
    line-height: 1;
    padding: 0;
    width: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: var(--transition);
}

.modal-close:hover {
    background: var(--clr-background--muted);
    color: var(--clr-text);
}

.modal-body {
    padding: 1.5rem;
}

.mentor-modal-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
}

.mentor-qr {
    width: 200px;
    height: 200px;
    border-radius: 0.5rem;
    overflow: hidden;
    border: 2px solid var(--clr-secondary);
    background: white;
}

.mentor-qr img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.mentor-details {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.mentor-details .info-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    background: var(--clr-background--muted);
    border-radius: 0.5rem;
}

.mentor-details .label {
    font-size: var(--fs-400);
    color: var(--clr-text--muted);
}

.mentor-details .value {
    font-size: var(--fs-400);
    color: var(--clr-text);
    font-weight: 600;
}

.modal-footer {
    padding: 1.5rem;
    border-top: 1px solid var(--clr-background--muted);
}

.modal-footer .btn {
    width: 100%;
}

/* Modal Transitions */
.modal-enter-active,
.modal-leave-active {
    transition: opacity 0.3s ease;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
    transition: transform 0.3s ease, opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
    transform: scale(0.9);
    opacity: 0;
}
</style>
