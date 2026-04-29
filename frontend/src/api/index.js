import axios from 'axios'

const http = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' },
})

export const produtosApi = {
  listar: () => http.get('/produtos'),
  buscar: (codigo) => http.get(`/produtos/${codigo}`),
  cadastrar: (data) => http.post('/produtos', data),
  atualizar: (codigo, data) => http.put(`/produtos/${codigo}`, data),
  remover: (codigo) => http.delete(`/produtos/${codigo}`),
}

export const carrinhoApi = {
  ver: () => http.get('/carrinho'),
  adicionar: (codigo, quantidade) => http.post('/carrinho/adicionar', { codigo, quantidade }),
  remover: (codigo, quantidade) => http.post('/carrinho/remover', { codigo, quantidade }),
  limpar: () => http.delete('/carrinho'),
}

export const pagamentoApi = {
  calcular: (data) => http.post('/pagamento/calcular', data),
  finalizar: (data) => http.post('/pagamento/finalizar', data),
}
