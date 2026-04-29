<script setup>
import { onMounted, ref } from 'vue'
import { produtosApi } from '../api'

const produtos = ref([])
const loading = ref(false)
const alertMsg = ref(null)

// Form novo produto
const novoNome = ref('')
const novaQtd = ref(0)
const novoPreco = ref(0)

// Edição
const editando = ref(null) // { codigo, nome, quantidade, preco }

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
    alertMsg.value = { tipo: 'error', texto: 'Nome é obrigatório.' }
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
    <h2>📦 Gerenciar Estoque</h2>

    <div v-if="alertMsg" :class="`alert alert-${alertMsg.tipo === 'success' ? 'success' : 'error'}`">
      {{ alertMsg.texto }}
    </div>

    <!-- Cadastrar produto -->
    <div class="card form-card">
      <h3>Cadastrar novo produto</h3>
      <div class="form-row">
        <div class="form-group">
          <label>Nome</label>
          <input v-model="novoNome" placeholder="Nome do produto" />
        </div>
        <div class="form-group">
          <label>Quantidade</label>
          <input v-model.number="novaQtd" type="number" min="0" />
        </div>
        <div class="form-group">
          <label>Preço (R$)</label>
          <input v-model.number="novoPreco" type="number" step="0.01" min="0" />
        </div>
        <div class="form-group form-btn">
          <button class="btn btn-primary" @click="cadastrar">+ Cadastrar</button>
        </div>
      </div>
    </div>

    <!-- Tabela de produtos -->
    <div class="card table-card">
      <h3>Produtos em estoque ({{ produtos.length }})</h3>
      <div v-if="loading" class="loading-msg">Carregando...</div>
      <div v-else-if="produtos.length === 0" class="empty-msg">Nenhum produto cadastrado.</div>
      <div v-else class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Nome</th>
              <th>Quantidade</th>
              <th>Preço</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in produtos" :key="p.codigo">
              <td>{{ p.codigo }}</td>
              <td>{{ p.nome }}</td>
              <td>
                <span :class="p.quantidade > 0 ? 'badge-green' : 'badge-red'" class="badge">
                  {{ p.quantidade }}
                </span>
              </td>
              <td>{{ fmt(p.preco) }}</td>
              <td class="acoes">
                <button class="btn btn-warning btn-sm" @click="abrirEdicao(p)">✏ Editar</button>
                <button class="btn btn-danger btn-sm" @click="remover(p.codigo)">🗑 Remover</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal edição -->
    <Teleport to="body">
      <div v-if="editando" class="modal-overlay" @click.self="editando = null">
        <div class="modal-box">
          <h3>✏ Editar Produto #{{ editando.codigo }}</h3>
          <div class="form-group">
            <label>Nome</label>
            <input v-model="editando.nome" />
          </div>
          <div class="form-group">
            <label>Quantidade</label>
            <input v-model.number="editando.quantidade" type="number" min="0" />
          </div>
          <div class="form-group">
            <label>Preço (R$)</label>
            <input v-model.number="editando.preco" type="number" step="0.01" min="0" />
          </div>
          <div class="modal-actions">
            <button class="btn btn-secondary" @click="editando = null">Cancelar</button>
            <button class="btn btn-primary" @click="salvarEdicao">Salvar</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.estoque-page { display: flex; flex-direction: column; gap: 1.5rem; }
.estoque-page h2 { color: #1b4332; }

.form-card h3, .table-card h3 { color: #1b4332; margin-bottom: 1rem; }

.form-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr auto;
  gap: 1rem;
  align-items: end;
}
.form-btn { padding-bottom: 0; }

.table-wrapper { overflow-x: auto; }

.acoes { display: flex; gap: 0.4rem; }

.loading-msg, .empty-msg { text-align: center; color: #888; padding: 2rem; }

.modal-actions { display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 1rem; }

@media (max-width: 640px) {
  .form-row { grid-template-columns: 1fr; }
}
</style>
