import { 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword,
  signOut,
  onAuthStateChanged
} from 'firebase/auth'
import { auth } from '../firebase/config'

const STORAGE_KEY_AUTH = 'firebase_auth_token'
const STORAGE_KEY_REMEMBER = 'firebase_remember_me'

/**
 * Serviço de autenticação Firebase
 */
class AuthService {
  constructor() {
    this.currentUser = null
    this.authStateListeners = []
  }

  /**
   * Verifica se deve usar localStorage ou sessionStorage
   */
  _getStorage() {
    const rememberMe = localStorage.getItem(STORAGE_KEY_REMEMBER) === 'true'
    return rememberMe ? localStorage : sessionStorage
  }

  /**
   * Salva o token de autenticação
   */
  _saveToken(token, rememberMe = false) {
    const storage = rememberMe ? localStorage : sessionStorage
    storage.setItem(STORAGE_KEY_AUTH, token)
    localStorage.setItem(STORAGE_KEY_REMEMBER, rememberMe.toString())
  }

  /**
   * Remove o token de autenticação
   */
  _removeToken() {
    localStorage.removeItem(STORAGE_KEY_AUTH)
    sessionStorage.removeItem(STORAGE_KEY_AUTH)
    localStorage.removeItem(STORAGE_KEY_REMEMBER)
  }

  /**
   * Obtém o token salvo
   */
  _getSavedToken() {
    const storage = this._getStorage()
    return storage.getItem(STORAGE_KEY_AUTH)
  }

  /**
   * Faz login com email e senha
   * @param {string} email - Email do usuário
   * @param {string} password - Senha do usuário
   * @param {boolean} rememberMe - Se deve manter logado
   * @returns {Promise<Object>} Dados do usuário
   */
  async login(email, password, rememberMe = false) {
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password)
      const user = userCredential.user
      
      // Obter token ID
      const token = await user.getIdToken()
      
      // Salvar token
      this._saveToken(token, rememberMe)
      
      this.currentUser = {
        uid: user.uid,
        email: user.email,
        displayName: user.displayName,
        emailVerified: user.emailVerified
      }
      
      return {
        success: true,
        user: this.currentUser,
        token
      }
    } catch (error) {
      console.error('Erro ao fazer login:', error)
      throw this._handleAuthError(error)
    }
  }

  /**
   * Registra um novo usuário
   * @param {string} email - Email do usuário
   * @param {string} password - Senha do usuário
   * @param {boolean} rememberMe - Se deve manter logado
   * @returns {Promise<Object>} Dados do usuário
   */
  async register(email, password, rememberMe = false) {
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password)
      const user = userCredential.user
      
      // Obter token ID
      const token = await user.getIdToken()
      
      // Salvar token
      this._saveToken(token, rememberMe)
      
      this.currentUser = {
        uid: user.uid,
        email: user.email,
        displayName: user.displayName,
        emailVerified: user.emailVerified
      }
      
      return {
        success: true,
        user: this.currentUser,
        token
      }
    } catch (error) {
      console.error('Erro ao registrar:', error)
      throw this._handleAuthError(error)
    }
  }

  /**
   * Faz logout
   */
  async logout() {
    try {
      await signOut(auth)
      this.currentUser = null
      this._removeToken()
      return { success: true }
    } catch (error) {
      console.error('Erro ao fazer logout:', error)
      throw this._handleAuthError(error)
    }
  }

  /**
   * Obtém o usuário atual
   * @returns {Promise<Object|null>} Dados do usuário ou null
   */
  async getCurrentUser() {
    return new Promise((resolve) => {
      const unsubscribe = onAuthStateChanged(auth, async (user) => {
        unsubscribe()
        
        if (user) {
          try {
            const token = await user.getIdToken()
            this.currentUser = {
              uid: user.uid,
              email: user.email,
              displayName: user.displayName,
              emailVerified: user.emailVerified
            }
            resolve(this.currentUser)
          } catch (error) {
            console.error('Erro ao obter token:', error)
            resolve(null)
          }
        } else {
          this.currentUser = null
          resolve(null)
        }
      })
    })
  }

  /**
   * Obtém o token atual
   * @returns {Promise<string|null>} Token ou null
   */
  async getCurrentToken() {
    if (auth.currentUser) {
      try {
        return await auth.currentUser.getIdToken()
      } catch (error) {
        console.error('Erro ao obter token:', error)
        return null
      }
    }
    return null
  }

  /**
   * Verifica se o usuário está autenticado
   * @returns {Promise<boolean>}
   */
  async isAuthenticated() {
    const user = await this.getCurrentUser()
    return user !== null
  }

  /**
   * Escuta mudanças no estado de autenticação
   * @param {Function} callback - Função chamada quando o estado muda
   * @returns {Function} Função para cancelar a escuta
   */
  onAuthStateChange(callback) {
    return onAuthStateChanged(auth, async (user) => {
      if (user) {
        try {
          const token = await user.getIdToken()
          this.currentUser = {
            uid: user.uid,
            email: user.email,
            displayName: user.displayName,
            emailVerified: user.emailVerified
          }
          callback(this.currentUser)
        } catch (error) {
          console.error('Erro ao obter token:', error)
          callback(null)
        }
      } else {
        this.currentUser = null
        callback(null)
      }
    })
  }

  /**
   * Trata erros de autenticação e retorna mensagens amigáveis
   */
  _handleAuthError(error) {
    const errorMessages = {
      'auth/user-not-found': 'Usuário não encontrado.',
      'auth/wrong-password': 'Senha incorreta.',
      'auth/email-already-in-use': 'Este email já está em uso.',
      'auth/weak-password': 'A senha é muito fraca. Use pelo menos 6 caracteres.',
      'auth/invalid-email': 'Email inválido.',
      'auth/user-disabled': 'Esta conta foi desabilitada.',
      'auth/too-many-requests': 'Muitas tentativas. Tente novamente mais tarde.',
      'auth/network-request-failed': 'Erro de conexão. Verifique sua internet.',
      'auth/operation-not-allowed': 'Operação não permitida.',
      'auth/invalid-credential': 'Credenciais inválidas.'
    }

    const errorCode = error.code || 'auth/unknown-error'
    const message = errorMessages[errorCode] || error.message || 'Erro desconhecido ao autenticar.'
    
    return {
      code: errorCode,
      message: message,
      originalError: error
    }
  }
}

// Exportar instância única
export default new AuthService()

