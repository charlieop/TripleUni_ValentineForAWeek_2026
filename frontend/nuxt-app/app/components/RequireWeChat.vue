<template>
    <Transition name="fade">
        <div v-if="!isWechat" class="modal-overlay">
            <div class="modal-container">
                <div class="card">
                    <div class="card-header">
                        <h2>请使用微信内置浏览器打开</h2>
                    </div>
                    <div class="card-body">
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
                    <div class="card-footer">
                        <button class="btn-primary" @click="copyAndRedirect">
                            复制链接并前往微信
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup lang="ts">
async function copyAndRedirect() {
    const url = window.location.href;
    if (navigator.clipboard) {
        await navigator.clipboard.writeText(url);
        alert("链接已复制, 正在前往微信内置浏览器打开");
    } else {
        try {
            var textarea = document.createElement("textarea");
            document.body.appendChild(textarea);
            // 隐藏此输入框
            textarea.style.position = "fixed";
            textarea.style.clip = "rect(0 0 0 0)";
            textarea.style.top = "10px";
            // 赋值
            textarea.value = url;
            // 选中
            textarea.select();
            // 复制
            document.execCommand("copy", true);
            // 移除输入框
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
.modal-container {
    width: 100%;
    max-width: 32rem;
}

.card {
    background-color: white;
    border-radius: 0.5rem;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
        0 10px 10px -5px rgba(0, 0, 0, 0.04);
    overflow: hidden;
}

.card-header {
    padding: 1.5rem;
    border-bottom: 1px solid #e5e7eb;
}

.card-header h2 {
    font-size: var(--fs-500);
    margin: 0;
    font-weight: 600;
}

.card-body {
    padding: 1.5rem;
}

.card-body p {
    margin: 0;
    line-height: 1.5;
}

.card-footer {
    padding: 1.5rem;
    border-top: 1px solid #e5e7eb;
    display: flex;
    justify-content: flex-end;
}

.btn-primary {
    background-color: #3b82f6;
    color: white;
    padding: 0.625rem 1.25rem;
    border-radius: 0.375rem;
    border: none;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.15s ease-in-out;
}

.btn-primary:hover {
    background-color: #2563eb;
}

.btn-primary:active {
    background-color: #1d4ed8;
}

.btn-primary:focus {
    outline: 2px solid #3b82f6;
    outline-offset: 2px;
}
</style>