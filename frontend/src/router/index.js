import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Items from '../views/Items.vue'
import Login from '../views/Login.vue'
import authService from '../services/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/items',
    name: 'Items',
    component: Items,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navegação para proteger rotas
router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.meta.requiresAuth !== false
  
  if (requiresAuth) {
    // Verifica se o usuário está autenticado
    const isAuthenticated = await authService.isAuthenticated()
    
    if (!isAuthenticated) {
      // Salva a rota de destino para redirecionar após login
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    // Se está acessando a página de login e já está autenticado, redireciona para dashboard
    if (to.path === '/login') {
      const isAuthenticated = await authService.isAuthenticated()
      if (isAuthenticated) {
        next('/')
      } else {
        next()
      }
    } else {
      next()
    }
  }
})

export default router
