<template>
    <div class="page-wrapper paper-background">
        <LogoSm />
        <h1 class="page-title">退出活动</h1>

        <div class="info-section">
            <img src="/imgs/paperslip.png" alt="" class="bg-img">
            <div class="warning-card">
                <p class="warning-title">请注意: </p>
                <p class="warning-text">
                    退出活动后，你将<strong>无法再次参加</strong>本次活动。此操作不可撤销。
                </p>
                <p class="warning-subtext">
                    我们将在活动结束后退还全部押金。
                </p>
            </div>
        </div>

        <div class="button-group">
            <button v-if="!clicked" @click="confirmWithdraw" class="btn">
                退出活动
            </button>
            <button v-else @click="confirmWithdraw" class="btn danger">
                再次点击以确认退出
            </button>
            <button @click="navigateTo('/')" class="btn primary">返回首页</button>
        </div>
    </div>
</template>

<script setup lang="ts">
useHead({
    title: "一周CP 2026 | 退出活动",
});

const clicked = ref(false);
const { del } = useRequest();

function confirmWithdraw() {
    if (!clicked.value) {
        clicked.value = true;
        return;
    }

    del("applicants/")
        .then(async (res) => {
            if (res.ok) {
                await fetchUserState();
                navigateTo("/");
            } else {
                throw new Error("退出活动失败");
            }
        })
        .catch((err) => {
            alert(err.message || "退出活动失败");
            console.error(err);
            clicked.value = false;
        });
}
</script>

<style scoped>
.info-section {
    position: relative;
    margin-block: 1rem;
}

.bg-img {
    min-height: 13rem;
}

.warning-card {
    font-size: var(--fs-400);
    position: absolute;
    inset: 9% 3%;
    padding: 1rem;
    z-index: 1;
}

.warning-title {
    font-size: var(--fs-500);
}


.btn {
    font-size: var(--fs-500);
}
</style>
