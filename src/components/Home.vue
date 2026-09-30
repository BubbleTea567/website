<script setup>
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import gameplayImage from '../assets/gameplay.jpg'
import heroImage from '../assets/hero.jpg'

const navLinks = [
  { label: '玩法特色', href: '#features' },
  { label: '魔法玩法', href: '#gameplay' },
  { label: '服务器信息', href: '#server' },
  { label: '加入我们', href: '#join' },
]

const stats = [
  { value: 'Java 版 1.20+', label: '支持版本' },
  { value: '魔法生存 · RPG', label: '玩法定位' },
  { value: '全天候开放', label: '在线时间' },
]

const features = [
  {
    title: '自定义法术体系',
    desc: '从咒语吟唱到符文刻印，自由组合法术效果与施法方式，打造只属于你的战斗风格。',
    icon: 'book',
  },
  {
    title: '元素派系进阶',
    desc: '火、水、风、雷等元素派系各具特色，随着修行深入，逐步解锁更强大的大魔法。',
    icon: 'flame',
  },
  {
    title: '遗迹探索与副本',
    desc: '主世界中散布着神秘魔法遗迹，与伙伴组队挑战高难副本，赢取稀有材料与专属装备。',
    icon: 'compass',
  },
  {
    title: '稳定社区与活动',
    desc: '长期稳定的服务器环境与友善活跃的社区，定期举办魔法主题活动与竞技联赛。',
    icon: 'shield',
  },
]

const gameplayPoints = [
  {
    title: '咒语吟唱与即时施法',
    desc: '学习咒语后可通过快捷栏与法杖即时施法，战斗节奏流畅，也支持编写专属法术组合。',
  },
  {
    title: '法杖、符文与炼金三条成长线',
    desc: '锻造法杖、铭刻符文、调配药剂，不同成长路线相互搭配，形成多样的养成体验。',
  },
  {
    title: '世界 BOSS 与限时魔法事件',
    desc: '定期刷新世界 BOSS 与限时魔法事件，全服玩家共同参与，争夺稀有奖励与称号。',
  },
]

const serverMeta = [
  { label: '支持版本', value: '即将推出' },
  { label: '玩法模式', value: '即将推出' },
  { label: '登录方式', value: '即将推出' },
]

// 用于追踪当前活跃区块的索引
const sections = ref([])
const activeSection = ref(0)
const snapContainer = ref(null)
let observer = null
let animObserver = null

const sectionLabels = ['首页', '玩法特色', '魔法玩法', '服务器信息', '加入我们', '页脚']

onMounted(async () => {
  await nextTick()
  sections.value = Array.from(document.querySelectorAll('[data-snap-section]'))
  snapContainer.value = document.querySelector('.snap-container')

  // 启用全屏 snap 模式（门控：无 JS 时页面仍可正常滚动）
  document.documentElement.classList.add('snap-mode')

  // 标记动画就绪，启用翻页过渡
  requestAnimationFrame(() => {
    snapContainer.value?.classList.add('anim-ready')
  })

  // 用于翻页指示器的活跃区块追踪
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const idx = Number(entry.target.dataset.sectionIndex)
          if (!Number.isNaN(idx)) {
            activeSection.value = idx
          }
        }
      })
    },
    {
      threshold: 0.55,
      rootMargin: '-10% 0px -10% 0px',
    }
  )

  sections.value.forEach((el) => observer.observe(el))

  // 用于触发区块进入动画
  animObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible')
        }
      })
    },
    {
      threshold: 0.35,
      rootMargin: '0px 0px -15% 0px',
    }
  )

  sections.value.forEach((el) => animObserver.observe(el))
})

onUnmounted(() => {
  if (observer) observer.disconnect()
  if (animObserver) animObserver.disconnect()
  document.documentElement.classList.remove('snap-mode')
})

const scrollToSection = (index) => {
  const target = sections.value[index]
  if (target) {
    target.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<template>
  <div class="home">
    <!-- 固定导航 -->
    <header class="nav">
      <div class="container nav-inner">
        <a class="brand" href="#top">
          <svg class="brand-mark" viewBox="0 0 24 24" aria-hidden="true">
            <path
              d="M12 2.5 14.4 9.6 21.5 12 14.4 14.4 12 21.5 9.6 14.4 2.5 12 9.6 9.6Z"
              fill="currentColor"
            />
          </svg>
          <span class="brand-name">香草猫娘</span>
          <small class="brand-tag">Minecraft 魔法服务器</small>
        </a>

        <nav class="nav-links" aria-label="站内导航">
          <a v-for="link in navLinks" :key="link.href" :href="link.href">{{ link.label }}</a>
        </nav>

        <a class="btn btn-primary btn-sm" href="#server">立即游玩</a>
      </div>
    </header>

    <!-- 翻页指示器 -->
    <nav class="page-indicator" aria-label="页面导航">
      <button
        v-for="(label, idx) in sectionLabels"
        :key="idx"
        class="page-indicator__dot"
        :class="{ 'is-active': activeSection === idx }"
        :aria-label="`跳转到第 ${idx + 1} 页：${label}`"
        @click="scrollToSection(idx)"
      >
        <span class="page-indicator__label">{{ label }}</span>
      </button>
    </nav>

    <!-- 翻页滚动容器 -->
    <div class="snap-container">
      <section
        id="top"
        class="section-page hero"
        data-snap-section
        data-section-index="0"
      >
        <div class="hero-bg" :style="{ backgroundImage: `url(${heroImage})` }"></div>
        <div class="hero-overlay"></div>

        <div class="container hero-inner">
          <span class="eyebrow">Minecraft 魔法主题服务器</span>
          <h1>香草猫娘</h1>
          <p class="hero-lead">
            在方块世界里编织你的魔法传说。香草猫娘是以魔法玩法为核心的 Minecraft
            服务器：自定义法术体系、元素派系、遗迹探索与团队副本，等待你书写属于自己的篇章。
          </p>

          <div class="hero-actions">
            <a class="btn btn-primary" href="#server">立即游玩</a>
            <a class="btn btn-ghost" href="#features">了解玩法</a>
          </div>

          <ul class="hero-stats">
            <li v-for="item in stats" :key="item.label">
              <strong>{{ item.value }}</strong>
              <span>{{ item.label }}</span>
            </li>
          </ul>
        </div>
      </section>

      <section
        id="features"
        class="section-page section"
        data-snap-section
        data-section-index="1"
      >
        <div class="container">
          <header class="section-head">
            <span class="eyebrow">玩法特色</span>
            <h2>以魔法为核心的方块世界</h2>
            <p class="section-desc">
              从第一次点燃法力水晶，到掌握禁咒与元素共鸣，香草猫娘为你准备了完整的魔法成长体验。
            </p>
          </header>

          <div class="feature-grid">
            <article v-for="feature in features" :key="feature.title" class="feature-card">
              <div class="feature-icon">
                <svg
                  v-if="feature.icon === 'book'"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.6"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  aria-hidden="true"
                >
                  <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H19v15H6.5A2.5 2.5 0 0 0 4 20.5Z" />
                  <path d="M4 20.5A2.5 2.5 0 0 1 6.5 18H19v3H6.5" />
                  <path d="M12 7 12.9 9.6 15.5 10.5 12.9 11.4 12 14 11.1 11.4 8.5 10.5 11.1 9.6Z" />
                </svg>
                <svg
                  v-else-if="feature.icon === 'flame'"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.6"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  aria-hidden="true"
                >
                  <path d="M12 3.5c2.8 3.3 4.8 5.7 4.8 8.6a4.8 4.8 0 0 1-9.6 0c0-2.9 2-5.3 4.8-8.6Z" />
                  <path d="M12 20.5a2.9 2.9 0 0 0 2.9-2.9c0-1.5-1-2.7-2.9-4.3-1.9 1.6-2.9 2.8-2.9 4.3A2.9 2.9 0 0 0 12 20.5Z" />
                </svg>
                <svg
                  v-else-if="feature.icon === 'compass'"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.6"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  aria-hidden="true"
                >
                  <circle cx="12" cy="12" r="8.5" />
                  <path d="M14.9 9.1 13 13l-3.9 1.9L11 11Z" />
                </svg>
                <svg
                  v-else
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.6"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  aria-hidden="true"
                >
                  <path d="M12 3.5 19 6v6c0 4-3 6.7-7 8.5-4-1.8-7-4.5-7-8.5V6Z" />
                  <path d="m9.2 12.2 2 2 3.6-3.9" />
                </svg>
              </div>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.desc }}</p>
            </article>
          </div>
        </div>
      </section>

      <section
        id="gameplay"
        class="section-page section section-alt"
        data-snap-section
        data-section-index="2"
      >
        <div class="container gameplay-grid">
          <figure class="gameplay-visual">
            <img :src="gameplayImage" alt="服务器内的魔法师塔：发光书架与地面上的法阵" />
          </figure>

          <div class="gameplay-copy">
            <span class="eyebrow">魔法玩法</span>
            <h2>独特的魔法体系，等你来修行</h2>
            <p class="section-desc">
              香草猫娘围绕魔法重构了战斗与成长体验，让每一次施法、每一场探索都充满仪式感。
            </p>

            <ul class="gameplay-list">
              <li v-for="point in gameplayPoints" :key="point.title">
                <div>
                  <strong>{{ point.title }}</strong>
                  <span>{{ point.desc }}</span>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </section>

      <section
        id="server"
        class="section-page section"
        data-snap-section
        data-section-index="3"
      >
        <div class="container">
          <header class="section-head">
            <span class="eyebrow">服务器信息</span>
            <h2>香草猫娘即将开放</h2>
            <p class="section-desc">服务器正在筹备中，开服时间与连接方式将在本站与社区同步公布。</p>
          </header>

          <div class="server-card">
            <div class="server-address">
              <span class="server-label">服务器地址</span>
              <span class="server-pending">即将推出</span>
            </div>

            <ul class="server-meta">
              <li v-for="item in serverMeta" :key="item.label">
                <span>{{ item.label }}</span>
                <strong>{{ item.value }}</strong>
              </li>
            </ul>

            <p class="server-note">开服前本站会更新服务器地址与进入方式，敬请期待。</p>
          </div>
        </div>
      </section>

      <section
        id="join"
        class="section-page section"
        data-snap-section
        data-section-index="4"
      >
        <div class="container">
          <div class="cta-inner">
            <h2>准备好开始你的魔法之旅了吗？</h2>
            <p class="section-desc">
              无论是初入魔法之门的新人，还是追寻禁咒的资深法师，香草猫娘都为你留好了位置。
            </p>
            <div class="hero-actions">
              <a class="btn btn-primary" href="#features">查看玩法特色</a>
              <a class="btn btn-ghost" href="#gameplay">了解魔法玩法</a>
            </div>
          </div>
        </div>
      </section>

      <footer
        class="footer section-page"
        data-snap-section
        data-section-index="5"
      >
        <div class="container">
          <div class="footer-inner">
            <div class="footer-brand">
              <svg class="brand-mark" viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d="M12 2.5 14.4 9.6 21.5 12 14.4 14.4 12 21.5 9.6 14.4 2.5 12 9.6 9.6Z"
                  fill="currentColor"
                />
              </svg>
              <div>
                <strong>香草猫娘</strong>
                <p>以魔法为核心的 Minecraft 服务器</p>
              </div>
            </div>

            <nav class="footer-links" aria-label="页脚导航">
              <a href="#top">首页</a>
              <a v-for="link in navLinks" :key="link.href" :href="link.href">{{ link.label }}</a>
            </nav>
          </div>

          <div class="footer-bottom">
            <span>© 2026 香草猫娘 · 保留所有权利</span>
            <span>本站为玩家自建服务器，与 Mojang Studios 及 Microsoft 无隶属关系。</span>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<style scoped>
/* ---------- 滚动容器与翻页布局 ---------- */
.home {
  position: relative;
  background: var(--bg-0);
  overflow: hidden;
  height: 100vh;
}

.snap-container {
  height: 100vh;
  overflow-y: auto;
  overflow-x: hidden;
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
  scrollbar-width: thin;
  scrollbar-color: #2a2440 transparent;
}

.section-page {
  scroll-snap-align: start;
  scroll-snap-stop: always;
  min-height: 100vh;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

/* 区块分隔装饰线 */
.section-page::before {
  content: "";
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  max-width: 680px;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(168, 85, 247, 0.28),
    transparent
  );
  pointer-events: none;
}

.section-page:last-child::before {
  display: none;
}

.container {
  width: min(1180px, 100% - 48px);
  margin-inline: auto;
  padding-top: 68px; /* 为固定导航预留空间 */
  padding-bottom: clamp(32px, 5vw, 64px);
}

/* ---------- 翻页指示器 ---------- */
.page-indicator {
  position: fixed;
  right: clamp(16px, 3vw, 36px);
  top: 50%;
  transform: translateY(-50%);
  z-index: 60;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.page-indicator__dot {
  position: relative;
  width: 12px;
  height: 12px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.18);
  cursor: pointer;
  transition:
    background-color 0.3s ease,
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.page-indicator__dot:hover {
  background: rgba(255, 255, 255, 0.45);
}

.page-indicator__dot.is-active {
  background: var(--primary);
  transform: scale(1.4);
  box-shadow: 0 0 16px rgba(168, 85, 247, 0.7);
}

.page-indicator__label {
  position: absolute;
  right: calc(100% + 14px);
  top: 50%;
  transform: translateY(-50%);
  padding: 4px 10px;
  border-radius: 6px;
  background: rgba(6, 6, 11, 0.85);
  border: 1px solid var(--border-soft);
  color: var(--text);
  font-size: 12px;
  letter-spacing: 0.04em;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s ease;
}

.page-indicator__dot:hover .page-indicator__label,
.page-indicator__dot.is-active .page-indicator__label {
  opacity: 1;
}

/* ---------- 导航 ---------- */
.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  background: rgba(6, 6, 11, 0.72);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--border-soft);
}

.nav-inner {
  display: flex;
  align-items: center;
  gap: 32px;
  height: 68px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-mark {
  width: 24px;
  height: 24px;
  color: var(--primary);
  filter: drop-shadow(0 0 10px rgba(168, 85, 247, 0.7));
}

.brand-name {
  font-size: 17px;
  font-weight: 600;
  letter-spacing: 0.06em;
  color: #fff;
}

.brand-tag {
  padding-left: 12px;
  border-left: 1px solid var(--border-soft);
  font-size: 12px;
  font-weight: 400;
  color: var(--text-muted);
  letter-spacing: 0.04em;
}

.nav-links {
  display: flex;
  gap: 28px;
  margin-left: auto;
  font-size: 14px;
  color: var(--text-muted);
}

.nav-links a {
  transition: color 0.2s ease;
}

.nav-links a:hover {
  color: #fff;
}

/* ---------- 按钮 ---------- */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 46px;
  padding: 0 26px;
  border: 1px solid transparent;
  border-radius: 999px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    box-shadow 0.25s ease,
    background-color 0.25s ease,
    border-color 0.25s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #a855f7, #7c3aed);
  color: #fff;
  box-shadow: 0 12px 32px -14px rgba(168, 85, 247, 0.9);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 18px 36px -14px rgba(168, 85, 247, 1);
}

.btn-ghost {
  background: rgba(255, 255, 255, 0.04);
  border-color: var(--border-soft);
  color: var(--text);
}

.btn-ghost:hover {
  background: var(--primary-soft);
  border-color: var(--border);
}

.btn-sm {
  height: 38px;
  padding: 0 20px;
  font-size: 14px;
}

/* ---------- 英雄区 ---------- */
.hero {
  text-align: center;
}

.hero .container {
  padding-top: clamp(88px, 12vw, 120px);
  padding-bottom: clamp(48px, 8vw, 96px);
}

.hero-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  opacity: 0.55;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(70% 60% at 50% 0%, rgba(168, 85, 247, 0.3), transparent 62%),
    linear-gradient(
      180deg,
      rgba(6, 6, 11, 0.55) 0%,
      rgba(6, 6, 11, 0.82) 55%,
      var(--bg-0) 100%
    );
}

.hero::after {
  content: "";
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
  background-size: 64px 64px;
  -webkit-mask-image: radial-gradient(60% 50% at 50% 30%, #000, transparent 78%);
  mask-image: radial-gradient(60% 50% at 50% 30%, #000, transparent 78%);
  pointer-events: none;
}

.hero-inner {
  position: relative;
  z-index: 1;
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  padding: 7px 16px;
  border: 1px solid var(--border);
  border-radius: 999px;
  background: var(--primary-soft);
  color: #dcc9ff;
  font-size: 13px;
  letter-spacing: 0.1em;
}

.hero h1 {
  margin: 26px 0 22px;
  font-size: clamp(44px, 7vw, 78px);
  font-weight: 700;
  letter-spacing: 0.08em;
  background: linear-gradient(180deg, #ffffff, #c9b4f5);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  filter: drop-shadow(0 0 32px rgba(168, 85, 247, 0.45));
}

.hero-lead {
  max-width: 660px;
  margin-inline: auto;
  color: var(--text-muted);
  font-size: clamp(15px, 1.3vw, 17px);
  line-height: 1.9;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 14px;
  margin-top: 36px;
}

.hero-stats {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: clamp(24px, 4vw, 60px);
  margin: clamp(40px, 5vw, 56px) 0 0;
  padding: 0;
  list-style: none;
}

.hero-stats li {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.hero-stats strong {
  color: #fff;
  font-size: clamp(17px, 1.6vw, 20px);
  font-weight: 600;
}

.hero-stats span {
  color: var(--text-muted);
  font-size: 13px;
  letter-spacing: 0.08em;
}

/* ---------- 通用区块 ---------- */
.section {
  padding-top: clamp(32px, 5vw, 48px);
  padding-bottom: clamp(32px, 5vw, 48px);
}

.section-alt {
  background: linear-gradient(
    180deg,
    transparent,
    rgba(168, 85, 247, 0.06) 30%,
    rgba(168, 85, 247, 0.06) 70%,
    transparent
  );
}

.section-head {
  max-width: 720px;
  margin: 0 auto clamp(32px, 4vw, 56px);
  text-align: center;
}

.section-head h2,
.gameplay-copy h2,
.cta-inner h2 {
  margin: 22px 0 16px;
  color: #fff;
  font-size: clamp(26px, 3.2vw, 38px);
  font-weight: 650;
  letter-spacing: 0.02em;
}

.section-desc {
  color: var(--text-muted);
  font-size: 15.5px;
  line-height: 1.9;
}

/* ---------- 玩法特色 ---------- */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.feature-card {
  padding: 28px 24px;
  border: 1px solid var(--border-soft);
  border-radius: 18px;
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0.05),
    rgba(255, 255, 255, 0.015)
  );
  transition:
    transform 0.3s ease,
    border-color 0.3s ease,
    box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-6px);
  border-color: var(--border);
  box-shadow: 0 26px 54px -32px rgba(168, 85, 247, 0.95);
}

.feature-icon {
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--primary-soft);
  color: #d8b4fe;
}

.feature-icon svg {
  width: 22px;
  height: 22px;
}

.feature-card h3 {
  margin: 20px 0 10px;
  color: #fff;
  font-size: 17px;
  font-weight: 600;
}

.feature-card p {
  color: var(--text-muted);
  font-size: 14.5px;
  line-height: 1.8;
}

/* ---------- 魔法玩法 ---------- */
.gameplay-grid {
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  gap: clamp(32px, 5vw, 64px);
  align-items: center;
}

.gameplay-visual {
  position: relative;
  overflow: hidden;
  border: 1px solid var(--border);
  border-radius: 22px;
  box-shadow: 0 44px 84px -44px rgba(0, 0, 0, 0.95);
}

.gameplay-visual img {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
}

.gameplay-visual::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, transparent 45%, rgba(6, 6, 11, 0.55));
  pointer-events: none;
}

.gameplay-list {
  display: grid;
  gap: 18px;
  margin: 30px 0 0;
  padding: 0;
  list-style: none;
}

.gameplay-list li {
  display: grid;
  grid-template-columns: 12px 1fr;
  gap: 14px;
}

.gameplay-list li::before {
  content: "";
  width: 10px;
  height: 10px;
  margin-top: 8px;
  background: linear-gradient(135deg, #c084fc, #7c3aed);
  clip-path: polygon(
    50% 0,
    62% 38%,
    100% 50%,
    62% 62%,
    50% 100%,
    38% 62%,
    0 50%,
    38% 38%
  );
  box-shadow: 0 0 12px rgba(168, 85, 247, 0.85);
}

.gameplay-list strong {
  display: block;
  margin-bottom: 5px;
  color: #fff;
  font-size: 15.5px;
  font-weight: 600;
}

.gameplay-list span {
  color: var(--text-muted);
  font-size: 14.5px;
  line-height: 1.8;
}

/* ---------- 服务器信息 ---------- */
.server-card {
  display: grid;
  gap: 28px;
  padding: clamp(28px, 4vw, 44px);
  border: 1px solid var(--border);
  border-radius: 24px;
  background:
    radial-gradient(120% 140% at 0% 0%, rgba(168, 85, 247, 0.18), transparent 55%),
    rgba(255, 255, 255, 0.025);
}

.server-address {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 14px 20px;
  padding-bottom: 26px;
  border-bottom: 1px solid var(--border-soft);
}

.server-label {
  color: var(--text-muted);
  font-size: 14px;
  letter-spacing: 0.06em;
}

.server-pending {
  padding: 6px 20px;
  border: 1px dashed var(--border);
  border-radius: 999px;
  background: var(--primary-soft);
  color: #dcc9ff;
  font-size: clamp(16px, 2vw, 21px);
  letter-spacing: 0.16em;
}

.server-meta {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.server-meta li {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.server-meta span {
  color: var(--text-muted);
  font-size: 13px;
  letter-spacing: 0.06em;
}

.server-meta strong {
  color: #fff;
  font-size: 16px;
  font-weight: 600;
}

.server-note {
  color: var(--text-muted);
  font-size: 14px;
}

/* ---------- 行动号召 ---------- */
.cta-inner {
  padding: clamp(48px, 7vw, 80px) clamp(24px, 4vw, 60px);
  border: 1px solid var(--border);
  border-radius: 28px;
  text-align: center;
  background:
    radial-gradient(90% 120% at 50% 0%, rgba(168, 85, 247, 0.24), transparent 62%),
    rgba(255, 255, 255, 0.02);
}

.cta-inner .section-desc {
  max-width: 580px;
  margin-inline: auto;
}

/* ---------- 页脚 ---------- */
.footer {
  min-height: 100vh;
  padding: 0;
  border-top: none;
  background: #05050a;
}

.footer .container {
  padding-top: clamp(64px, 8vw, 96px);
  padding-bottom: clamp(40px, 5vw, 72px);
  margin-top: auto;
  margin-bottom: auto;
}

.footer-inner {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 36px;
  align-items: start;
}

.footer-brand {
  display: flex;
  gap: 12px;
}

.footer-brand strong {
  display: block;
  color: #fff;
  font-size: 16px;
  letter-spacing: 0.06em;
}

.footer-brand p {
  margin-top: 6px;
  color: var(--text-muted);
  font-size: 14px;
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 12px 26px;
  font-size: 14px;
  color: var(--text-muted);
}

.footer-links a {
  transition: color 0.2s ease;
}

.footer-links a:hover {
  color: #fff;
}

.footer-bottom {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 10px;
  margin-top: 40px;
  padding-top: 22px;
  border-top: 1px solid var(--border-soft);
  color: var(--text-muted);
  font-size: 13px;
}

/* ---------- 翻页进入动画 ---------- */
.section-page {
  opacity: 0;
  transform: translateY(40px) scale(0.98);
  transition:
    opacity 0.5s cubic-bezier(0.22, 1, 0.36, 1),
    transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}

/* JS 未就绪时，所有区块直接可见（无动画） */
.snap-container:not(.anim-ready) .section-page {
  opacity: 1;
  transform: none;
}

/* JS 就绪后，通过 is-visible 类触发翻页动画 */
.snap-container.anim-ready .section-page.is-visible {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* 各 section 内子元素的错峰进入动画 */
.snap-container.anim-ready .section-page.is-visible .feature-card,
.snap-container.anim-ready .section-page.is-visible .gameplay-list li,
.snap-container.anim-ready .section-page.is-visible .server-meta li {
  opacity: 0;
  animation: flipInUp 0.5s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

.snap-container.anim-ready .section-page.is-visible .feature-card:nth-child(1),
.snap-container.anim-ready .section-page.is-visible .gameplay-list li:nth-child(1),
.snap-container.anim-ready .section-page.is-visible .server-meta li:nth-child(1) { animation-delay: 0.1s; }

.snap-container.anim-ready .section-page.is-visible .feature-card:nth-child(2),
.snap-container.anim-ready .section-page.is-visible .gameplay-list li:nth-child(2),
.snap-container.anim-ready .section-page.is-visible .server-meta li:nth-child(2) { animation-delay: 0.2s; }

.snap-container.anim-ready .section-page.is-visible .feature-card:nth-child(3),
.snap-container.anim-ready .section-page.is-visible .gameplay-list li:nth-child(3),
.snap-container.anim-ready .section-page.is-visible .server-meta li:nth-child(3) { animation-delay: 0.3s; }

.snap-container.anim-ready .section-page.is-visible .feature-card:nth-child(4) { animation-delay: 0.4s; }

@keyframes flipInUp {
  from {
    opacity: 0;
    transform: perspective(600px) rotateX(12deg) translateY(24px);
  }
  to {
    opacity: 1;
    transform: perspective(600px) rotateX(0) translateY(0);
  }
}

/* Hero 特有动画 */
.snap-container.anim-ready .hero.is-visible .eyebrow {
  animation: fadeSlideDown 0.6s cubic-bezier(0.22, 1, 0.36, 1) 0.1s both;
}
.snap-container.anim-ready .hero.is-visible h1 {
  animation: fadeSlideDown 0.7s cubic-bezier(0.22, 1, 0.36, 1) 0.25s both;
}
.snap-container.anim-ready .hero.is-visible .hero-lead {
  animation: fadeSlideDown 0.6s cubic-bezier(0.22, 1, 0.36, 1) 0.4s both;
}
.snap-container.anim-ready .hero.is-visible .hero-actions {
  animation: fadeSlideDown 0.6s cubic-bezier(0.22, 1, 0.36, 1) 0.55s both;
}
.snap-container.anim-ready .hero.is-visible .hero-stats {
  animation: fadeSlideDown 0.6s cubic-bezier(0.22, 1, 0.36, 1) 0.7s both;
}

@keyframes fadeSlideDown {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ---------- prefers-reduced-motion ---------- */
@media (prefers-reduced-motion: reduce) {
  .snap-container {
    scroll-snap-type: none;
    scroll-behavior: auto;
  }

  .section-page {
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
    min-height: auto;
  }

  .page-indicator {
    display: none;
  }

  .feature-card,
  .gameplay-list li,
  .server-meta li {
    animation: none !important;
    opacity: 1 !important;
  }
}

/* ---------- 响应式 ---------- */
@media (min-width: 640px) {
  .hero-stats li + li {
    padding-left: clamp(24px, 4vw, 60px);
    border-left: 1px solid var(--border-soft);
  }
}

@media (max-width: 1024px) {
  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 900px) {
  .gameplay-grid {
    grid-template-columns: 1fr;
  }

  .brand-tag {
    display: none;
  }
}

@media (max-width: 860px) {
  .nav-links {
    display: none;
  }

  .nav-inner {
    justify-content: space-between;
  }

  .page-indicator {
    right: 10px;
    gap: 10px;
  }

  .page-indicator__dot {
    width: 10px;
    height: 10px;
  }

  .page-indicator__label {
    display: none;
  }
}

@media (max-width: 760px) {
  .server-meta {
    grid-template-columns: 1fr;
  }

  .footer-inner {
    grid-template-columns: 1fr;
  }

  .footer-links {
    justify-content: flex-start;
  }
}

@media (max-width: 600px) {
  .container {
    width: min(1180px, 100% - 32px);
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }

  .snap-container {
    scroll-snap-type: y proximity;
  }

  .section-page {
    min-height: 100vh;
    height: auto;
    overflow: visible;
  }
}
</style>
