<script setup>
import { RouterLink, RouterView, useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <div id="app-root">
    <nav class="navbar">
      <div class="navbar-brand">
        <span class="brand-icon">🛒</span>
        <span class="brand-name">Sistema de Caixa</span>
      </div>
      <div class="navbar-links">
        <RouterLink to="/caixa" :class="{ active: route.path === '/caixa' }">
          🛒 Caixa
        </RouterLink>
        <RouterLink to="/estoque" :class="{ active: route.path === '/estoque' }">
          📦 Estoque
        </RouterLink>
      </div>
    </nav>
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
  background: #ecf0ea;
}
.navbar {
  background: #1b4332;
  color: #c8e6cd;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.navbar-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: #fff;
}
.brand-icon { font-size: 1.5rem; }
.navbar-links {
  display: flex;
  gap: 0.5rem;
}
.navbar-links a {
  color: #b7dbc0;
  text-decoration: none;
  padding: 0.4rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  transition: background 0.2s;
}
.navbar-links a:hover,
.navbar-links a.active {
  background: rgba(255,255,255,0.18);
  color: #fff;
}
.main-content {
  flex: 1;
  padding: 1.5rem 2rem;
}
</style>
