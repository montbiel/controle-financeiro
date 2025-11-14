import axios from 'axios'
import authService from './auth'

// Detectar automaticamente a URL da API baseada no hostname e ambiente
function getApiBaseUrl() {
  // Em produção, usar variável de ambiente se configurada (Railway)
  if (process.env.VUE_APP_API_URL) {
    return process.env.VUE_APP_API_URL;
  }
  
  const hostname = window.location.hostname;
  const protocol = window.location.protocol;
  
  // Se for localhost ou 127.0.0.1, usar localhost (desenvolvimento local)
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:8000';
  }
  
  // Se for montbiel.com.br (produção), usar a API do Railway
  if (hostname === 'montbiel.com.br' || hostname === 'www.montbiel.com.br') {
    // Em produção, assumimos que a API está em um subdomínio ou caminho
    // Ajuste conforme sua configuração do Railway
    return `${protocol}//api.montbiel.com.br`; // ou `${protocol}//${hostname}/api`
  }
  
  // Para desenvolvimento em rede local, usar o mesmo IP na porta 8000
  return `http://${hostname}:8000`;
}

const API_BASE_URL = getApiBaseUrl()

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Lista de rotas públicas que não precisam de token
const publicRoutes = ['/health', '/docs', '/openapi.json']

// Interceptor de requisição para adicionar token
api.interceptors.request.use(
  async (config) => {
    // Verifica se a rota é pública
    const isPublicRoute = publicRoutes.some(route => config.url?.includes(route))
    
    if (!isPublicRoute) {
      try {
        // Obtém o token atual
        const token = await authService.getCurrentToken()
        
        if (token) {
          // Adiciona o token no header Authorization
          config.headers.Authorization = `Bearer ${token}`
        }
      } catch (error) {
        console.error('Erro ao obter token:', error)
        // Não bloqueia a requisição, mas pode falhar no backend
      }
    }
    
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Interceptor de resposta para tratamento de erros
api.interceptors.response.use(
  response => response,
  async error => {
    console.error('Erro na API:', error.response?.data || error.message)
    
    // Se receber 401 (não autenticado), redireciona para login
    if (error.response?.status === 401) {
      // Limpa a autenticação
      try {
        await authService.logout()
      } catch (logoutError) {
        console.error('Erro ao fazer logout:', logoutError)
      }
      
      // Redireciona para login apenas se não estiver já na página de login
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    
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

  // Marcar parcela como paga
  async markInstallmentPaid(itemId, mes, pessoa) {
    const response = await api.put(`/payments/items/${itemId}/installments/pay`, null, {
      params: { mes, pessoa }
    })
    return response.data
  },

  // Verificar saúde da API
  async healthCheck() {
    const response = await api.get('/health')
    return response.data
  }
}

export default api
