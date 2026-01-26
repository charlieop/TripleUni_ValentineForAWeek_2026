<template>
    <Modal v-model="showModal" :show-close-button="false">
        <div class="require-wechat-content">
            <div class="require-wechat-header">
                <h2>请使用微信内置浏览器打开</h2>
            </div>
            <div class="require-wechat-body">
                <p>
                    Triple Uni 需要使用你的微信信息用于<strong>登陆与验证</strong>,
                    我们无法在非微信环境请求你的授权。
                </p>
                <br />
                <p>
                    我们会在你授权后获取并保存你的<strong>微信昵称与头像</strong>用于展示匹配结果
                    <strong>我们不会通过微信授权收集其他信息</strong>。
                </p>
                <br />
                <p>请使用微信内置浏览器打开此页面以继续。</p>
            </div>
            <div class="require-wechat-footer">
                <button class="btn" @click="copyAndRedirect">
                    复制链接并前往微信
                </button>
            </div>
        </div>
    </Modal>
</template>

<script setup lang="ts">
import { isWechat } from '~/composables/useUtils';

// Modal should always be shown when not in WeChat, so prevent closing
const showModal = computed({
    get: () => !isWechat.value,
    set: () => {
        // Prevent closing - always show when not in WeChat
    }
});

async function copyAndRedirect() {
    const url = window.location.href;
    if (navigator.clipboard) {
        await navigator.clipboard.writeText(url);
        alert("链接已复制, 正在前往微信内置浏览器打开");
    } else {
        try {
            var textarea = document.createElement("textarea");
            document.body.appendChild(textarea);
            textarea.style.position = "fixed";
            textarea.style.clip = "rect(0 0 0 0)";
            textarea.style.top = "10px";
            textarea.value = url;
            textarea.select();
            document.execCommand("copy", true);
            document.body.removeChild(textarea);
            alert("链接已复制, 正在前往微信内置浏览器打开");
        } catch (error) {
            alert("复制失败, 请手动复制链接");
        }
    }
    window.location.href = "weixin://";
}
</script>

<style scoped>
.require-wechat-content {
    display: flex;
    flex-direction: column;
}

.require-wechat-header {
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--clr-border, #e5e7eb);
}

.require-wechat-header h2 {
    font-size: var(--fs-500);
    margin: 0;
    font-weight: 600;
    color: var(--clr-primary-dark);
}

.require-wechat-body {
    flex: 1;
    margin-bottom: 1.5rem;
}

.require-wechat-body p {
    margin: 0;
    line-height: 1.5;
    color: var(--clr-text);
}

.require-wechat-footer {
    padding-top: 1rem;
    border-top: 1px solid var(--clr-border, #e5e7eb);
    display: flex;
    justify-content: center;
}

.btn {
    background: var(--clr-primary-dark);
    color: #EFEFEF;
    font-size: var(--fs-300);
}
</style>