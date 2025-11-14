import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import authService from '../services/auth'

/**
 * Composable Vue 3 para gerenciar autenticação
 */
export function useAuth() {
  const router = useRouter()
  const user = ref(null)
  const loading = ref(true)
  const error = ref(null)
  let unsubscribeAuth = null

  /**
   * Verifica se o usuário está autenticado
   */
  const isAuthenticated = computed(() => user.value !== null)

  /**
   * Faz login
   */
  const login = async (email, password, rememberMe = false) => {
    try {
      loading.value = true
      error.value = null
      const result = await authService.login(email, password, rememberMe)
      user.value = result.user
      return result
    } catch (err) {
      error.value = err
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Registra um novo usuário
   */
  const register = async (email, password, rememberMe = false) => {
    try {
      loading.value = true
      error.value = null
      const result = await authService.register(email, password, rememberMe)
      user.value = result.user
      return result
    } catch (err) {
      error.value = err
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Faz logout
   */
  const logout = async () => {
    try {
      loading.value = true
      error.value = null
      await authService.logout()
      user.value = null
      router.push('/login')
    } catch (err) {
      error.value = err
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Obtém o token atual
   */
  const getToken = async () => {
    return await authService.getCurrentToken()
  }

  /**
   * Verifica autenticação atual
   */
  const checkAuth = async () => {
    try {
      loading.value = true
      const currentUser = await authService.getCurrentUser()
      user.value = currentUser
      return currentUser !== null
    } catch (err) {
      error.value = err
      user.value = null
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Escuta mudanças no estado de autenticação
   */
  const setupAuthListener = () => {
    unsubscribeAuth = authService.onAuthStateChange((currentUser) => {
      user.value = currentUser
      loading.value = false
    })
  }

  /**
   * Limpa o listener ao desmontar
   */
  onMounted(() => {
    setupAuthListener()
    checkAuth()
  })

  onUnmounted(() => {
    if (unsubscribeAuth) {
      unsubscribeAuth()
    }
  })

  return {
    user,
    loading,
    error,
    isAuthenticated,
    login,
    register,
    logout,
    getToken,
    checkAuth
  }
}

