<template>
  <div>
    <h1>Hello World</h1>
    <div class="button-group">
      <button @click="navigateTo('/apply')">活动报名</button>
      <button @click="navigateTo('/payment')">支付押金</button>
      <button @click="navigateTo('/withdraw')">撤销申请</button>
    </div>
  </div>
</template>

<script setup lang="ts">


</script>

<style scoped>

</style>