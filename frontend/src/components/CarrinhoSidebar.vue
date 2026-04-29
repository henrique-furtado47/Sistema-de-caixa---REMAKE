<script setup>
import { ref, watch } from 'vue'
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
const removingCodigos = ref(new Set())

// reset preview when method changes
watch(metodo, () => { preview.value = null; msgPag.value = null })

async function removerItem(codigo, quantidade) {
  removingCodigos.value = new Set([...removingCodigos.value, codigo])
  try {
    const { data } = await carrinhoApi.remover(codigo, quantidade)
    emit('atualizado', data)
  } catch (e) {
    console.error(e)
  } finally {
    removingCodigos.value.delete(codigo)
    removingCodigos.value = new Set(removingCodigos.value)
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
    emit('atualizado', { itens: [], total: 0, quantidade_total: 0, vazio: true })
    showPagamento.value = false
    preview.value = null
    metodo.value = 'dinheiro'
    parcelas.value = 1
    valorRecebido.value = ''
    // show success outside modal
    msgPag.value = { tipo: 'success', texto: data.mensagem }
    setTimeout(() => (msgPag.value = null), 3500)
  } catch (e) {
    msgPag.value = { tipo: 'error', texto: e.response?.data?.detail || 'Erro ao finalizar.' }
  } finally {
    loadingFinalizar.value = false
  }
}

function fmt(v) {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v)
}

function openPagamento() {
  msgPag.value = null
  preview.value = null
  showPagamento.value = true
}
</script>

<template>
  <div class="cart-panel">
    <!-- Header -->
    <div class="cart-header">
      <div class="cart-title">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/>
          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
        </svg>
        <span>Carrinho</span>
      </div>
      <div style="display:flex;align-items:center;gap:0.5rem">
        <span v-if="!carrinho.vazio" class="badge badge-green">{{ carrinho.quantidade_total }}</span>
        <button v-if="!carrinho.vazio" class="btn-clear" @click="limpar" title="Limpar carrinho">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Empty state -->
    <div v-if="carrinho.vazio" class="cart-empty">
      <div class="cart-empty-icon">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="opacity:0.3">
          <circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/>
          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
        </svg>
      </div>
      <p>Nenhum item adicionado</p>
      <p class="cart-empty-hint">Selecione produtos ao lado</p>
    </div>

    <!-- Items -->
    <div v-else class="cart-items">
      <TransitionGroup name="item">
        <div
          v-for="item in carrinho.itens"
          :key="item.codigo"
          class="cart-item"
        >
          <div class="item-dot" :style="{ background: `hsl(${(item.codigo * 47) % 60 + 100}, 48%, 72%)` }"></div>
          <div class="item-body">
            <div class="item-nome">{{ item.nome }}</div>
            <div class="item-meta">
              <span class="item-qty-badge">{{ item.quantidade }}×</span>
              <span class="item-unit">{{ fmt(item.preco_unitario) }}</span>
            </div>
          </div>
          <div class="item-right">
            <span class="item-subtotal">{{ fmt(item.subtotal) }}</span>
            <button
              class="item-remove"
              @click="removerItem(item.codigo, item.quantidade)"
              :disabled="removingCodigos.has(item.codigo)"
              title="Remover"
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
        </div>
      </TransitionGroup>
    </div>

    <!-- Footer -->
    <div v-if="!carrinho.vazio" class="cart-footer">
      <div class="cart-total-row">
        <span class="cart-total-label">Total</span>
        <span class="cart-total-value">{{ fmt(carrinho.total) }}</span>
      </div>
      <button class="btn btn-success btn-full btn-lg checkout-btn" @click="openPagamento">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/>
        </svg>
        Finalizar Compra
      </button>
    </div>

    <!-- Alert post-payment -->
    <Transition name="alert-fade">
      <div v-if="msgPag && !showPagamento" :class="`alert alert-${msgPag.tipo === 'success' ? 'success' : 'error'}`" style="margin:0.75rem 0 0">
        {{ msgPag.texto }}
      </div>
    </Transition>
  </div>

  <!-- Payment modal -->
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="showPagamento" class="modal-overlay" @click.self="showPagamento = false">
        <div class="modal-box pag-modal">
          <div class="modal-header">
            <div>
              <h3>Finalizar Pagamento</h3>
              <p class="pag-total">{{ fmt(carrinho.total) }}</p>
            </div>
            <button class="modal-close" @click="showPagamento = false">✕</button>
          </div>

          <!-- Method selector -->
          <div class="form-group">
            <label class="form-label">Método de pagamento</label>
            <div class="method-grid">
              <div
                v-for="m in [{ id:'dinheiro', icon:'💵', label:'Dinheiro' }, { id:'debito', icon:'💳', label:'Débito' }, { id:'credito', icon:'🔄', label:'Crédito' }]"
                :key="m.id"
                :class="['method-option', { selected: metodo === m.id }]"
                @click="metodo = m.id"
              >
                <span class="method-icon">{{ m.icon }}</span>
                <span class="method-label">{{ m.label }}</span>
              </div>
            </div>
          </div>

          <!-- Credit installments -->
          <Transition name="field-fade">
            <div v-if="metodo === 'credito'" class="form-group">
              <label class="form-label">Número de parcelas</label>
              <div class="installment-row">
                <div class="stepper">
                  <button class="stepper-btn" @click="parcelas > 1 && parcelas--">−</button>
                  <span class="stepper-value">{{ parcelas }}</span>
                  <button class="stepper-btn" @click="parcelas < 24 && parcelas++">+</button>
                </div>
                <span class="parcelas-hint">{{ parcelas <= 6 ? 'Sem juros' : `Com juros (${parcelas}/150 × 100%)` }}</span>
              </div>
            </div>
          </Transition>

          <!-- Cash amount -->
          <Transition name="field-fade">
            <div v-if="metodo === 'dinheiro'" class="form-group">
              <label class="form-label">Valor recebido</label>
              <div class="input-group">
                <span class="input-icon">R$</span>
                <input
                  v-model="valorRecebido"
                  type="number"
                  step="0.01"
                  placeholder="0,00"
                  class="form-control"
                  style="padding-left:2.5rem"
                />
              </div>
            </div>
          </Transition>

          <!-- Calculate button -->
          <button class="btn btn-ghost btn-full" style="margin-bottom:0.75rem" @click="calcularPrevio">
            Calcular
          </button>

          <!-- Preview -->
          <Transition name="field-fade">
            <div v-if="preview" class="preview-card">
              <div v-if="preview.parcelas" class="preview-row">
                <span>{{ preview.parcelas }}× de</span>
                <strong>{{ fmt(preview.valor_parcela) }}</strong>
              </div>
              <div v-if="preview.parcelas" class="preview-divider"></div>
              <div class="preview-row">
                <span>Total final</span>
                <strong class="preview-total">{{ fmt(preview.total_final) }}</strong>
              </div>
              <div v-if="preview.troco != null" class="preview-row troco">
                <span>Troco</span>
                <strong>{{ fmt(preview.troco) }}</strong>
              </div>
            </div>
          </Transition>

          <!-- Error inside modal -->
          <div v-if="msgPag && showPagamento" :class="`alert alert-${msgPag.tipo === 'success' ? 'success' : 'error'}`" style="margin-bottom:0.75rem">
            {{ msgPag.texto }}
          </div>

          <div class="modal-footer">
            <button class="btn btn-ghost" @click="showPagamento = false">Cancelar</button>
            <button class="btn btn-success btn-lg" :disabled="loadingFinalizar" @click="finalizar">
              <span v-if="loadingFinalizar" class="spinner" style="width:16px;height:16px;border-width:2px"></span>
              <span v-else>✔ Confirmar compra</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.cart-panel {
  background: var(--surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: sticky;
  top: 76px;
  max-height: calc(100vh - 96px);
}

/* Header */
.cart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.cart-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--c-800);
}
.btn-clear {
  width: 28px; height: 28px;
  border: none;
  background: var(--danger-light);
  color: var(--danger);
  border-radius: 6px;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.18s;
}
.btn-clear:hover { background: var(--danger); color: #fff; }

/* Empty */
.cart-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2.5rem 1rem;
  gap: 0.4rem;
  text-align: center;
}
.cart-empty-icon { margin-bottom: 0.5rem; }
.cart-empty p { font-size: 0.85rem; color: var(--text-muted); font-weight: 500; }
.cart-empty-hint { font-size: 0.75rem; color: var(--text-muted); opacity: 0.7; }

/* Items */
.cart-items {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem 0;
  min-height: 0;
}
.cart-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.6rem 1.25rem;
  transition: background 0.15s;
}
.cart-item:hover { background: var(--c-50); }

.item-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.item-body { flex: 1; min-width: 0; }
.item-nome {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.item-meta { display: flex; align-items: center; gap: 0.4rem; margin-top: 0.15rem; }
.item-qty-badge {
  background: var(--c-100);
  color: var(--c-800);
  font-size: 0.68rem;
  font-weight: 700;
  padding: 0.1rem 0.35rem;
  border-radius: 4px;
}
.item-unit { font-size: 0.75rem; color: var(--text-muted); }
.item-right { display: flex; align-items: center; gap: 0.5rem; flex-shrink: 0; }
.item-subtotal { font-size: 0.85rem; font-weight: 700; color: var(--c-700); }
.item-remove {
  width: 24px; height: 24px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  border-radius: 5px;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.15s, color 0.15s;
}
.item-remove:hover { background: var(--danger-light); color: var(--danger); }
.item-remove:disabled { opacity: 0.4; cursor: default; }

/* Item transitions */
.item-enter-active, .item-leave-active { transition: all 0.22s ease; }
.item-enter-from, .item-leave-to { opacity: 0; transform: translateX(12px); }
.item-move { transition: transform 0.22s ease; }

/* Footer */
.cart-footer {
  padding: 1rem 1.25rem;
  border-top: 1px solid var(--border);
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.cart-total-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.cart-total-label { font-size: 0.85rem; color: var(--text-muted); font-weight: 600; }
.cart-total-value { font-size: 1.35rem; font-weight: 800; color: var(--c-700); letter-spacing: -0.5px; }

.checkout-btn { gap: 0.5rem; }

/* Alert transitions */
.alert-fade-enter-active, .alert-fade-leave-active { transition: all 0.2s; }
.alert-fade-enter-from, .alert-fade-leave-to { opacity: 0; transform: translateY(-4px); }

/* Modal transitions */
.modal-enter-active, .modal-leave-active { transition: opacity 0.18s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }

/* Payment modal specific */
.pag-modal {}
.pag-total {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--c-700);
  letter-spacing: -1px;
  margin-top: 0.15rem;
}

.installment-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.parcelas-hint { font-size: 0.78rem; color: var(--text-muted); }

/* Preview card */
.preview-card {
  background: var(--c-50);
  border: 1px solid var(--c-100);
  border-radius: var(--radius-md);
  padding: 0.85rem 1rem;
  margin-bottom: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.preview-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  color: var(--text-secondary);
}
.preview-divider { border-top: 1px solid var(--c-200); margin: 0.2rem 0; }
.preview-total { font-size: 1.1rem; color: var(--c-700); }
.troco strong { color: var(--success); }

/* Field transitions */
.field-fade-enter-active, .field-fade-leave-active { transition: all 0.2s; }
.field-fade-enter-from, .field-fade-leave-to { opacity: 0; transform: translateY(-6px); }
</style>

