<script setup>
import { computed, onMounted, ref } from 'vue'
import { carrinhoApi, produtosApi } from '../api'
import CarrinhoSidebar from '../components/CarrinhoSidebar.vue'
import ProdutoCard from '../components/ProdutoCard.vue'

const produtos = ref([])
const carrinho = ref({ itens: [], total: 0, quantidade_total: 0, vazio: true })
const busca = ref('')
const loading = ref(false)
const alertMsg = ref(null)

const produtosFiltrados = computed(() =>
  produtos.value.filter(p =>
    p.nome.toLowerCase().includes(busca.value.toLowerCase())
  )
)

async function carregarProdutos() {
  loading.value = true
  try {
    const { data } = await produtosApi.listar()
    produtos.value = data
  } catch (e) {
    alertMsg.value = { tipo: 'error', texto: 'Erro ao carregar produtos.' }
  } finally {
    loading.value = false
  }
}

async function carregarCarrinho() {
  try {
    const { data } = await carrinhoApi.ver()
    carrinho.value = data
  } catch (e) {
    console.error(e)
  }
}

async function handleAdicionar(codigo, quantidade) {
  alertMsg.value = null
  try {
    const { data } = await carrinhoApi.adicionar(codigo, quantidade)
    carrinho.value = data
    await carregarProdutos()
    alertMsg.value = { tipo: 'success', texto: 'Produto adicionado ao carrinho!' }
    setTimeout(() => (alertMsg.value = null), 2500)
  } catch (e) {
    alertMsg.value = { tipo: 'error', texto: e.response?.data?.detail || 'Erro ao adicionar.' }
  }
}

function handleCarrinhoAtualizado(novoCarrinho) {
  carrinho.value = novoCarrinho
  carregarProdutos()
}

onMounted(() => {
  carregarProdutos()
  carregarCarrinho()
})
</script>

<template>
  <div class="caixa-layout">
    <!-- Products panel -->
    <section class="produtos-section">
      <!-- Page header -->
      <div class="page-header">
        <div>
          <h2 class="page-title">Ponto de Venda</h2>
          <p class="page-sub">{{ produtos.length }} produto(s) disponível(is)</p>
        </div>
        <button class="btn btn-ghost btn-sm" @click="carregarProdutos" title="Atualizar">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M23 4v6h-6"/><path d="M1 20v-6h6"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
          </svg>
          Atualizar
        </button>
      </div>

      <!-- Search bar -->
      <div class="search-bar">
        <div class="input-group">
          <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input
            v-model="busca"
            class="form-control search-input"
            placeholder="Buscar produto por nome..."
          />
          <button v-if="busca" class="search-clear" @click="busca = ''">✕</button>
        </div>
        <div class="results-count" v-if="busca">
          {{ produtosFiltrados.length }} resultado(s)
        </div>
      </div>

      <!-- Alert -->
      <Transition name="alert-slide">
        <div v-if="alertMsg" :class="`alert alert-${alertMsg.tipo === 'success' ? 'success' : 'error'}`">
          <span>{{ alertMsg.tipo === 'success' ? '✓' : '✕' }}</span>
          {{ alertMsg.texto }}
        </div>
      </Transition>

      <!-- Loading -->
      <div v-if="loading" class="loading-grid">
        <div v-for="i in 8" :key="i" class="skeleton-card"></div>
      </div>

      <!-- Empty state -->
      <div v-else-if="produtosFiltrados.length === 0" class="empty-state">
        <div class="empty-state-icon">{{ busca ? '🔍' : '📦' }}</div>
        <p>{{ busca ? `Nenhum resultado para "${busca}"` : 'Nenhum produto cadastrado' }}</p>
        <p style="font-size:0.8rem;opacity:0.6">{{ busca ? 'Tente outro termo' : 'Vá para Estoque para cadastrar produtos' }}</p>
      </div>

      <!-- Grid -->
      <div v-else class="produtos-grid">
        <ProdutoCard
          v-for="p in produtosFiltrados"
          :key="p.codigo"
          :produto="p"
          @adicionado="handleAdicionar"
        />
      </div>
    </section>

    <!-- Cart panel -->
    <aside class="cart-column">
      <CarrinhoSidebar :carrinho="carrinho" @atualizado="handleCarrinhoAtualizado" />
    </aside>
  </div>
</template>

<style scoped>
.caixa-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 1.5rem;
  align-items: start;
}

/* Page header */
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 1.25rem;
  gap: 1rem;
}
.page-title { color: var(--c-800); font-size: 1.4rem; }
.page-sub { font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem; }

/* Search */
.search-bar { margin-bottom: 1rem; }
.search-input { border-radius: var(--radius-md); padding-right: 2.5rem; }
.search-clear {
  position: absolute;
  right: 0.75rem;
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 0.8rem;
  padding: 0.25rem;
  border-radius: 4px;
}
.search-clear:hover { color: var(--danger); }
.results-count { font-size: 0.75rem; color: var(--text-muted); margin-top: 0.4rem; padding-left: 0.2rem; }

/* Alert */
.alert-slide-enter-active, .alert-slide-leave-active { transition: all 0.2s ease; }
.alert-slide-enter-from, .alert-slide-leave-to { opacity: 0; transform: translateY(-6px); }

/* Skeleton loading */
.loading-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
  gap: 1rem;
}
.skeleton-card {
  height: 180px;
  background: linear-gradient(90deg, var(--border) 25%, #eef2ee 50%, var(--border) 75%);
  background-size: 200% 100%;
  border-radius: var(--radius-lg);
  animation: shimmer 1.4s infinite;
}
@keyframes shimmer { to { background-position: -200% 0; } }

/* Products grid */
.produtos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
  gap: 1rem;
}

/* Cart column */
.cart-column { position: sticky; top: 76px; }

@media (max-width: 900px) {
  .caixa-layout {
    grid-template-columns: 1fr;
  }
  .cart-column {
    order: -1;
    position: static;
  }
}
</style>
