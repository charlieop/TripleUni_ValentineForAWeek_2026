<template>
    <div class="page-wrapper flower-background">
        <div class="title-wrapper">
            <h1 class="page-title">秘密任务</h1>
            <LogoSm />
        </div>

        <template v-if="error">
            <div class="state-card error">
                <div class="state-icon">❌</div>
                <p class="state-title">加载失败</p>
                <p class="state-message">{{ error }}</p>
            </div>
            <div class="button-group">
                <button @click="loadSecretTask" class="btn primary">重试</button>
                <button @click="navigateTo('/match')" class="btn">返回</button>
            </div>
        </template>

        <div v-else class="task-content">
            <section class="mission-section">
                <h2 class="section-title">任务描述</h2>
                <div class="mission-card">
                    <div v-if="secretTask" class="mission-body">
                        <h3 class="mission-title">1. 仅你可见 (Day 3 前完成)</h3>
                        <p class="mission-content">
                            今天是见到ta的第一天！不知道你的心情是期待，抑或是害羞呢？发出一个仅ta可见的朋友圈记录下此刻的心情与想对ta说的话吧！在第三天，你们向对方打开朋友圈权限之时，不知道ta是否会注意到这条特殊的朋友圈呢？
                        </p>
                        <br>
                        <h3 class="mission-title">2. {{ secretTask.title }}</h3>
                        <p class="mission-content">{{ secretTask.desc }}</p>
                        <p class="mission-note">
                            请不要向你的 CP 透露这项秘密任务，直到 Day 7 再向对方展示并上传。
                        </p>
                    </div>
                    <div v-else class="mission-placeholder">
                        <p class="placeholder-text">加载中...</p>
                    </div>
                </div>
            </section>

            <section class="actions-section">
                <button @click="navigateTo('/match')" class="btn primary">返回</button>
            </section>
        </div>
    </div>
</template>

<script setup lang="ts">
useHead({
    title: "一周CP 2026 | 秘密任务",
});

const { get } = useRequest();

type SecretTask = {
    title: string;
    desc: string;
};

const secretTask = ref<SecretTask | null>(null);
const error = ref<string | null>(null);

const loadSecretTask = async () => {
    error.value = null;
    secretTask.value = null;

    try {
        const res = await get("tasks/secret/");
        if (res.ok) {
            const data = await res.json();
            secretTask.value = data.data;
        } else {
            const errorData = await res.json();
            throw new Error(errorData.detail || res.statusText);
        }
    } catch (err: any) {
        error.value = err.message || "加载秘密任务失败";
        console.error(err);
    }
};

onMounted(() => {
    loadSecretTask();
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

section {
    padding-inline: 0.75rem;
    margin-block: 2rem;
}

.task-content {
    padding-bottom: 2rem;
}

.section-title {
    font-size: var(--fs-600);
    color: var(--clr-primary-dark);
    font-weight: 900;
    text-align: left;
    padding-inline: 0.5rem;
    backdrop-filter: blur(1px);
    -webkit-backdrop-filter: blur(1px);
}

.mission-card {
    margin-top: 0.75rem;
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
    margin: 0;
    font-size: var(--fs-300);
}

.mission-note {
    margin: 0.75rem 0 0;
    font-size: var(--fs-300);
    color: var(--clr-text--muted);
    line-height: 1.5;
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

.actions-section {
    padding-inline: 0.75rem;
    margin-block: 1.5rem 3rem;
    display: flex;
}

.actions-section>button {
    width: 100%;
}
</style>