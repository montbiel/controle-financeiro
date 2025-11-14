<template>
  <div id="app">
    <!-- Navbar apenas se estiver autenticado -->
    <nav v-if="user" class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <a class="navbar-brand" href="#">
          <i class="fas fa-calculator me-2"></i>
          Controle de Pagamentos
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link to="/" class="nav-link">
                <i class="fas fa-home me-1"></i>
                Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/items" class="nav-link">
                <i class="fas fa-list me-1"></i>
                Itens
              </router-link>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="fas fa-user me-1"></i>
                {{ user.email }}
              </a>
              <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                <li>
                  <a class="dropdown-item" href="#" @click.prevent="handleLogout">
                    <i class="fas fa-sign-out-alt me-2"></i>
                    Sair
                  </a>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <main :class="user ? 'container mt-4' : ''">
      <router-view />
    </main>

    <!-- Footer apenas se estiver autenticado -->
    <footer v-if="user" class="bg-light text-center py-3 mt-5">
      <div class="container">
        <p class="text-muted mb-0">
          Sistema de Controle de Pagamentos
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
import { useAuth } from './composables/useAuth'

export default {
  name: 'App',
  setup() {
    const { user, logout } = useAuth()

    const handleLogout = async () => {
      try {
        await logout()
      } catch (error) {
        console.error('Erro ao fazer logout:', error)
      }
    }

    return {
      user,
      handleLogout
    }
  }
}
</script>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}

.navbar-brand {
  font-weight: bold;
}

.router-link-active {
  font-weight: bold;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: 1px solid rgba(0, 0, 0, 0.125);
}

.btn {
  border-radius: 0.375rem;
}

.form-control, .form-select {
  border-radius: 0.375rem;
}

.table {
  border-radius: 0.375rem;
  overflow: hidden;
}

.badge {
  font-size: 0.75em;
}

.text-success {
  color: #198754 !important;
}

.text-danger {
  color: #dc3545 !important;
}

.text-warning {
  color: #fd7e14 !important;
}
</style>
