<template>
    <div>
        <h1>支付押金</h1>
        <div class="button-group">
            <button disabled>支付押金</button>
            <button @click="navigateTo('/')">返回首页</button>
        </div>
    </div>
</template>

<script setup lang="ts">
useHead({
    title: "一周CP 2026 | 支付押金",
});
</script>

<style scoped></style>