<script setup>
import { ref, onMounted } from 'vue'
import { produtosApi } from '../api'

const emit = defineEmits(['adicionado'])

const props = defineProps({
  produto: { type: Object, required: true },
})

const quantidade = ref(1)
const loading = ref(false)
const msg = ref(null)

async function adicionar() {
  loading.value = true
  msg.value = null
  try {
    await emit('adicionado', props.produto.codigo, quantidade.value)
    quantidade.value = 1
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="produto-card" :class="{ esgotado: produto.quantidade === 0 }">
    <div class="produto-nome">{{ produto.nome }}</div>
    <div class="produto-preco">R$ {{ produto.preco.toFixed(2) }}</div>
    <div class="produto-estoque">
      <span :class="produto.quantidade > 0 ? 'badge-green' : 'badge-red'" class="badge">
        Estoque: {{ produto.quantidade }}
      </span>
    </div>
    <div class="produto-actions">
      <input
        v-model.number="quantidade"
        type="number"
        min="1"
        :max="produto.quantidade"
        class="qty-input"
        :disabled="produto.quantidade === 0"
      />
      <button
        class="btn btn-primary btn-sm"
        :disabled="produto.quantidade === 0 || loading"
        @click="adicionar"
      >
        + Adicionar
      </button>
    </div>
  </div>
</template>

<style scoped>
.produto-card {
  background: #fff;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  transition: box-shadow 0.2s;
}
.produto-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.12); }
.produto-card.esgotado { opacity: 0.55; }

.produto-nome { font-weight: 700; font-size: 1rem; color: #1a2e1e; }
.produto-preco { font-size: 1.15rem; color: #2d6a4f; font-weight: 700; }
.produto-actions { display: flex; gap: 0.5rem; align-items: center; }
.qty-input { width: 60px; }
</style>
