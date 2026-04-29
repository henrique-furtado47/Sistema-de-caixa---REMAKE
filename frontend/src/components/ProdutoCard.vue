<script setup>
import { computed, ref } from 'vue'

const emit = defineEmits(['adicionado'])

const props = defineProps({
  produto: { type: Object, required: true },
})

const quantidade = ref(1)
const loading = ref(false)

const esgotado = computed(() => props.produto.quantidade === 0)
const maxQtd = computed(() => props.produto.quantidade)

function decrement() { if (quantidade.value > 1) quantidade.value-- }
function increment() { if (quantidade.value < maxQtd.value) quantidade.value++ }

// First letter(s) for the avatar
const avatar = computed(() => {
  const words = props.produto.nome.trim().split(' ')
  return words.length >= 2
    ? words[0][0].toUpperCase() + words[1][0].toUpperCase()
    : words[0].slice(0, 2).toUpperCase()
})

// Deterministic color from name
const avatarHue = computed(() => {
  let hash = 0
  for (const c of props.produto.nome) hash = c.charCodeAt(0) + ((hash << 5) - hash)
  return ((hash % 60) + 60) % 60 + 100 // hue 100-160 (greens)
})

async function adicionar() {
  if (esgotado.value || loading.value) return
  loading.value = true
  try {
    await emit('adicionado', props.produto.codigo, quantidade.value)
    quantidade.value = 1
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="p-card" :class="{ esgotado }">
    <!-- Avatar -->
    <div class="p-avatar" :style="{ background: `hsl(${avatarHue}, 48%, 86%)`, color: `hsl(${avatarHue}, 48%, 28%)` }">
      {{ avatar }}
    </div>

    <!-- Info -->
    <div class="p-info">
      <div class="p-nome" :title="produto.nome">{{ produto.nome }}</div>
      <div class="p-code">#{{ produto.codigo }}</div>
    </div>

    <!-- Price -->
    <div class="p-preco">R$&nbsp;{{ produto.preco.toFixed(2) }}</div>

    <!-- Stock -->
    <div class="p-stock">
      <span v-if="esgotado" class="badge badge-red">Esgotado</span>
      <span v-else-if="produto.quantidade <= 5" class="badge badge-yellow">
        ⚠️ {{ produto.quantidade }} restantes
      </span>
      <span v-else class="badge badge-green">
        {{ produto.quantidade }} em estoque
      </span>
    </div>

    <!-- Actions -->
    <div class="p-actions">
      <div class="stepper">
        <button class="stepper-btn" @click="decrement" :disabled="esgotado || quantidade <= 1">−</button>
        <span class="stepper-value">{{ quantidade }}</span>
        <button class="stepper-btn" @click="increment" :disabled="esgotado || quantidade >= maxQtd">+</button>
      </div>
      <button
        class="btn btn-primary btn-sm add-btn"
        :disabled="esgotado || loading"
        @click="adicionar"
      >
        <span v-if="loading" class="spinner" style="width:14px;height:14px;border-width:2px"></span>
        <span v-else>Adicionar</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.p-card {
  background: var(--surface);
  border-radius: var(--radius-lg);
  padding: 1.1rem;
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  transition: box-shadow 0.18s, transform 0.18s, border-color 0.18s;
  cursor: default;
  position: relative;
  overflow: hidden;
}
.p-card::before {
  content: '';
  position: absolute;
  inset: 0 0 auto 0;
  height: 3px;
  background: linear-gradient(90deg, var(--c-600), var(--c-400));
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  opacity: 0;
  transition: opacity 0.18s;
}
.p-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); border-color: var(--c-200); }
.p-card:hover::before { opacity: 1; }
.p-card.esgotado { opacity: 0.5; pointer-events: none; }

.p-avatar {
  width: 44px; height: 44px;
  border-radius: var(--radius-md);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.9rem;
  font-weight: 800;
  letter-spacing: -0.5px;
  flex-shrink: 0;
  align-self: flex-start;
}

.p-info { flex: 1; }
.p-nome {
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--text-primary);
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.p-code { font-size: 0.72rem; color: var(--text-muted); margin-top: 0.15rem; font-weight: 500; }

.p-preco {
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--c-700);
  letter-spacing: -0.5px;
}

.p-stock {}

.p-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.1rem;
}
.add-btn { flex: 1; font-size: 0.8rem; }
</style>
