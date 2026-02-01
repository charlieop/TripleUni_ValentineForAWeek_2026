<template>
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32"
        viewBox="0 0 24 24"><!-- Icon from Sharp free icons by Streamline - https://creativecommons.org/licenses/by/4.0/ -->
        <path fill="currentColor" fill-rule="evenodd"
            d="M12 23c6.075 0 11-4.925 11-11S18.075 1 12 1S1 5.925 1 12s4.925 11 11 11M9 11.5h2v4H9v2h6v-2h-2v-6H9zM13 8V6h-2v2z"
            clip-rule="evenodd" />
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