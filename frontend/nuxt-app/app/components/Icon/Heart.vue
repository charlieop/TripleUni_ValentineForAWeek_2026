<template>
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" version="1.1" shape-rendering="geometricPrecision" text-rendering="geometricPrecision" image-rendering="optimizeQuality" fill-rule="evenodd" clip-rule="evenodd" viewBox="0 0 5000000 4800000" x="0px" y="0px"><g><path fill-rule="nonzero" d="M2500591 1022631c78782,-120004 163587,-218866 261740,-297293 173155,-138548 376666,-207881 643839,-207881 297057,0 566239,120595 761008,315365l9450 10157c189218,194062 305915,459109 305915,750969 0,494779 -240362,980228 -600846,1460951 -349735,466314 -805419,921998 -1261103,1377682 -66498,66498 -174572,66498 -241070,0 -455684,-455684 -911368,-911368 -1261103,-1377682 -360484,-480723 -600846,-966172 -600846,-1460951 0,-297057 120595,-566238 315365,-761126 194770,-194770 463951,-315365 761126,-315365 433478,0 688486,168431 906525,505174z"/></g></svg>
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
    fill: v-bind(color);
}
</style>