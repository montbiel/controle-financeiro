import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para tratamento de erros
api.interceptors.response.use(
  response => response,
  error => {
    console.error('Erro na API:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export const paymentService = {
  // Buscar resumo dos pagamentos
  async getPaymentSummary() {
    const response = await api.get('/payments/summary')
    return response.data
  },

  // Buscar todos os itens
  async getItems() {
    const response = await api.get('/payments/items')
    return response.data
  },

  // Criar novo item
  async createItem(itemData) {
    const response = await api.post('/payments/items', itemData)
    return response.data
  },

  // Atualizar item
  async updateItem(itemId, itemData) {
    const response = await api.put(`/payments/items/${itemId}`, itemData)
    return response.data
  },

  // Deletar item
  async deleteItem(itemId) {
    const response = await api.delete(`/payments/items/${itemId}`)
    return response.data
  },

  // Verificar saúde da API
  async healthCheck() {
    const response = await api.get('/health')
    return response.data
  }
}

export default api
