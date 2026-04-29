import { createRouter, createWebHistory } from 'vue-router'
import CaixaView from '../views/CaixaView.vue'
import EstoqueView from '../views/EstoqueView.vue'

const routes = [
  { path: '/', redirect: '/caixa' },
  { path: '/caixa', name: 'Caixa', component: CaixaView },
  { path: '/estoque', name: 'Estoque', component: EstoqueView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
