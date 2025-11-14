<template>
  <div class="login-container">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">
        <div class="col-12 col-md-6 col-lg-4">
          <div class="card shadow">
            <div class="card-body p-4">
              <!-- Header -->
              <div class="text-center mb-4">
                <h2 class="h3 mb-2 login-title">
                  <i class="fas fa-lock me-2"></i>
                  Acesso ao Sistema
                </h2>
                <p class="text-muted mb-0">Sistema de Controle de Pagamentos</p>
              </div>

              <!-- Mensagem de erro -->
              <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="fas fa-exclamation-circle me-2"></i>
                {{ error.message }}
                <button type="button" class="btn-close" @click="error = null" aria-label="Close"></button>
              </div>

              <!-- Formulário de login -->
              <form @submit.prevent="handleLogin">
                <!-- Campo Email -->
                <div class="mb-3">
                  <label for="email" class="form-label">
                    <i class="fas fa-envelope me-1"></i>
                    Email
                  </label>
                  <input
                    type="email"
                    class="form-control"
                    :class="{ 'is-invalid': errors.email }"
                    id="email"
                    v-model="form.email"
                    placeholder="Digite seu email"
                    required
                    autocomplete="email"
                    @blur="validateEmail"
                  />
                  <div v-if="errors.email" class="invalid-feedback">
                    {{ errors.email }}
                  </div>
                </div>

                <!-- Campo Senha -->
                <div class="mb-3">
                  <label for="password" class="form-label">
                    <i class="fas fa-key me-1"></i>
                    Senha
                  </label>
                  <div class="password-input-wrapper">
                    <input
                      :type="showPassword ? 'text' : 'password'"
                      class="form-control"
                      :class="{ 'is-invalid': errors.password }"
                      id="password"
                      v-model="form.password"
                      placeholder="Digite sua senha"
                      required
                      autocomplete="current-password"
                      @blur="validatePassword"
                    />
                    <button
                      type="button"
                      class="password-toggle-btn"
                      @click="togglePasswordVisibility"
                      :aria-label="showPassword ? 'Ocultar senha' : 'Mostrar senha'"
                    >
                      <i 
                        :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'" 
                        class="eye-icon"
                        style="
                          color: #495057 !important; 
                          font-size: 1.2rem !important; 
                          display: inline-block !important; 
                          visibility: visible !important;
                          opacity: 1 !important;
                          font-family: 'Font Awesome 6 Free' !important;
                          font-weight: 900 !important;
                        "
                      ></i>
                    </button>
                  </div>
                  <div v-if="errors.password" class="invalid-feedback d-block">
                    {{ errors.password }}
                  </div>
                </div>

                <!-- Checkbox Manter-me logado -->
                <div class="mb-3 form-check">
                  <input
                    type="checkbox"
                    class="form-check-input"
                    id="rememberMe"
                    v-model="form.rememberMe"
                  />
                  <label class="form-check-label" for="rememberMe">
                    Logar automaticamente
                  </label>
                </div>

                <!-- Botão de Login -->
                <div class="d-grid">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="loading || !isFormValid"
                  >
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    <i v-else class="fas fa-sign-in-alt me-2"></i>
                    {{ loading ? 'Entrando...' : 'Entrar' }}
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- Footer opcional -->
          <div class="text-center mt-3">
            <small class="text-muted">
              Sistema de Controle de Pagamentos - Desenvolvido com Vue.js e FastAPI
            </small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '../composables/useAuth'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const { login, loading, error } = useAuth()

    const form = ref({
      email: '',
      password: '',
      rememberMe: false
    })

    const showPassword = ref(false)
    const errors = ref({
      email: null,
      password: null
    })

    /**
     * Valida o formato do email
     */
    const validateEmail = () => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!form.value.email) {
        errors.value.email = 'Email é obrigatório'
      } else if (!emailRegex.test(form.value.email)) {
        errors.value.email = 'Email inválido'
      } else {
        errors.value.email = null
      }
    }

    /**
     * Valida a senha
     */
    const validatePassword = () => {
      if (!form.value.password) {
        errors.value.password = 'Senha é obrigatória'
      } else if (form.value.password.length < 6) {
        errors.value.password = 'Senha deve ter pelo menos 6 caracteres'
      } else {
        errors.value.password = null
      }
    }

    /**
     * Alterna visibilidade da senha
     */
    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value
    }

    /**
     * Verifica se o formulário é válido
     */
    const isFormValid = computed(() => {
      return form.value.email && 
             form.value.password && 
             !errors.value.email && 
             !errors.value.password &&
             form.value.password.length >= 6
    })

    /**
     * Processa o login
     */
    const handleLogin = async () => {
      // Validar campos
      validateEmail()
      validatePassword()

      if (!isFormValid.value) {
        return
      }

      try {
        await login(form.value.email, form.value.password, form.value.rememberMe)
        
        // Redirecionar para a rota de destino ou dashboard
        const redirect = route.query.redirect || '/'
        router.push(redirect)
      } catch (err) {
        // Erro já é tratado pelo composable useAuth
        console.error('Erro no login:', err)
      }
    }

    return {
      form,
      showPassword,
      errors,
      loading,
      error,
      isFormValid,
      togglePasswordVisibility,
      validateEmail,
      validatePassword,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: #ffffff;
  padding: 20px;
}

.card {
  border: none;
  border-radius: 0.5rem;
}

.card-body {
  background: white;
}

.login-title {
  color: #0d6efd;
}

.login-title i {
  color: #0d6efd;
}

.password-input-wrapper {
  position: relative;
}

.password-input-wrapper .form-control {
  padding-right: 2.5rem;
}

.password-toggle-btn {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  border: none;
  background: rgba(255, 255, 255, 0.01) !important;
  cursor: pointer;
  display: flex !important;
  align-items: center;
  justify-content: center;
  padding: 0 0.75rem;
  color: #495057 !important;
  z-index: 1000;
  transition: color 0.15s ease-in-out;
  width: auto;
  min-width: 2.5rem;
  pointer-events: auto !important;
  visibility: visible !important;
  opacity: 1 !important;
}

.password-toggle-btn:hover {
  color: #0d6efd !important;
  background: transparent !important;
}

.password-toggle-btn:focus {
  box-shadow: none;
  outline: none;
}

.password-toggle-btn i,
.password-toggle-btn .eye-icon,
.password-toggle-btn i.fa-eye,
.password-toggle-btn i.fa-eye-slash {
  font-size: 1.2rem !important;
  color: #495057 !important;
  opacity: 1 !important;
  display: inline-block !important;
  visibility: visible !important;
  font-weight: normal !important;
  font-style: normal !important;
  line-height: 1 !important;
  width: auto !important;
  height: auto !important;
}

.password-toggle-btn:hover i,
.password-toggle-btn:hover .eye-icon,
.password-toggle-btn:hover i.fa-eye,
.password-toggle-btn:hover i.fa-eye-slash {
  color: #0d6efd !important;
  opacity: 1 !important;
}

.form-check-input:checked {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-primary:hover:not(:disabled) {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

.alert {
  border-radius: 0.375rem;
}

@media (max-width: 576px) {
  .login-container {
    padding: 10px;
  }
  
  .card-body {
    padding: 1.5rem !important;
  }
}
</style>

