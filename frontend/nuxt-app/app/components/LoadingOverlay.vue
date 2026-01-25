<template>
  <Transition name="fade">
    <div v-if="isLoading" class="modal-overlay">
      <LogoLg />
      <div class="loading-text">
        <p>丘比特搜寻中</p>
        <p>请稍候<span class="dots">...</span></p>
      </div>
      <div class="decor">
        <IconHeart class="heart-icon heart3" size="140%" color="hsl(353, 58%, 61%)" />
        <IconHeart class="heart-icon heart2" size="120%" color="hsl(353, 58%, 51%)" />
        <IconHeart class="heart-icon heart1" size="100%" color="hsl(353, 58%, 41%)" />
        <img src="@/assets/imgs/cupid-flying.png" alt="decor" class="decor-img">
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
const { isLoading } = useLoading();
</script>

<style scoped>
.modal-overlay {
  display: block;

}

.loading-text {
  font-size: var(--fs-600);
  color: #EFEFEF;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.dots {
  display: inline-block;
  width: fit-content;
  font-weight: bold;
  font-family: monospace;
  font-size: 20px;
  clip-path: inset(0 3ch 0 0);
  animation: l4 3s steps(4) infinite;
}
@keyframes l4 {
  to {
    clip-path: inset(0 -1ch 0 0);
  }
}

.decor {
  position: absolute;
  bottom: 3rem;
  left: 0;
  z-index: 1;
}

.heart-icon {
  position: absolute;
  left: -0.5px;
  animation: heartAppear 3s ease-in-out infinite;
}

.heart1 {
  top: 2%;
  animation-delay: 0s;
}

.heart2 {
  top: -10%;
  animation-delay: 0.3s;
}

.heart3 {
  top: -22%;
  animation-delay: 0.6s;
}

@keyframes heartAppear {
  0% {
    opacity: 0;
    transform: scale(0.5);
  }

  5% {
    opacity: 0;
    transform: scale(0.5);
  }

  25% {
    opacity: 1;
    transform: scale(1);
  }

  75% {
    opacity: 1;
    transform: scale(1);
  }

  100% {
    opacity: 0;
    transform: scale(0.5);
  }
}


.decor-img {
  position: relative;
  width: 70%;
  margin: 0 auto;
  object-fit: cover;
  z-index: 10;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
