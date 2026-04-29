<script setup>
import { computed, onMounted, ref } from 'vue'
import { produtosApi } from '../api'

const produtos = ref([])
const loading = ref(false)
const alertMsg = ref(null)
const showForm = ref(false)
const buscaTabela = ref('')

// Form novo produto
const novoNome = ref('')
const novaQtd = ref(0)
const novoPreco = ref(0)

// EdiÃ§Ã£o
const editando = ref(null) // { codigo, nome, quantidade, preco }

const produtosFiltrados = computed(() => {
  if (!buscaTabela.value.trim()) return produtos.value
  const q = buscaTabela.value.toLowerCase()
  return produtos.value.filter(p => p.nome.toLowerCase().includes(q) || String(p.codigo).includes(q))
})

const totalUnidades = computed(() => produtos.value.reduce((s, p) => s + p.quantidade, 0))
const baixoEstoque = computed(() => produtos.value.filter(p => p.quantidade <= 5).length)

async function carregar() {
  loading.value = true
  try {
    const { data } = await produtosApi.listar()
    produtos.value = data
  } catch (e) {
    alertMsg.value = { tipo: 'error', texto: 'Erro ao carregar estoque.' }
  } finally {
    loading.value = false
  }
}

async function cadastrar() {
  alertMsg.value = null
  if (!novoNome.value.trim()) {
    alertMsg.value = { tipo: 'error', texto: 'Nome Ã© obrigatÃ³rio.' }
    return
  }
  try {
    await produtosApi.cadastrar({
      nome: novoNome.value.trim(),
      quantidade: novaQtd.value,
      preco: novoPreco.value,
    })
    novoNome.value = ''
    novaQtd.value = 0
    novoPreco.value = 0
    alertMsg.value = { tipo: 'success', texto: 'Produto cadastrado com sucesso!' }
    await carregar()
  } catch (e) {
    alertMsg.value = { tipo: 'error', texto: e.response?.data?.detail || 'Erro ao cadastrar.' }
  }
}

function abrirEdicao(produto) {
  editando.value = { ...produto }
}

async function salvarEdicao() {
  alertMsg.value = null
  try {
    await produtosApi.atualizar(editando.value.codigo, {
      nome: editando.value.nome,
      quantidade: editando.value.quantidade,
      preco: editando.value.preco,
    })
    editando.value = null
    alertMsg.value = { tipo: 'success', texto: 'Produto atualizado!' }
    await carregar()
  } catch (e) {
    alertMsg.value = { tipo: 'error', texto: e.response?.data?.detail || 'Erro ao atualizar.' }
  }
}

async function remover(codigo) {
  if (!confirm('Remover este produto do estoque?')) return
  alertMsg.value = null
  try {
    await produtosApi.remover(codigo)
    alertMsg.value = { tipo: 'success', texto: 'Produto removido.' }
    await carregar()
  } catch (e) {
    alertMsg.value = { tipo: 'error', texto: e.response?.data?.detail || 'Erro ao remover.' }
  }
}

function fmt(v) { return `R$ ${Number(v).toFixed(2)}` }

onMounted(carregar)
</script>

<template>
  <div class="estoque-page">

    <!-- Page header -->
    <div class="page-header">
      <div>
        <h2 class="page-title">Gerenciar Estoque</h2>
        <p class="page-sub">Controle de produtos e quantidades</p>
      </div>
      <button class="btn btn-primary" @click="showForm = !showForm">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Novo Produto
      </button>
    </div>

    <!-- Stats row -->
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-icon green">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>
          </svg>
        </div>
        <div>
          <div class="stat-value">{{ produtos.length }}</div>
          <div class="stat-label">Produtos</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon blue">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
          </svg>
        </div>
        <div>
          <div class="stat-value">{{ totalUnidades }}</div>
          <div class="stat-label">Unidades em estoque</div>
        </div>
      </div>
      <div class="stat-card" :class="{ 'stat-card--warn': baixoEstoque > 0 }">
        <div class="stat-icon" :class="baixoEstoque > 0 ? 'orange' : 'gray'">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
        </div>
        <div>
          <div class="stat-value">{{ baixoEstoque }}</div>
          <div class="stat-label">Estoque baixo (â‰¤ 5)</div>
        </div>
      </div>
    </div>

    <!-- Alert -->
    <Transition name="alert-slide">
      <div v-if="alertMsg" :class="`alert alert-${alertMsg.tipo === 'success' ? 'success' : 'error'}`">
        <span>{{ alertMsg.tipo === 'success' ? 'âœ“' : 'âœ•' }}</span>
        {{ alertMsg.texto }}
      </div>
    </Transition>

    <!-- Add product panel -->
    <Transition name="form-slide">
      <div v-if="showForm" class="card form-card">
        <div class="form-card-header">
          <h3>Novo Produto</h3>
          <button class="btn btn-icon" @click="showForm = false" title="Fechar">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Nome do produto</label>
            <input v-model="novoNome" class="form-control" placeholder="Ex: Coca-Cola 350ml" />
          </div>
          <div class="form-group">
            <label class="form-label">Quantidade inicial</label>
            <input v-model.number="novaQtd" class="form-control" type="number" min="0" />
          </div>
          <div class="form-group">
            <label class="form-label">PreÃ§o (R$)</label>
            <div class="input-group">
              <span class="input-prefix">R$</span>
              <input v-model.number="novoPreco" class="form-control" type="number" step="0.01" min="0" style="padding-left:2.8rem" />
            </div>
          </div>
          <div class="form-group form-btn">
            <button class="btn btn-success btn-full" @click="cadastrar">Cadastrar</button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Table section -->
    <div class="card table-card">
      <div class="table-header">
        <div>
          <h3>Produtos em Estoque</h3>
          <span class="count-badge">{{ produtosFiltrados.length }}</span>
        </div>
        <div class="input-group" style="max-width:240px">
          <svg class="input-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input v-model="buscaTabela" class="form-control" placeholder="Filtrar..." />
        </div>
      </div>

      <div v-if="loading" class="table-loading">
        <div class="spinner"></div>
        <span>Carregando estoqueâ€¦</span>
      </div>

      <div v-else-if="produtosFiltrados.length === 0" class="empty-state">
        <div class="empty-state-icon">ðŸ“¦</div>
        <p>{{ buscaTabela ? `Nenhum resultado para "${buscaTabela}"` : 'Nenhum produto cadastrado ainda.' }}</p>
      </div>

      <div v-else class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th style="width:60px">#</th>
              <th>Nome</th>
              <th style="width:130px">Qtd</th>
              <th style="width:130px">PreÃ§o</th>
              <th style="width:140px">AÃ§Ãµes</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in produtosFiltrados" :key="p.codigo">
              <td><span class="code-badge">#{{ p.codigo }}</span></td>
              <td class="nome-cell">{{ p.nome }}</td>
              <td>
                <span class="badge" :class="p.quantidade === 0 ? 'badge-red' : p.quantidade <= 5 ? 'badge-yellow' : 'badge-green'">
                  {{ p.quantidade }} un.
                </span>
              </td>
              <td class="preco-cell">{{ fmt(p.preco) }}</td>
              <td class="acoes">
                <button class="btn btn-ghost btn-sm" @click="abrirEdicao(p)" title="Editar">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                  Editar
                </button>
                <button class="btn btn-danger btn-sm" @click="remover(p.codigo)" title="Remover">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Edit modal -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="editando" class="modal-overlay" @click.self="editando = null">
          <div class="modal-box">
            <div class="modal-header">
              <h3>Editar Produto</h3>
              <span class="code-badge">#{{ editando.codigo }}</span>
              <button class="btn btn-icon" @click="editando = null">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
            </div>
            <div class="modal-body">
              <div class="form-group">
                <label class="form-label">Nome</label>
                <input v-model="editando.nome" class="form-control" />
              </div>
              <div class="form-row-2">
                <div class="form-group">
                  <label class="form-label">Quantidade</label>
                  <input v-model.number="editando.quantidade" class="form-control" type="number" min="0" />
                </div>
                <div class="form-group">
                  <label class="form-label">PreÃ§o (R$)</label>
                  <div class="input-group">
                    <span class="input-prefix">R$</span>
                    <input v-model.number="editando.preco" class="form-control" type="number" step="0.01" min="0" style="padding-left:2.8rem" />
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-ghost" @click="editando = null">Cancelar</button>
              <button class="btn btn-primary" @click="salvarEdicao">Salvar alteraÃ§Ãµes</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.estoque-page { display: flex; flex-direction: column; gap: 1.5rem; }

/* Page header */
.page-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; }
.page-title { color: var(--c-800); font-size: 1.4rem; }
.page-sub { font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem; }

/* Stats */
.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1rem 1.25rem; display: flex; align-items: center; gap: 1rem; }
.stat-card--warn { border-color: var(--warning); }
.stat-icon { width: 42px; height: 42px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.stat-icon.green { background: var(--c-50); color: var(--c-700); }
.stat-icon.blue { background: #eff6ff; color: #2563eb; }
.stat-icon.orange { background: #fff7ed; color: #ea580c; }
.stat-icon.gray { background: var(--border); color: var(--text-muted); }
.stat-value { font-size: 1.6rem; font-weight: 700; color: var(--text); line-height: 1; }
.stat-label { font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem; }

/* Alert */
.alert-slide-enter-active, .alert-slide-leave-active { transition: all 0.2s ease; }
.alert-slide-enter-from, .alert-slide-leave-to { opacity: 0; transform: translateY(-6px); }

/* Form panel */
.form-slide-enter-active, .form-slide-leave-active { transition: all 0.25s ease; overflow: hidden; }
.form-slide-enter-from, .form-slide-leave-to { opacity: 0; transform: translateY(-8px); }
.form-card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; }
.form-card-header h3 { font-size: 1rem; color: var(--c-800); }
.form-row { display: grid; grid-template-columns: 2fr 1fr 1fr auto; gap: 1rem; align-items: end; }
.form-btn { padding-bottom: 0; }
.input-prefix { position: absolute; left: 0.85rem; color: var(--text-muted); font-size: 0.85rem; pointer-events: none; top: 50%; transform: translateY(-50%); }

/* Table card */
.table-header { display: flex; align-items: center; justify-content: space-between; gap: 1rem; margin-bottom: 1.25rem; flex-wrap: wrap; }
.table-header h3 { font-size: 1rem; color: var(--c-800); display: inline; margin-right: 0.5rem; }
.count-badge { display: inline-flex; align-items: center; justify-content: center; background: var(--c-100); color: var(--c-700); font-size: 0.7rem; font-weight: 700; border-radius: 20px; padding: 0.15rem 0.5rem; vertical-align: middle; }
.table-loading { display: flex; align-items: center; gap: 0.75rem; color: var(--text-muted); padding: 2rem 0; justify-content: center; font-size: 0.9rem; }
.table-wrapper { overflow-x: auto; border-radius: var(--radius-md); border: 1px solid var(--border); }
.code-badge { font-family: 'Courier New', monospace; font-size: 0.75rem; background: var(--c-50); color: var(--c-700); border: 1px solid var(--c-100); border-radius: 4px; padding: 0.1rem 0.4rem; }
.nome-cell { font-weight: 500; }
.preco-cell { font-family: 'Courier New', monospace; font-weight: 600; color: var(--c-700); }
.acoes { display: flex; gap: 0.4rem; align-items: center; }

/* Modal */
.modal-fade-enter-active, .modal-fade-leave-active { transition: all 0.2s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
.modal-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem; }
.modal-header h3 { font-size: 1.05rem; color: var(--c-800); flex: 1; }
.modal-body { display: flex; flex-direction: column; gap: 1rem; }
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.modal-footer { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.5rem; padding-top: 1.25rem; border-top: 1px solid var(--border); }

@media (max-width: 700px) {
  .stats-row { grid-template-columns: 1fr; }
  .form-row { grid-template-columns: 1fr; }
  .form-row-2 { grid-template-columns: 1fr; }
  .page-header { flex-direction: column; align-items: flex-start; }
}
</style>
