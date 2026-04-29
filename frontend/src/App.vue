<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'

const route = useRoute()
const mobileOpen = ref(false)
</script>

<template>
  <div id="app-root">
    <!-- Navbar -->
    <header class="navbar">
      <div class="nav-inner">
        <!-- Brand -->
        <RouterLink to="/caixa" class="brand">
          <div class="brand-logo">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
            </svg>
          </div>
          <div class="brand-text">
            <span class="brand-name">Sistema de Caixa</span>
            <span class="brand-sub">PDV</span>
          </div>
        </RouterLink>

        <!-- Desktop nav -->
        <nav class="nav-links desktop-only">
          <RouterLink to="/caixa" :class="['nav-link', { active: route.path === '/caixa' }]">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
            </svg>
            Caixa
          </RouterLink>
          <RouterLink to="/estoque" :class="['nav-link', { active: route.path === '/estoque' }]">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
              <line x1="12" y1="22.08" x2="12" y2="12"/>
            </svg>
            Estoque
          </RouterLink>
        </nav>

        <!-- Mobile burger -->
        <button class="burger mobile-only" @click="mobileOpen = !mobileOpen" :aria-expanded="mobileOpen">
          <span :class="['burger-line', { open: mobileOpen }]"></span>
          <span :class="['burger-line', { open: mobileOpen }]"></span>
          <span :class="['burger-line', { open: mobileOpen }]"></span>
        </button>
      </div>

      <!-- Mobile menu -->
      <Transition name="slide">
        <nav v-if="mobileOpen" class="mobile-menu" @click="mobileOpen = false">
          <RouterLink to="/caixa" :class="['nav-link', { active: route.path === '/caixa' }]">
            🛒 Caixa
          </RouterLink>
          <RouterLink to="/estoque" :class="['nav-link', { active: route.path === '/estoque' }]">
            📦 Estoque
          </RouterLink>
        </nav>
      </Transition>
    </header>

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
#app-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg);
}

/* Navbar */
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--c-800);
  background: linear-gradient(135deg, var(--c-900) 0%, var(--c-800) 100%);
  box-shadow: 0 2px 16px rgba(0,0,0,0.3);
}
.nav-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1.5rem;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

/* Brand */
.brand {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  text-decoration: none;
  flex-shrink: 0;
}
.brand-logo {
  width: 36px; height: 36px;
  background: rgba(255,255,255,0.12);
  border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
  transition: background 0.2s;
}
.brand:hover .brand-logo { background: rgba(255,255,255,0.2); }
.brand-text { display: flex; flex-direction: column; line-height: 1.15; }
.brand-name { font-size: 0.95rem; font-weight: 800; color: #fff; letter-spacing: -0.2px; }
.brand-sub  { font-size: 0.65rem; color: var(--c-300); font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; }

/* Nav links */
.nav-links { display: flex; gap: 0.25rem; }
.nav-link {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.45rem 0.9rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--c-300);
  text-decoration: none;
  transition: background 0.18s, color 0.18s;
}
.nav-link:hover { background: rgba(255,255,255,0.1); color: #fff; }
.nav-link.active { background: rgba(255,255,255,0.16); color: #fff; }

/* Burger */
.burger {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 36px; height: 36px;
  padding: 0;
  background: transparent;
  border: none;
  cursor: pointer;
  border-radius: 8px;
}
.burger-line {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--c-300);
  border-radius: 2px;
  transition: all 0.25s ease;
  transform-origin: center;
}
.burger-line.open:nth-child(1) { transform: translateY(7px) rotate(45deg); background: #fff; }
.burger-line.open:nth-child(2) { opacity: 0; }
.burger-line.open:nth-child(3) { transform: translateY(-7px) rotate(-45deg); background: #fff; }

/* Mobile menu */
.mobile-menu {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.75rem 1rem;
  border-top: 1px solid rgba(255,255,255,0.08);
  background: var(--c-900);
}
.mobile-menu .nav-link { font-size: 0.95rem; padding: 0.7rem 1rem; }

/* Transition */
.slide-enter-active, .slide-leave-active { transition: all 0.2s ease; }
.slide-enter-from, .slide-leave-to { opacity: 0; transform: translateY(-8px); }

/* Helpers */
.desktop-only { display: flex; }
.mobile-only  { display: none; }

@media (max-width: 640px) {
  .desktop-only { display: none; }
  .mobile-only  { display: flex; }
}

/* Main content */
.main-content {
  flex: 1;
  padding: 1.75rem 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

@media (max-width: 640px) {
  .main-content { padding: 1rem; }
}
</style>
