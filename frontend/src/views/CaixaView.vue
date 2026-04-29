<script setup>
import { ref, onMounted, computed } from 'vue'
import { produtosApi, carrinhoApi } from '../api'
import ProdutoCard from '../components/ProdutoCard.vue'
import CarrinhoSidebar from '../components/CarrinhoSidebar.vue'

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
  try {
    const { data } = await produtosApi.listar()
    produtos.value = data
  } catch (e) {
    alertMsg.value = { tipo: 'error', texto: 'Erro ao carregar produtos.' }
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
    <!-- Painel produtos -->
    <section class="produtos-section">
      <div class="section-header">
        <h2>🏷️ Produtos</h2>
        <input v-model="busca" placeholder="Buscar produto..." class="busca-input" />
      </div>

      <div v-if="alertMsg" :class="`alert alert-${alertMsg.tipo === 'success' ? 'success' : 'error'}`">
        {{ alertMsg.texto }}
      </div>

      <div v-if="produtosFiltrados.length === 0" class="empty-msg">
        Nenhum produto encontrado.
      </div>

      <div class="produtos-grid">
        <ProdutoCard
          v-for="p in produtosFiltrados"
          :key="p.codigo"
          :produto="p"
          @adicionado="handleAdicionar"
        />
      </div>
    </section>

    <!-- Painel carrinho -->
    <aside class="carrinho-section">
      <CarrinhoSidebar :carrinho="carrinho" @atualizado="handleCarrinhoAtualizado" />
    </aside>
  </div>
</template>

<style scoped>
.caixa-layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 1.5rem;
  align-items: start;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  gap: 1rem;
  flex-wrap: wrap;
}
.section-header h2 { color: #1b4332; }
.busca-input { max-width: 240px; }

.produtos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
  gap: 1rem;
}

.empty-msg { color: #888; padding: 2rem 0; text-align: center; }

@media (max-width: 768px) {
  .caixa-layout { grid-template-columns: 1fr; }
  .carrinho-section { order: -1; }
}
</style>
