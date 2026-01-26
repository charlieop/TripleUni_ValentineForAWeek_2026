<template>
    <Transition name="modal-transition">
        <div v-if="modelValue" :class="class" class="modal-overlay" @click="handleOverlayClick">
            <div class="modal-content" @click.stop>
                <button v-if="showCloseButton" class="modal-close" @click="close" aria-label="Close">
                    <IconCross size="1.5rem" color="var(--clr-text--muted)" />
                </button>
                <div class="modal-body">
                    <slot />
                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup lang="ts">
const props = withDefaults(defineProps<{
    modelValue: boolean;
    showCloseButton?: boolean;
    class?: string;
}>(), {
    showCloseButton: true
});

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void;
}>();

const close = () => {
    emit('update:modelValue', false);
};

const handleOverlayClick = () => {
    close();
};

// Disable body scrolling when modal is open
let originalBodyOverflow: string | null = null;

const disableBodyScroll = () => {
    if (originalBodyOverflow === null) {
        originalBodyOverflow = document.body.style.overflow;
    }
    document.body.style.overflow = 'hidden';
};

const enableBodyScroll = () => {
    if (originalBodyOverflow !== null) {
        document.body.style.overflow = originalBodyOverflow;
        originalBodyOverflow = null;
    } else {
        document.body.style.overflow = '';
    }
};

// watch(() => props.modelValue, (isOpen) => {
//     if (isOpen) {
//         disableBodyScroll();
//     } else {
//         enableBodyScroll();
//     }
// }, { immediate: true });

// Close modal on ESC key
onMounted(() => {
    const handleEsc = (e: KeyboardEvent) => {
        if (e.key === 'Escape' && props.modelValue) {
            close();
        }
    };
    window.addEventListener('keydown', handleEsc);
    onUnmounted(() => {
        window.removeEventListener('keydown', handleEsc);
        // Ensure body scroll is re-enabled when component is unmounted
        enableBodyScroll();
    });
});
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    inset: 0;
    background-color: rgba(0, 0, 0, 0.65);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999;
    padding: 1.5rem;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    touch-action: none;
}

.modal-content {
    position: relative;
    background: var(--clr-background);
    border-radius: 1rem;
    padding: 2rem;
    width: 100%;
    max-width: min(500px, 90vw);
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.modal-close {
    position: absolute;
    top: 0.75rem;
    right: 0.75rem;
    background: transparent;
    border: none;
    font-size: 2rem;
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: var(--transition);
}

.modal-close:hover {
    background: var(--clr-background--muted);
    color: var(--clr-text);
    transform: scale(1.1);
}

.modal-body {
    padding-top: 0.5rem;
}
</style>
