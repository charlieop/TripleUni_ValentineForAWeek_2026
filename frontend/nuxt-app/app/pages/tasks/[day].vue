<template>
    <div class="page-wrapper flower-background">
        <div class="title-wrapper">
            <h1 class="page-title">Day {{ day }} 任务</h1>
            <LogoSm />
        </div>

        <template v-if="error">
            <div class="state-card error">
                <div class="state-icon">❌</div>
                <p class="state-title">加载失败</p>
                <p class="state-message">{{ error }}</p>
            </div>
            <div class="button-group">
                <button @click="loadTaskData" class="btn primary">重试</button>
                <button @click="navigateTo('/match')" class="btn">返回</button>
            </div>
        </template>

        <div v-else-if="taskData" class="task-content">
            <div v-if="taskData.due" class="due-banner">
                <span class="due-banner-title">截止提醒</span>
                <span class="due-banner-text">本日任务已过截止时间，当前为只读状态。若对评分有异议，请联系你的Mentor。</span>
            </div>

            <!-- Scores Section -->
            <section class="scores-section" v-if="taskData.due">
                <h2 class="section-title">得分情况</h2>
                <div class="score-card">
                    <div class="score-grid">
                        <div class="score-row">
                            <span class="score-label">
                                基础得分
                                <span class="score-badge"
                                    :class="{ completed: isBasicCompleted, pending: !isBasicCompleted }">
                                    {{ isBasicCompleted ? '已完成' : '未完成' }}
                                </span>
                            </span>
                            <span class="score-value">{{ taskData.basic_score ?? 0 }}</span>
                        </div>
                        <div class="score-row">
                            <span class="score-label">加分任务得分</span>
                            <span class="score-value">{{ taskData.bonus_score ?? 0 }}</span>
                        </div>
                        <div class="score-row">
                            <span class="score-label">日常得分</span>
                            <span class="score-value">{{ taskData.daily_score ?? 0 }}</span>
                        </div>
                        <p class="score-notes">
                            评分最多需要12小时更新, 若在截止后12小时后仍未更新, 请联系你的Mentor.
                        </p>
                    </div>
                </div>
            </section>

            <!-- Mission Description Section -->
            <section class="mission-section">
                <h2 class="section-title">任务描述</h2>
                <div class="mission-card">
                    <div v-if="missionError" class="mission-placeholder">
                        <p class="placeholder-text">{{ missionError }}</p>
                    </div>
                    <div v-else-if="missionData" class="mission-body">
                        <h3 class="mission-title">{{ missionData.title }}</h3>
                        <p class="mission-content">{{ missionData.content }}</p>
                        <button v-if="missionData.link" class="btn danger mission-link-btn" @click="goToMissionLink">
                            查看任务
                        </button>
                    </div>
                    <div v-else class="mission-placeholder">
                        <p class="placeholder-text">加载中...</p>
                    </div>
                </div>
            </section>

            <!-- Submission Section -->
            <section class="submission-section">
                <h2 class="section-title">提交内容</h2>

                <!-- Images Section -->
                <div class="images-section">
                    <label class="field-label">图片</label>
                    <div class="images-grid">
                        <div v-for="(image, index) in taskData.images" :key="image.id" class="polaroid-frame">
                            <img :src="getImageUrl(image.image_url)" :alt="`Image ${image.id}`"
                                @click="openImageModal(typeof index === 'number' ? index : parseInt(index))"
                                class="polaroid-image" loading="lazy" />
                            <button v-if="!taskData.due" @click.stop="removeImage(image.id)"
                                class="hover-button remove-image-btn">
                                <IconCross size="1.5rem" color="#EEEEEE" />
                            </button>
                        </div>
                        <div v-if="taskData.images.length < 25 && !taskData.due" class="image-upload-card"
                            @click="triggerFileInput">
                            <span class="upload-icon">+</span>
                            <span class="upload-text">添加图片</span>
                        </div>
                    </div>
                    <input ref="fileInput" type="file"
                        accept="image/jpeg,image/jpg,image/png,image/heic,image/heif,image/webp" multiple
                        @change="handleFileSelect" style="display: none" />
                    <p class="field-hint">最多可上传25张图片，每张图片不超过5MB. <strong>本次活动使用AI自动审核, 请不要拼接/ 遮挡/ 模糊你提交的图片.</strong></p>
                </div>
            </section>

            <!-- Text Submission Card -->
            <div class="submission-card">
                <label for="submit-text" class="field-label">文字内容</label>
                <textarea id="submit-text" v-model="editedText" class="text-input" rows="4"
                    placeholder="你可以在此对图片内容进行简要描述..." :disabled="taskData.due"></textarea>
                <button v-if="!taskData.due" @click="saveTask" class="btn primary">
                    保存
                </button>
            </div>

            <!-- Mentor Visibility Toggle -->
            <section class="visibility-section">
                <h2 class="section-title">Mentor 可见性</h2>
                <div class="visibility-card">
                    <div class="visibility-labels">
                        <p class="visibility-hint">
                            开启后，你的 Mentor 将可以查看此任务的提交。你可以随时更改此设置，即使已过截止时间。
                        </p>
                    </div>
                    <label class="switch">
                        <input type="checkbox" :checked="mentorVisible" @change="onMentorVisibilityToggle" />
                        <span class="slider round"></span>
                    </label>
                </div>
            </section>


            <section class="actions-section">
                <button @click="navigateTo('/match')" class="btn primary">
                    返回
                </button>
            </section>
        </div>

        <!-- Image Lightbox Modal -->
        <Modal v-model="showImageModal" :class="'image-lightbox-modal'" :showCloseButton="false">
            <div class="lightbox-content">

                <img v-if="taskData.images[selectedImageIndex]"
                    :src="getImageUrl(taskData.images[selectedImageIndex].image_url)"
                    :alt="`Image ${selectedImageIndex + 1}`" class="lightbox-image" loading="lazy" />
            </div>
            <Teleport to="body">
                <Transition name="modal-transition">
                    <div class="lightbox-controls">
                        <button @click="previousImage" class="hover-button lightbox-nav lightbox-nav-prev">
                            <IconArrow size="2rem" color="#FFFFFF" />
                        </button>
                        <button @click="nextImage" class="hover-button lightbox-nav lightbox-nav-next">
                            <IconArrow size="2rem" color="#FFFFFF" />
                        </button>
                        <div v-if="taskData.images.length > 1" class="lightbox-counter">
                            {{ selectedImageIndex + 1 }} / {{ taskData.images.length }}
                        </div>
                    </div>
                </Transition>
            </Teleport>

        </Modal>
    </div>
</template>

<script setup lang="ts">
useHead({
    title: `一周CP 2026 | Day ${useRoute().params.day} 任务`,
});

const route = useRoute();
const day = computed(() => parseInt(route.params.day as string));

const { get, post, del } = useRequest();

const taskData = ref<any>(null);
const error = ref<string | null>(null);
const missionData = ref<{ title: string; content: string | null; link: string | null } | null>(null);
const missionError = ref<string | null>(null);
const editedText = ref("");
const fileInput = ref<HTMLInputElement | null>(null);
const selectedImageIndex = ref<number>(0);
const showImageModal = ref(false);
const isBasicCompleted = computed(() => Boolean(taskData.value?.basic_completed));
const mentorVisible = ref(false);

const loadMissionData = async () => {
    missionError.value = null;
    missionData.value = null;

    try {
        const res = await get(`missions/${day.value}/`);
        if (res.ok) {
            const data = await res.json();
            missionData.value = data.data;
        } else {
            const errorData = await res.json();
            throw new Error(errorData.detail || res.statusText);
        }
    } catch (err: any) {
        // Keep mission failure isolated from the task page
        missionError.value = err.message || '加载任务描述失败';
        console.error(err);
    }
};

const loadTaskData = async () => {
    error.value = null;

    try {
        const res = await get(`tasks/${day.value}/`);
        if (res.ok) {
            const data = await res.json();
            taskData.value = data.data;
            editedText.value = data.data.submit_text || "";
            mentorVisible.value = Boolean(data.data.visible_to_mentor);
            // Mission is gated by release time; load it after task loads.
            await loadMissionData();
        } else {
            const errorData = await res.json();
            throw new Error(errorData.detail || res.statusText);
        }
    } catch (err: any) {
        error.value = err.message || '加载任务数据失败';
        console.error(err);
    }
};

const saveTask = async () => {
    if (!taskData.value) return;
    try {
        const res = await post(`tasks/${day.value}/`, { submit_text: editedText.value });
        if (res.ok) {
            const data = await res.json();
            if (taskData.value) {
                taskData.value.submit_text = data.data.submit_text;
            }
            alert('保存成功');
        } else {
            const errorData = await res.json();
            throw new Error(errorData.detail || res.statusText);
        }
    } catch (err: any) {
        alert(err.message || '保存失败');
        console.error(err);
    }
};

const onMentorVisibilityToggle = async (event: Event) => {
    if (!taskData.value) return;

    const target = event.target as HTMLInputElement;
    const newValue = target.checked;

    // Optimistically update UI
    mentorVisible.value = newValue;

    try {
        const res = await post(`tasks/${day.value}/visibility/`, {
            visible_to_mentor: newValue,
        });
        if (res.ok) {
            const data = await res.json();
            const serverValue = Boolean(data.data.visible_to_mentor);
            mentorVisible.value = serverValue;
            if (taskData.value) {
                taskData.value.visible_to_mentor = serverValue;
            }
            alert(serverValue ? 'Mentor 现在可以看到你的任务了' : 'Mentor 现在看不到你的任务了');
        } else {
            const errorData = await res.json();
            throw new Error(errorData.detail || res.statusText);
        }
    } catch (err: any) {
        // Revert toggle on error
        mentorVisible.value = !newValue;
        (event.target as HTMLInputElement).checked = mentorVisible.value;
        alert(err.message || '更新失败');
        console.error(err);
    }
};

const removeImage = async (imageId: string) => {
    if (!confirm('确定要删除这张图片吗？')) return;

    try {
        const res = await del(`tasks/${day.value}/imgs/${imageId}/`);
        if (res.ok) {
            if (taskData.value) {
                taskData.value.images = taskData.value.images.filter(
                    (img: any) => img.id !== imageId
                );
            }
        } else {
            const errorData = await res.json();
            throw new Error(errorData.detail || res.statusText);
        }
    } catch (err: any) {
        alert(err.message || '删除图片失败');
        console.error(err);
    }
};

const triggerFileInput = () => {
    fileInput.value?.click();
};

const handleFileSelect = async (event: Event) => {
    const target = event.target as HTMLInputElement;
    const files = target.files;
    if (!files || files.length === 0) return;

    // Check total images count
    const currentImageCount = taskData.value?.images?.length || 0;
    if (currentImageCount + files.length > 25) {
        alert('最多只能上传25张图片');
        target.value = '';
        return;
    }

    // Validate file types
    const validFiles: File[] = [];
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (!file) continue;
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/heic', 'image/heif', 'image/webp'];
        if (!validTypes.includes(file.type)) {
            alert(`图片 ${file.name} 格式不支持，已跳过`);
            continue;
        }
        validFiles.push(file);
    }

    if (validFiles.length === 0) {
        target.value = '';
        return;
    }

    const compressedFiles: File[] = [];
    for (const file of validFiles) {
        try {
            const compressedBlob = await compressImage(file);
            if (compressedBlob.size > 5 * 1024 * 1024) {
                alert(`图片 ${file.name} 压缩后仍超过5MB，已跳过`);
                continue;
            }
            const baseName = file.name.replace(/\.[^/.]+$/, '') || 'image';
            const compressedFile = new File(
                [compressedBlob],
                `${baseName}.jpg`,
                { type: compressedBlob.type || 'image/jpeg' }
            );
            compressedFiles.push(compressedFile);
        } catch (error) {
            alert(`图片 ${file.name} 压缩失败，已跳过`);
            console.error(error);
        }
    }
    if (compressedFiles.length === 0) {
        target.value = '';
        return;
    }

    // Upload images
    const formData = new FormData();
    compressedFiles.forEach(file => {
        formData.append('images', file);
    });

    try {
        const res = await post(`tasks/${day.value}/imgs/`, formData);
        if (res.ok) {
            // Reload task data to get updated images
            await loadTaskData();
        } else {
            const errorData = await res.json();
            throw new Error(errorData.detail || res.statusText);
        }
    } catch (err: any) {
        alert(err.message || '上传图片失败');
        console.error(err);
    } finally {
        target.value = '';
    }
};

const openImageModal = (index: number) => {
    selectedImageIndex.value = index;
    showImageModal.value = true;
};

const previousImage = () => {
    selectedImageIndex.value = (selectedImageIndex.value - 1 + taskData.value.images.length) % taskData.value.images.length;
};

const nextImage = () => {
    selectedImageIndex.value = (selectedImageIndex.value + 1) % taskData.value.images.length;
};

onMounted(() => {
    if (day.value < 1 || day.value > 7) {
        error.value = '无效的任务天数，必须是1-7之间的数字';
        return;
    }
    loadTaskData();
});

const goToMissionLink = async () => {
    const link = missionData.value?.link;
    if (!link) return;
    await navigateTo(link, { external: true });
};
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

h1 {
    position: relative;
    font-size: var(--fs-700);
    width: 100%;
}

section {
    padding-inline: 0.75rem;
    margin-block: 2rem;
}

.btn.primary {
    width: 100%;
}

.hover-button {
    position: absolute;
    padding: 0.25rem;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: var(--transition);
    z-index: 100;
    cursor: pointer;
    border: none;
}

.task-content {
    padding-bottom: 2rem;
}

.due-banner {
    margin: 1rem 0.75rem 0;
    padding: 0.75rem 1rem;
    border-radius: 0.75rem;
    background: rgba(255, 196, 140, 0.25);
    border: 1px solid rgba(255, 160, 120, 0.45);
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    font-size: var(--fs-300);
}

.due-banner-title {
    font-weight: 700;
    color: var(--clr-primary-dark);
}

.due-banner-text {
    color: var(--clr-text);
}

/* State Card */
.state-card {
    max-width: 520px;
    margin: 1.5rem auto;
    width: 100%;
    padding: 1.25rem 1.5rem;
    border-radius: 1rem;
    text-align: center;
    font-size: var(--fs-400);
    background: rgba(255, 255, 255, 0.75);
    box-shadow: 0 12px 26px rgba(0, 0, 0, 0.08),
        0 0 0 1px rgba(255, 255, 255, 0.6) inset;
}

.state-card.error {
    border: 1px solid rgba(255, 128, 128, 0.4);
    color: red;
}

.state-icon {
    width: 3rem;
    height: 3rem;
    border-radius: 999px;
    background: rgba(255, 196, 140, 0.2);
    display: grid;
    place-items: center;
    font-size: 1.5rem;
    font-weight: 900;
    margin: 0 auto 0.75rem;
}

.state-card.error .state-icon {
    color: red;
    background: rgba(255, 128, 128, 0.2);
}

.state-title {
    font-size: var(--fs-600);
    font-weight: 800;
}

.state-message {
    margin-top: 0.25rem;
    font-size: var(--fs-400);
}

/* Section Titles */
.section-title {
    font-size: var(--fs-600);
    color: var(--clr-primary-dark);
    font-weight: 900;
    text-align: left;
    padding-inline: 0.5rem;
    backdrop-filter: blur(1px);
    -webkit-backdrop-filter: blur(1px);
}

.score-card {
    margin-top: 0.75rem;
    background: rgba(255, 255, 255, 0.7);
    border-radius: 1rem;
    padding: 1rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.score-grid {
    display: grid;
    gap: 0.5rem;
}

.score-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px dashed rgba(0, 0, 0, 0.08);
    font-size: var(--fs-400);
}

.score-notes {
    font-size: var(--fs-200);
    color: var(--clr-text--muted);
    margin-bottom: 0;
}

.score-label {
    color: var(--clr-text);
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
}

.score-value {
    font-variant-numeric: tabular-nums;
}

.score-badge {
    font-size: var(--fs-200);
    padding: 0.15rem 0.5rem;
    border-radius: 999px;
    border: 1px solid transparent;
    font-weight: 600;
}

.score-badge.completed {
    color: #1b6b3c;
    background: rgba(140, 220, 170, 0.2);
    border-color: rgba(140, 220, 170, 0.6);
}

.score-badge.pending {
    color: #9e2b2b;
    background: rgba(255, 180, 180, 0.2);
    border-color: rgba(255, 180, 180, 0.6);
}

.mission-card {
    background: hsla(356, 100%, 98%, 0.3);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    padding: 0.5rem;
    border-radius: 1rem;
}

.mission-body {
    padding: 1rem 1rem 0.75rem;
    background: rgba(255, 255, 255, 0.55);
    border-radius: 0.75rem;
    border: 1px solid rgba(0, 0, 0, 0.06);
}

.mission-title {
    font-size: var(--fs-500);
    font-weight: 900;
    margin: 0 0 0.5rem;
}

.mission-content {
    white-space: pre-wrap;
    margin: 0 0 0.75rem;
    font-size: var(--fs-300);
}

.mission-link-btn {
    width: 100%;
}

.mission-placeholder {
    text-align: center;
    padding: 2rem 1rem;
    background: rgba(255, 255, 255, 0.55);
    border-radius: 0.75rem;
    border: 2px dashed var(--clr-text--muted);
}

.placeholder-text {
    font-size: var(--fs-400);
    color: var(--clr-text--muted);
    margin: 0;
}

.visibility-section {
    padding-inline: 0.75rem;
    margin-block: 1.5rem;
}

.visibility-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.75rem 1rem;
    border-radius: 1rem;
    background: rgba(255, 255, 255, 0.75);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
}

.visibility-labels {
    flex: 1;
}

.visibility-hint {
    font-size: var(--fs-300);
    color: var(--clr-text--muted);
    margin: 0.25rem 0 0;
}

/* Toggle switch */
.switch {
    position: relative;
    display: inline-block;
    width: 52px;
    height: 28px;
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: 0.3s;
}

.slider:before {
    position: absolute;
    content: "";
    height: 22px;
    width: 22px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: 0.3s;
}

input:checked+.slider {
    background-color: var(--clr-primary);
}

input:focus+.slider {
    box-shadow: 0 0 1px var(--clr-primary);
}

input:checked+.slider:before {
    transform: translateX(24px);
}

.slider.round {
    border-radius: 34px;
}

.slider.round:before {
    border-radius: 50%;
}


.submission-card {
    background: hsla(356, 100%, 98%, 0.3);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    padding: 1rem;
    border-radius: 1rem;
    margin-bottom: 1rem;
}

.field-label {
    display: block;
    font-size: var(--fs-400);
    font-weight: 600;
    color: var(--clr-text);
    margin-bottom: 0.5rem;
}

.text-input {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid var(--clr-text--muted);
    border-radius: 0.75rem;
    font-size: var(--fs-400);
    background: rgba(255, 255, 255, 0.9);
    color: var(--clr-text);
    font-family: inherit;
    resize: vertical;
    box-sizing: border-box;
    transition: var(--transition);
}

.text-input:focus {
    outline: none;
    border-color: var(--clr-primary);
    background: #ffffff;
}

.text-input:disabled {
    background: rgba(240, 240, 240, 0.9);
    color: var(--clr-text--muted);
    cursor: not-allowed;
    border-color: rgba(0, 0, 0, 0.1);
}

/* Images Section */
.images-section {
    background: hsla(356, 100%, 98%, 0.3);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    padding: 1rem;
    border-radius: 1rem;
}

.images-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
    gap: 1rem;
    margin-bottom: 0.5rem;
}

.polaroid-frame {
    position: relative;
    aspect-ratio: 1/1.15;
    background: white;
    padding: 4%;
    box-shadow: 1px 1px 10px 0 rgba(0, 0, 0, 0.2);
    border-radius: 0.25rem;
    cursor: pointer;
    transition: var(--transition);
}

.polaroid-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    background: var(--clr-text--muted);
}

.remove-image-btn {
    top: 0.5rem;
    right: 0.5rem;

}

.image-upload-card {
    aspect-ratio: 1/1.15;
    border: 2px dashed var(--clr-text--muted);
    border-radius: 0.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: var(--transition);
    background: rgba(255, 255, 255, 0.55);
}

.upload-icon {
    font-size: 2rem;
    color: var(--clr-text--muted);
    margin-bottom: 0.25rem;
}

.upload-text {
    font-size: var(--fs-300);
    color: var(--clr-text--muted);
}

.field-hint {
    font-size: var(--fs-300);
    margin-top: 0.5rem;
    margin-bottom: 0;
}

.image-lightbox-modal :deep(.modal-content) {
    background: transparent;
    box-shadow: none;
    padding: 0;
    max-width: 90vw;
    max-height: 90vh;
    overflow: visible;
    width: unset;
}

.image-lightbox-modal :deep(.modal-body) {
    padding: 0;
}

.lightbox-content {
    display: flex;
    align-items: center;
    justify-content: center;
}

.lightbox-image {
    max-width: 90vw;
    max-height: 85vh;
    object-fit: contain;
    border-radius: 0.5rem;
    box-shadow: 0 4px 40px rgba(0, 0, 0, 0.7);
}

.lightbox-nav {
    position: fixed;
    top: 50%;
    padding: 0.75rem;
}

.lightbox-nav-prev {
    left: 0.5rem;
    transform: translateY(-50%);
}

.lightbox-nav-next {
    right: 0.5rem;
    transform: translateY(-50%) rotate(180deg);
}

.lightbox-counter {
    position: fixed;
    bottom: 1rem;
    left: 50%;
    transform: translateX(-50%);
    color: white;
    font-size: var(--fs-400);
    background: rgba(0, 0, 0, 0.6);
    padding: 0.5rem 1rem;
    border-radius: 1rem;
    z-index: 1001;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
}
</style>
