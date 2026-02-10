<template>
  <div class="page-wrapper heart-background">
    <LogoSm />
    <h1 class="page-title">里程排行榜</h1>
    <p class="leaderboard-total">{{ rankMode === 'total' ? '快来看看你与你的CP走了多远吧！' : `第${currentDay ?? '?'}日里程排行` }}</p>

    <div class="tab-row">
      <button
        type="button"
        class="tab-btn"
        :class="{ 'tab-btn--active': rankMode === 'total' }"
        @click="setRankMode('total')"
      >
        总里程
      </button>
      <button
        type="button"
        class="tab-btn"
        :class="{ 'tab-btn--active': rankMode === 'daily' }"
        @click="setRankMode('daily')"
      >
        今日里程
      </button>
    </div>

    <template v-if="error">
      <div class="state-card error">
        <div class="state-icon">❌</div>
        <p class="state-title">加载失败</p>
        <p class="state-message">{{ error }}</p>
      </div>
      <div class="button-group">
        <button class="btn primary" @click="loadInitial">重试</button>
        <NuxtLink to="/" class="btn">返回首页</NuxtLink>
      </div>
    </template>

    <template v-else>
      <section class="leaderboard-section">
        <div v-if="loading" class="load-more">加载中...</div>
        <template v-else>
          <ul class="rank-list">
            <li v-for="entry in ranks" :key="entry.id" class="rank-row" :class="{
              'rank-row--top3': entry.rank <= 3,
              'rank-row--high-score': entry.score > 520
            }">
              <span class="rank-cell" :class="'rank-cell--' + Math.min(entry.rank, 4)">
                <span v-if="entry.rank === 1" class="rank-trophy" aria-label="第1名">🥇</span>
                <span v-else-if="entry.rank === 2" class="rank-trophy" aria-label="第2名">🥈</span>
                <span v-else-if="entry.rank === 3" class="rank-trophy" aria-label="第3名">🥉</span>
                <span v-else class="rank-num">{{ entry.rank }}</span>
              </span>
              <span class="rank-name">{{ entry.name }}</span>
              <span class="rank-id">#{{ entry.id }}</span>
              <span class="rank-score">{{ entry.score }} km</span>
            </li>
          </ul>
          <div v-if="hasMore && !loadingMore" ref="sentinelRef" class="sentinel" aria-hidden="true" />
          <div v-if="loadingMore" class="load-more">加载中...</div>
          <div v-else-if="total !== null && total > 0 && ranks.length >= total" class="load-more end">
            已经到底啦
          </div>
          <div v-else-if="!loading && total === 0" class="state-card empty">
            <div class="state-icon">🏆</div>
            <p class="state-title">暂无排行</p>
            <p class="state-message">活动开始后将显示CP组得分排行</p>
          </div>
        </template>
      </section>

      <div class="button-group">
        <NuxtLink to="/" class="btn primary">返回首页</NuxtLink>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { API_URL } from "~/composables/useConfigs";

useHead({
  title: "一周CP 2026 | 排行榜",
});

const PAGE_SIZE = 50;

interface RankEntry {
  id: number;
  name: string;
  score: number;
  rank: number;
}

type RankMode = "total" | "daily";

const rankMode = ref<RankMode>("total");
const currentDay = ref<number | null>(null);
const ranks = ref<RankEntry[]>([]);
const total = ref<number | null>(null);
const loading = ref(true);
const loadingMore = ref(false);
const error = ref<string | null>(null);
const sentinelRef = ref<HTMLElement | null>(null);

const hasMore = computed(
  () =>
    total.value !== null &&
    ranks.value.length < total.value &&
    !loading.value
);

async function fetchPage(
  startPos: number,
  endPos: number,
  mode: RankMode = rankMode.value
): Promise<{ total: number; ranks: RankEntry[]; day?: number }> {
  const url = `${API_URL}/ranks/?start_pos=${startPos}&end_pos=${endPos}&type=${mode}`;
  const res = await fetch(url);
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || res.statusText || "加载失败");
  }
  return res.json();
}

function setRankMode(mode: RankMode) {
  if (rankMode.value === mode) return;
  rankMode.value = mode;
  loadInitial();
}

async function loadInitial() {
  error.value = null;
  loading.value = true;
  ranks.value = [];
  total.value = null;
  currentDay.value = null;
  try {
    const data = await fetchPage(1, PAGE_SIZE, rankMode.value);
    total.value = data.total;
    ranks.value = data.ranks || [];
    currentDay.value = data.day ?? null;
  } catch (e: any) {
    error.value = e.message || "加载失败";
  } finally {
    loading.value = false;
  }
}

async function loadMore() {
  if (loadingMore.value || total.value === null || ranks.value.length >= total.value) return;
  loadingMore.value = true;
  const startPos = ranks.value.length + 1;
  const endPos = Math.min(ranks.value.length + PAGE_SIZE, total.value);
  try {
    const data = await fetchPage(startPos, endPos, rankMode.value);
    ranks.value = [...ranks.value, ...(data.ranks || [])];
  } catch (e: any) {
    error.value = e.message || "加载更多失败";
  } finally {
    loadingMore.value = false;
  }
}

let observer: IntersectionObserver | null = null;

onMounted(() => {
  loadInitial();
  observer = new IntersectionObserver(
    (entries) => {
      const entry = entries[0];
      if (entry?.isIntersecting && hasMore.value) {
        loadMore();
      }
    },
    { root: null, rootMargin: "200px", threshold: 0 }
  );
});

onBeforeUnmount(() => {
  observer?.disconnect();
});

watch(sentinelRef, (el, prev) => {
  if (!observer) return;
  if (prev) observer.unobserve(prev);
  if (el) observer.observe(el);
}, { flush: "post" });
</script>

<style scoped>
.leaderboard-section {
  background: hsla(356, 100%, 98%, 0.3);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  margin-bottom: 2rem;
  padding: 1rem;
  border-radius: 1rem;
  max-width: 520px;
  margin-inline: auto;
}

.leaderboard-total {
  font-size: var(--fs-300);
  color: var(--clr-text--muted);
  text-align: center;
  margin: 0 0 1rem;
}

.tab-row {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  margin-bottom: 1rem;
  max-width: 400px;
  padding-inline: 1rem;
  margin-inline: auto;
}

.tab-btn {
  flex: 1;
  padding: 0.5rem 1.25rem;
  font-size: var(--fs-300);
  font-weight: 600;
  border-radius: 2rem;
  border: 2px solid var(--clr-primary);
  background: rgba(254, 234, 244, 0.687);
  color: var(--clr-primary);
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.tab-btn--active {
  background: var(--clr-primary);
  color: white;
}

.rank-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.rank-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.55);
  border-radius: 0.75rem;
  font-size: var(--fs-400);
}

.rank-row--top3 {
  background: rgba(255, 248, 240, 0.85);
  border: 1px solid rgba(255, 196, 140, 0.35);
}

.rank-row--high-score {
  background: linear-gradient(135deg, rgba(255, 216, 222, 0.35), rgba(255, 155, 205, 0.2));
  border: 1px solid rgba(255, 105, 180, 0.45);
  box-shadow: 0 0 0 1px rgba(255, 182, 193, 0.3) inset;
}

.rank-row--top3.rank-row--high-score {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.35), rgba(255, 230, 180, 0.45));
  border-color: rgba(255, 180, 80, 0.55);
}

.rank-cell {
  flex-shrink: 0;
  width: 2.5rem;
  height: 2.5rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.rank-trophy {
  font-size: 1.75rem;
  line-height: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.rank-num {
  width: 1.75rem;
  height: 1.75rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-weight: 800;
  font-size: var(--fs-300);
  background: var(--clr-text--muted);
  color: var(--clr-background);
}

.rank-cell--1 .rank-trophy {
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.rank-cell--2 .rank-trophy {
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.rank-cell--3 .rank-trophy {
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.rank-name {
  flex: 1;
  min-width: 0;
  white-space: normal;
  word-break: break-word;
  overflow-wrap: break-word;
  font-weight: 600;
  color: var(--clr-text);
}

.rank-id {
  flex-shrink: 0;
  font-size: var(--fs-300);
  color: var(--clr-text--muted);
  font-weight: 600;
}

.rank-score {
  flex-shrink: 0;
  font-weight: 800;
  color: var(--clr-primary-dark);
}

.sentinel {
  height: 1px;
  width: 100%;
  pointer-events: none;
  visibility: hidden;
}

.load-more {
  text-align: center;
  padding: 1rem;
  font-size: var(--fs-300);
  color: var(--clr-text--muted);
}

.load-more.end {
  color: var(--clr-primary-dark);
  font-weight: 600;
}

.button-group {
  margin-block: 2rem 4rem;
}

.button-group .btn {
  text-shadow: none;
}

.button-group :deep(a) {
  display: block;
  text-align: center;
  text-decoration: none;
  color: inherit;
}
</style>
