<template>
    <div class="page-wrapper">
        <h1>Day {{ day }} 任务</h1>

        <div v-if="loading" class="loading">
            <p>加载中...</p>
        </div>

        <div v-else-if="error" class="error">
            <p>{{ error }}</p>
            <div class="button-group">
                <button @click="loadTaskData" class="btn primary">重试</button>
                <button @click="navigateTo('/match')" class="btn secondary">返回</button>
            </div>
        </div>

        <div v-else-if="taskData" class="task-content">
            <!-- Mission Description Section (Placeholder) -->
            <section class="info-section mission-description-section">
                <h2>任务描述</h2>
                <div class="mission-description-placeholder">
                    <p class="placeholder-text">任务描述功能开发中...</p>
                </div>
            </section>

            <!-- Submission Section -->
            <section class="info-section submission-section">
                <h2>提交内容</h2>

                <!-- Text Submission -->
                <div class="submission-field">
                    <label for="submit-text" class="field-label">文字内容</label>
                    <textarea id="submit-text" v-model="editedText" class="text-input" rows="6"
                        placeholder="请输入任务提交的文字内容..."></textarea>
                </div>

                <!-- Images Section -->
                <div class="submission-field">
                    <label class="field-label">图片</label>
                    <div class="images-container">
                        <div v-for="(image, index) in taskData.images" :key="image.id" class="image-item">
                            <img :src="getImageUrl(image.image_url)" :alt="`Image ${image.id}`"
                                @click="openImageModal(typeof index === 'number' ? index : parseInt(index))"
                                class="clickable-image" />
                            <button @click.stop="removeImage(image.id)" class="remove-image-btn"
                                :disabled="removingImageId === image.id">
                                {{ removingImageId === image.id ? '删除中...' : '×' }}
                            </button>
                        </div>
                        <div v-if="taskData.images.length < 20" class="image-upload-placeholder"
                            @click="triggerFileInput">
                            <span class="upload-icon">+</span>
                            <span class="upload-text">添加图片</span>
                        </div>
                    </div>
                    <input ref="fileInput" type="file"
                        accept="image/jpeg,image/jpg,image/png,image/heic,image/heif,image/webp" multiple
                        @change="handleFileSelect" style="display: none" />
                    <p class="field-hint">最多可上传20张图片，每张图片不超过5MB</p>
                </div>

                <!-- Scores Display -->
                <div class="scores-section">
                    <h3>得分情况</h3>
                    <div class="scores-grid">
                        <div class="score-item">
                            <span class="score-label">基础任务</span>
                            <span class="score-value" :class="{ 'completed': taskData.basic_completed }">
                                {{ taskData.basic_completed ? '✓ 已完成' : '未完成' }}
                            </span>
                            <span class="score-points">{{ taskData.basic_score }} 分</span>
                        </div>
                        <div class="score-item">
                            <span class="score-label">支线&Bonus</span>
                            <span class="score-value">{{ taskData.bonus_score }} 分</span>
                        </div>
                        <div class="score-item">
                            <span class="score-label">日常任务</span>
                            <span class="score-value">{{ taskData.daily_score }} 分</span>
                        </div>
                    </div>
                </div>

                <!-- Action Buttons -->
                <div class="button-group">
                    <button @click="saveTask" class="btn primary" :disabled="saving">
                        {{ saving ? '保存中...' : '保存' }}
                    </button>
                    <button @click="navigateTo('/match')" class="btn secondary" :disabled="saving">
                        返回
                    </button>
                </div>
            </section>
        </div>

        <!-- Image Lightbox Modal -->
        <Transition name="modal">
            <div v-if="selectedImageIndex !== null" class="image-modal-overlay" @click="closeImageModal">
                <div class="image-modal-content" @click.stop>
                    <button @click="closeImageModal" class="image-modal-close">×</button>
                    <button v-if="taskData && taskData.images.length > 1 && selectedImageIndex > 0"
                        @click="previousImage" class="image-modal-nav image-modal-nav-prev">
                        ‹
                    </button>
                    <button
                        v-if="taskData && taskData.images.length > 1 && selectedImageIndex < taskData.images.length - 1"
                        @click="nextImage" class="image-modal-nav image-modal-nav-next">
                        ›
                    </button>
                    <img v-if="taskData && taskData.images[selectedImageIndex]"
                        :src="getImageUrl(taskData.images[selectedImageIndex].image_url)"
                        :alt="`Image ${selectedImageIndex + 1}`" class="image-modal-img" />
                    <div v-if="taskData && taskData.images.length > 1" class="image-modal-counter">
                        {{ selectedImageIndex + 1 }} / {{ taskData.images.length }}
                    </div>
                </div>
            </div>
        </Transition>
    </div>
</template>

<script setup lang="ts">
import { API_HOST, API_URL } from "@/app/composables/useUtils";
import { useStore } from "@/app/composables/useStore";
import { useLoading } from "@/app/composables/useLoading";

useHead({
    title: `一周CP 2026 | Day ${useRoute().params.day} 任务`,
});

const route = useRoute();
const day = computed(() => parseInt(route.params.day as string));

const { get, post, del } = useRequest();
const { getToken } = useStore();
const { startLoading, stopLoading } = useLoading();
const taskData = ref<any>(null);
const loading = ref(true);
const error = ref<string | null>(null);
const editedText = ref("");
const saving = ref(false);
const removingImageId = ref<string | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);
const selectedImageIndex = ref<number | null>(null);

const getImageUrl = (path: string | null) => {
    if (!path) return '';
    // If path already includes the full URL, return as is
    if (path.startsWith('http')) return path;
    return `${API_HOST}${path}`;
};

const loadTaskData = async () => {
    loading.value = true;
    error.value = null;

    try {
        const res = await get(`tasks/${day.value}/`);
        if (res.ok) {
            const data = await res.json();
            taskData.value = data.data;
            editedText.value = data.data.submit_text || "";
        } else {
            const errorData = await res.json();
            throw new Error(errorData.detail || res.statusText);
        }
    } catch (err: any) {
        error.value = err.message || '加载任务数据失败';
        console.error(err);
    } finally {
        loading.value = false;
    }
};

const saveTask = async () => {
    if (!taskData.value) return;

    saving.value = true;
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
    } finally {
        saving.value = false;
    }
};

const removeImage = async (imageId: string) => {
    if (!confirm('确定要删除这张图片吗？')) return;

    removingImageId.value = imageId;
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
    } finally {
        removingImageId.value = null;
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
    if (currentImageCount + files.length > 20) {
        alert('最多只能上传20张图片');
        target.value = '';
        return;
    }

    // Validate file sizes and types
    const validFiles: File[] = [];
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (!file) continue;
        if (file.size > 5 * 1024 * 1024) {
            alert(`图片 ${file.name} 超过5MB，已跳过`);
            continue;
        }
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

    // Upload images
    saving.value = true;
    try {
        const formData = new FormData();
        validFiles.forEach(file => {
            formData.append('images', file);
        });

        startLoading();
        const response = await fetch(`${API_URL}/tasks/${day.value}/imgs/`, {
            method: 'POST',
            headers: {
                'Authorization': getToken() || '',
            },
            body: formData,
        });
        stopLoading();

        if (response.ok) {
            // Reload task data to get updated images
            await loadTaskData();
            alert('图片上传成功');
        } else {
            const errorData = await response.json();
            throw new Error(errorData.detail || response.statusText);
        }
    } catch (err: any) {
        alert(err.message || '上传图片失败');
        console.error(err);
    } finally {
        saving.value = false;
        target.value = '';
    }
};

const openImageModal = (index: number) => {
    selectedImageIndex.value = index;
};

const closeImageModal = () => {
    selectedImageIndex.value = null;
};

const previousImage = () => {
    if (selectedImageIndex.value !== null && selectedImageIndex.value > 0) {
        selectedImageIndex.value--;
    }
};

const nextImage = () => {
    if (selectedImageIndex.value !== null && taskData.value && selectedImageIndex.value < taskData.value.images.length - 1) {
        selectedImageIndex.value++;
    }
};

// Close modal on ESC key
onMounted(() => {
    if (day.value < 1 || day.value > 7) {
        error.value = '无效的任务天数，必须是1-7之间的数字';
        loading.value = false;
        return;
    }
    loadTaskData();

    const handleEsc = (e: KeyboardEvent) => {
        if (e.key === 'Escape' && selectedImageIndex.value !== null) {
            closeImageModal();
        }
    };
    window.addEventListener('keydown', handleEsc);
    onUnmounted(() => {
        window.removeEventListener('keydown', handleEsc);
    });
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

h3 {
    font-size: var(--fs-500);
    color: var(--clr-text);
    margin-bottom: 0.75rem;
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

/* Mission Description Section */
.mission-description-placeholder {
    text-align: center;
    padding: 2rem 1rem;
    background: var(--clr-background);
    border-radius: 0.5rem;
    border: 2px dashed var(--clr-text--muted);
}

.placeholder-text {
    font-size: var(--fs-400);
    color: var(--clr-text--muted);
    margin: 0;
}

/* Submission Section */
.submission-field {
    margin-bottom: 1.5rem;
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
    border-radius: 0.5rem;
    font-size: var(--fs-400);
    background: var(--clr-background);
    color: var(--clr-text);
    font-family: inherit;
    resize: vertical;
    box-sizing: border-box;
}

.text-input:focus {
    outline: none;
    border-color: var(--clr-primary);
}

.field-hint {
    font-size: var(--fs-300);
    color: var(--clr-text--muted);
    margin-top: 0.5rem;
    margin-bottom: 0;
}

/* Images Container */
.images-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 1rem;
    margin-bottom: 0.5rem;
}

.image-item {
    position: relative;
    aspect-ratio: 1;
    border-radius: 0.5rem;
    overflow: hidden;
    border: 2px solid var(--clr-text--muted);
    background: var(--clr-background);
}

.image-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.image-item img.clickable-image {
    cursor: pointer;
    transition: opacity 0.2s;
}

.image-item img.clickable-image:hover {
    opacity: 0.9;
}

.remove-image-btn {
    position: absolute;
    top: 0.25rem;
    right: 0.25rem;
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    border: none;
    font-size: 1.25rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: var(--transition);
    line-height: 1;
}

.remove-image-btn:hover:not(:disabled) {
    background: rgba(220, 53, 69, 0.9);
}

.remove-image-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.image-upload-placeholder {
    aspect-ratio: 1;
    border: 2px dashed var(--clr-text--muted);
    border-radius: 0.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: var(--transition);
    background: var(--clr-background);
}

.image-upload-placeholder:hover {
    border-color: var(--clr-primary);
    background: var(--clr-primary-light);
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

/* Scores Section */
.scores-section {
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 2px solid var(--clr-background);
}

.scores-grid {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.score-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1rem;
    background: var(--clr-background);
    border-radius: 0.5rem;
    border: 1px solid var(--clr-text--muted);
}

.score-label {
    font-size: var(--fs-400);
    color: var(--clr-text);
    font-weight: 600;
}

.score-value {
    font-size: var(--fs-400);
    color: var(--clr-text);
}

.score-value.completed {
    color: var(--clr-primary-dark);
    font-weight: 600;
}

.score-points {
    font-size: var(--fs-400);
    color: var(--clr-primary);
    font-weight: 600;
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

.btn.secondary:hover:not(:disabled) {
    background: var(--clr-secondary-dark);
}

/* Image Modal Styles */
.image-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.9);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2000;
    padding: 0.5rem;
    backdrop-filter: blur(4px);
}

.image-modal-content {
    position: relative;
    max-width: 90vw;
    max-height: 90vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.image-modal-close {
    position: fixed;
    top: 2rem;
    right: 2rem;
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: none;
    font-size: 2.5rem;
    width: 3rem;
    height: 3rem;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: var(--transition);
    z-index: 2001;
    line-height: 1;
}

.image-modal-close:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: scale(1.1);
}

.image-modal-img {
    max-width: 100%;
    max-height: 90vh;
    object-fit: contain;
    border-radius: 0.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.image-modal-nav {
    position: fixed;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: none;
    font-size: 3rem;
    width: 4rem;
    height: 4rem;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: var(--transition);
    z-index: 2001;
    line-height: 1;
    font-weight: bold;
}

.image-modal-nav:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-50%) scale(1.1);
}

.image-modal-nav-prev {
    left: 2rem;
}

.image-modal-nav-next {
    right: 2rem;
}

.image-modal-counter {
    position: fixed;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    color: white;
    font-size: var(--fs-400);
    background: rgba(0, 0, 0, 0.5);
    padding: 0.5rem 1rem;
    border-radius: 1rem;
    z-index: 2001;
}

/* Modal Transitions */
.modal-enter-active,
.modal-leave-active {
    transition: opacity 0.3s ease;
}

.modal-enter-active .image-modal-content,
.modal-leave-active .image-modal-content {
    transition: transform 0.3s ease, opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}

.modal-enter-from .image-modal-content,
.modal-leave-to .image-modal-content {
    transform: scale(0.9);
    opacity: 0;
}

@media (max-width: 768px) {
    .image-modal-nav {
        width: 3rem;
        height: 3rem;
        font-size: 2rem;
    }

    .image-modal-nav-prev {
        left: 0.5rem;
    }

    .image-modal-nav-next {
        right: 0.5rem;
    }

    .image-modal-close {
        top: 1rem;
        right: 1rem;
        width: 2.5rem;
        height: 2.5rem;
        font-size: 2rem;
    }

    .image-modal-counter {
        bottom: 1rem;
    }
}
</style>
