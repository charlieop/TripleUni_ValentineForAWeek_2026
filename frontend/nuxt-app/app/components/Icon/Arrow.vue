<template>
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32"
        viewBox="1 0 24 24"><!-- Icon from Material Symbols by Google - https://github.com/google/material-design-icons/blob/master/LICENSE -->
        <path fill="currentColor" d="M16 22L6 12L16 2l1.775 1.775L9.55 12l8.225 8.225z" />
    </svg>
</template>

<script setup lang="ts">
const props = defineProps<{
    size: string | null;
    color: string | null;
}>();
</script>

<style scoped>
svg {
    width: v-bind(size);
    height: v-bind(size);
    color: v-bind(color);
}
</style>