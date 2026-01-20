<template>
    <div>
        <h1>Withdraw</h1>
        <div class="button-group">
            <button v-if="!clicked" @click="confirmWithdraw" class="first-click">撤销申请</button>
            <button v-else @click="confirmWithdraw" class="second-click">再次点击以确认撤销</button>
            <button @click="navigateTo('/')">返回首页</button>
        </div>
    </div>
</template>

<script setup lang="ts">
useHead({
    title: "一周CP 2026 | 取消申请",
});

const clicked = ref(false);
const { del } = useRequest();

function confirmWithdraw() {
    if (!clicked.value) {
        clicked.value = true;
        return;
    }

    del("applicants/").then((res) => {
        navigateTo("/");
    }).catch((err) => {
        console.error(err);
    });
}
</script>

<style scoped>
.first-click {
    background-color: var(--clr-primary);
}

.second-click {
    background-color: var(--clr-danger);
}
</style>