<script setup>
import { ref } from 'vue'
import { carrinhoApi, pagamentoApi } from '../api'

const props = defineProps({
  carrinho: { type: Object, required: true },
})

const emit = defineEmits(['atualizado'])

const showPagamento = ref(false)
const metodo = ref('dinheiro')
const parcelas = ref(1)
const valorRecebido = ref('')
const preview = ref(null)
const msgPag = ref(null)
const loadingFinalizar = ref(false)

async function removerItem(codigo, quantidade) {
  try {
    const { data } = await carrinhoApi.remover(codigo, quantidade)
    emit('atualizado', data)
  } catch (e) {
    console.error(e)
  }
}

async function limpar() {
  if (!confirm('Limpar o carrinho?')) return
  try {
    await carrinhoApi.limpar()
    emit('atualizado', { itens: [], total: 0, quantidade_total: 0, vazio: true })
  } catch (e) {
    console.error(e)
  }
}

async function calcularPrevio() {
  msgPag.value = null
  preview.value = null
  try {
    const payload = { metodo: metodo.value }
    if (metodo.value === 'credito') payload.parcelas = parcelas.value
    if (metodo.value === 'dinheiro') payload.valor_recebido = parseFloat(valorRecebido.value)
    const { data } = await pagamentoApi.calcular(payload)
    preview.value = data
  } catch (e) {
    msgPag.value = { tipo: 'error', texto: e.response?.data?.detail || 'Erro ao calcular pagamento.' }
  }
}

async function finalizar() {
  msgPag.value = null
  loadingFinalizar.value = true
  try {
    const payload = { metodo: metodo.value }
    if (metodo.value === 'credito') payload.parcelas = parcelas.value
    if (metodo.value === 'dinheiro') payload.valor_recebido = parseFloat(valorRecebido.value)
    const { data } = await pagamentoApi.finalizar(payload)
    msgPag.value = { tipo: 'success', texto: data.mensagem }
    emit('atualizado', { itens: [], total: 0, quantidade_total: 0, vazio: true })
    showPagamento.value = false
    preview.value = null
  } catch (e) {
    msgPag.value = { tipo: 'error', texto: e.response?.data?.detail || 'Erro ao finalizar.' }
  } finally {
    loadingFinalizar.value = false
  }
}

function fmt(v) { return `R$ ${Number(v).toFixed(2)}` }
</script>

<template>
  <div class="carrinho-panel card">
    <div class="carrinho-header">
      <h3>🛒 Carrinho</h3>
      <span class="badge badge-green" v-if="!carrinho.vazio">
        {{ carrinho.quantidade_total }} item(s)
      </span>
    </div>

    <div v-if="carrinho.vazio" class="carrinho-vazio">
      Carrinho vazio
    </div>

    <div v-else>
      <div class="carrinho-item" v-for="item in carrinho.itens" :key="item.codigo">
        <div class="item-info">
          <span class="item-nome">{{ item.nome }}</span>
          <span class="item-qty">{{ item.quantidade }}x {{ fmt(item.preco_unitario) }}</span>
        </div>
        <div class="item-right">
          <span class="item-subtotal">{{ fmt(item.subtotal) }}</span>
          <button class="btn btn-danger btn-sm" @click="removerItem(item.codigo, item.quantidade)">
            🗑
          </button>
        </div>
      </div>

      <hr class="divider" />
      <div class="carrinho-total">
        <strong>Total:</strong>
        <strong class="total-valor">{{ fmt(carrinho.total) }}</strong>
      </div>

      <div class="carrinho-btns">
        <button class="btn btn-secondary btn-sm" @click="limpar">Limpar</button>
        <button class="btn btn-success" @click="showPagamento = true">Finalizar compra</button>
      </div>
    </div>

    <!-- Mensagem pós-pagamento -->
    <div v-if="msgPag" :class="`alert alert-${msgPag.tipo === 'success' ? 'success' : 'error'}`" style="margin-top:0.8rem">
      {{ msgPag.texto }}
    </div>
  </div>

  <!-- Modal pagamento -->
  <Teleport to="body">
    <div v-if="showPagamento" class="modal-overlay" @click.self="showPagamento = false">
      <div class="modal-box">
        <h3>💳 Pagamento</h3>
        <p class="total-info">Total: <strong>{{ fmt(carrinho.total) }}</strong></p>
        <hr class="divider" />

        <div class="form-group">
          <label>Método</label>
          <select v-model="metodo">
            <option value="dinheiro">💵 Dinheiro</option>
            <option value="debito">💳 Débito</option>
            <option value="credito">💳 Crédito</option>
          </select>
        </div>

        <div v-if="metodo === 'credito'" class="form-group">
          <label>Parcelas</label>
          <input v-model.number="parcelas" type="number" min="1" max="24" />
        </div>

        <div v-if="metodo === 'dinheiro'" class="form-group">
          <label>Valor recebido</label>
          <input v-model="valorRecebido" type="number" step="0.01" placeholder="0.00" />
        </div>

        <button class="btn btn-secondary btn-sm" style="margin-bottom:0.8rem" @click="calcularPrevio">
          Calcular
        </button>

        <div v-if="preview" class="preview-box">
          <div v-if="preview.parcelas">
            {{ preview.parcelas }}x de <strong>{{ fmt(preview.valor_parcela) }}</strong>
            = Total <strong>{{ fmt(preview.total_final) }}</strong>
          </div>
          <div v-else-if="preview.troco !== null && preview.troco !== undefined">
            Troco: <strong>{{ fmt(preview.troco) }}</strong>
          </div>
          <div v-else>
            Total: <strong>{{ fmt(preview.total_final) }}</strong>
          </div>
        </div>

        <div v-if="msgPag" :class="`alert alert-${msgPag.tipo === 'success' ? 'success' : 'error'}`">
          {{ msgPag.texto }}
        </div>

        <div class="modal-actions">
          <button class="btn btn-secondary" @click="showPagamento = false">Cancelar</button>
          <button class="btn btn-success" :disabled="loadingFinalizar" @click="finalizar">
            ✔ Confirmar compra
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.carrinho-panel { display: flex; flex-direction: column; gap: 0.75rem; }
.carrinho-header { display: flex; align-items: center; justify-content: space-between; }
.carrinho-header h3 { color: #1b4332; }
.carrinho-vazio { color: #888; text-align: center; padding: 1.5rem 0; }

.carrinho-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.4rem 0; border-bottom: 1px solid #e8f0e9;
}
.item-info { display: flex; flex-direction: column; }
.item-nome { font-weight: 600; font-size: 0.9rem; }
.item-qty { font-size: 0.8rem; color: #666; }
.item-right { display: flex; align-items: center; gap: 0.5rem; }
.item-subtotal { font-weight: 700; color: #2d6a4f; }

.carrinho-total { display: flex; justify-content: space-between; font-size: 1rem; }
.total-valor { color: #2d6a4f; font-size: 1.1rem; }

.carrinho-btns { display: flex; gap: 0.5rem; justify-content: flex-end; margin-top: 0.5rem; }

.total-info { color: #444; margin-bottom: 0.5rem; }
.preview-box { background: #f0f7f1; border-radius: 8px; padding: 0.7rem 1rem; margin-bottom: 0.8rem; font-size: 0.95rem; }
.modal-actions { display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 1rem; }
</style>
