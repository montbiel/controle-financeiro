<template>
  <div class="dashboard">
    <!-- Header -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex flex-column">
          <h1 class="h2 mb-1">
            <i class="fas fa-tachometer-alt me-2 text-primary"></i>
            Dashboard de Pagamentos
          </h1>
          <p class="text-muted mb-2 ms-4">Visão geral dos pagamentos mensais</p>
          <div v-if="paymentSummary" class="text-muted ms-4">
            <small><i class="fas fa-calendar me-1"></i> Mês atual: {{ paymentSummary.mes_atual }}</small>
          </div>
        </div>
      </div>
    </div>

    <!-- Status da API -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="alert" :class="apiStatusClass" role="alert">
          <i class="fas" :class="apiStatusIcon"></i>
          {{ apiStatusMessage }}
        </div>
      </div>
    </div>

    <!-- Cards de Resumo -->
    <div class="row mb-4" v-if="paymentSummary">
      <div class="col-md-6 mb-3">
        <div class="card border-primary">
          <div class="card-header bg-primary text-white">
            <h5 class="card-title mb-0">
              <i class="fas fa-user me-2"></i>
              {{ paymentSummary.pessoa1 }}
            </h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-4">
                <h6 class="text-muted mb-1">Valor Mensal</h6>
                <h4 class="text-primary mb-0">{{ formatCurrency(paymentSummary.total_pessoa1) }}</h4>
              </div>
              <div class="col-4">
                <h6 class="text-muted mb-1">Restante</h6>
                <h4 class="text-warning mb-0">{{ formatCurrency(paymentSummary.valor_restante_pessoa1) }}</h4>
              </div>
              <div class="col-4">
                <h6 class="text-muted mb-1">Atual (não pago)</h6>
                <h4 class="text-danger mb-0">{{ formatCurrency(paymentSummary.valor_atual_pessoa1) }}</h4>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6 mb-3">
        <div class="card border-success">
          <div class="card-header bg-success text-white">
            <h5 class="card-title mb-0">
              <i class="fas fa-user me-2"></i>
              {{ paymentSummary.pessoa2 }}
            </h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-4">
                <h6 class="text-muted mb-1">Valor Mensal</h6>
                <h4 class="text-success mb-0">{{ formatCurrency(paymentSummary.total_pessoa2) }}</h4>
              </div>
              <div class="col-4">
                <h6 class="text-muted mb-1">Restante</h6>
                <h4 class="text-warning mb-0">{{ formatCurrency(paymentSummary.valor_restante_pessoa2) }}</h4>
              </div>
              <div class="col-4">
                <h6 class="text-muted mb-1">Atual (não pago)</h6>
                <h4 class="text-danger mb-0">{{ formatCurrency(paymentSummary.valor_atual_pessoa2) }}</h4>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Menu Expansível - Resumo Individual -->
    <div class="row mb-4" v-if="paymentSummary">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="fas fa-list me-2"></i>
              Resumo Individual por Pessoa
            </h5>
          </div>
          <div class="card-body">
            <!-- Gabriel -->
            <div class="mb-3">
              <button 
                class="btn btn-outline-primary w-100 text-start" 
                type="button" 
                data-bs-toggle="collapse" 
                data-bs-target="#gabrielResumo" 
                aria-expanded="false"
              >
                <i class="fas fa-user me-2"></i>
                <strong>{{ paymentSummary.pessoa1 }}</strong>
                <span class="float-end">
                  <i class="fas fa-chevron-down"></i>
                </span>
              </button>
              <div class="collapse mt-2" id="gabrielResumo">
                <div class="card card-body">
                  <div class="row">
                    <div class="col-md-4">
                      <h6 class="text-muted">Valor Mensal Total</h6>
                      <h4 class="text-primary">{{ formatCurrency(paymentSummary.total_pessoa1) }}</h4>
                    </div>
                    <div class="col-md-4">
                      <h6 class="text-muted">Valor Restante</h6>
                      <h4 class="text-warning">{{ formatCurrency(paymentSummary.valor_restante_pessoa1) }}</h4>
                    </div>
                    <div class="col-md-4">
                      <h6 class="text-muted">Valor Atual (não pago)</h6>
                      <h4 class="text-danger">{{ formatCurrency(paymentSummary.valor_atual_pessoa1) }}</h4>
                    </div>
                  </div>
                  <hr>
                  <h6 class="text-muted mb-3">Contas de {{ paymentSummary.pessoa1 }}:</h6>
                  <div class="row">
                    <div 
                      v-for="item in getPersonItems(1)" 
                      :key="item.id" 
                      class="col-md-6 mb-2"
                    >
                      <div class="d-flex justify-content-between align-items-center p-2 border rounded">
                        <div>
                          <strong>{{ item.nome }}</strong>
                          <br>
                          <small class="text-muted">
                            {{ formatCurrency(getPersonMonthlyValue(item, 1)) }}/mês
                            <span v-if="item.conta_fixa" class="badge bg-info ms-1">Fixa</span>
                          </small>
                        </div>
                        <div class="form-check">
                          <input 
                            class="form-check-input" 
                            type="checkbox" 
                            :id="`pago_gabriel_${item.id}`"
                            :checked="item.pago_pessoa1"
                            @change="togglePayment(item.id, 1, $event.target.checked)"
                          >
                          <label class="form-check-label" :for="`pago_gabriel_${item.id}`">
                            Pago
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Juliana -->
            <div class="mb-3">
              <button 
                class="btn btn-outline-success w-100 text-start" 
                type="button" 
                data-bs-toggle="collapse" 
                data-bs-target="#julianaResumo" 
                aria-expanded="false"
              >
                <i class="fas fa-user me-2"></i>
                <strong>{{ paymentSummary.pessoa2 }}</strong>
                <span class="float-end">
                  <i class="fas fa-chevron-down"></i>
                </span>
              </button>
              <div class="collapse mt-2" id="julianaResumo">
                <div class="card card-body">
                  <div class="row">
                    <div class="col-md-4">
                      <h6 class="text-muted">Valor Mensal Total</h6>
                      <h4 class="text-success">{{ formatCurrency(paymentSummary.total_pessoa2) }}</h4>
                    </div>
                    <div class="col-md-4">
                      <h6 class="text-muted">Valor Restante</h6>
                      <h4 class="text-warning">{{ formatCurrency(paymentSummary.valor_restante_pessoa2) }}</h4>
                    </div>
                    <div class="col-md-4">
                      <h6 class="text-muted">Valor Atual (não pago)</h6>
                      <h4 class="text-danger">{{ formatCurrency(paymentSummary.valor_atual_pessoa2) }}</h4>
                    </div>
                  </div>
                  <hr>
                  <h6 class="text-muted mb-3">Contas de {{ paymentSummary.pessoa2 }}:</h6>
                  <div class="row">
                    <div 
                      v-for="item in getPersonItems(2)" 
                      :key="item.id" 
                      class="col-md-6 mb-2"
                    >
                      <div class="d-flex justify-content-between align-items-center p-2 border rounded">
                        <div>
                          <strong>{{ item.nome }}</strong>
                          <br>
                          <small class="text-muted">
                            {{ formatCurrency(getPersonMonthlyValue(item, 2)) }}/mês
                            <span v-if="item.conta_fixa" class="badge bg-info ms-1">Fixa</span>
                          </small>
                        </div>
                        <div class="form-check">
                          <input 
                            class="form-check-input" 
                            type="checkbox" 
                            :id="`pago_juliana_${item.id}`"
                            :checked="item.pago_pessoa2"
                            @change="togglePayment(item.id, 2, $event.target.checked)"
                          >
                          <label class="form-check-label" :for="`pago_juliana_${item.id}`">
                            Pago
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Resumo Total -->
    <div class="row mb-4" v-if="paymentSummary">
      <div class="col-12">
        <div class="card border-info">
          <div class="card-header bg-info text-white">
            <h5 class="card-title mb-0">
              <i class="fas fa-chart-pie me-2"></i>
              Resumo Total
            </h5>
          </div>
          <div class="card-body">
            <div class="row text-center">
              <div class="col-md-4">
                <h6 class="text-muted mb-1">Total Mensal</h6>
                <h3 class="text-info mb-0">{{ formatCurrency(totalMensal) }}</h3>
              </div>
              <div class="col-md-4">
                <h6 class="text-muted mb-1">Total Restante</h6>
                <h3 class="text-warning mb-0">{{ formatCurrency(totalRestante) }}</h3>
              </div>
              <div class="col-md-4">
                <h6 class="text-muted mb-1">Itens Ativos</h6>
                <h3 class="text-success mb-0">{{ paymentSummary.itens.length }}</h3>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Lista de Itens Recentes -->
    <div class="row" v-if="paymentSummary && paymentSummary.itens.length > 0">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="fas fa-list me-2"></i>
              Itens de Pagamento
            </h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Valor Total</th>
                    <th>Parcelas</th>
                    <th>Valor Mensal</th>
                    <th>Divisão</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in paymentSummary.itens" :key="item.id">
                    <td>
                      <strong>{{ item.nome }}</strong>
                    </td>
                    <td>{{ formatCurrency(item.valor) }}</td>
                    <td>
                      <span class="badge bg-secondary">{{ item.parcelas }}x</span>
                    </td>
                    <td>{{ formatCurrency(item.valor / item.parcelas) }}</td>
                    <td>
                      <small class="text-muted">
                        {{ item.percentual_pessoa1 }}% / {{ item.percentual_pessoa2 }}%
                      </small>
                    </td>
                    <td>
                      <span class="badge" :class="item.ativo ? 'bg-success' : 'bg-danger'">
                        {{ item.ativo ? 'Ativo' : 'Inativo' }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mensagem quando não há itens -->
    <div class="row" v-else-if="paymentSummary && paymentSummary.itens.length === 0">
      <div class="col-12">
        <div class="card">
          <div class="card-body text-center py-5">
            <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
            <h5 class="text-muted">Nenhum item de pagamento encontrado</h5>
            <p class="text-muted">Adicione novos itens para começar a controlar seus pagamentos.</p>
            <router-link to="/items" class="btn btn-primary">
              <i class="fas fa-plus me-2"></i>
              Adicionar Item
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div class="row" v-if="loading">
      <div class="col-12">
        <div class="card">
          <div class="card-body text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Carregando...</span>
            </div>
            <p class="mt-3 text-muted">Carregando dados...</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { paymentService } from '../services/api'

export default {
  name: 'Dashboard',
  data() {
    return {
      paymentSummary: null,
      loading: true,
      apiStatus: 'checking'
    }
  },
  computed: {
    totalMensal() {
      if (!this.paymentSummary) return 0
      return this.paymentSummary.total_pessoa1 + this.paymentSummary.total_pessoa2
    },
    totalRestante() {
      if (!this.paymentSummary) return 0
      return this.paymentSummary.valor_restante_pessoa1 + this.paymentSummary.valor_restante_pessoa2
    },
    apiStatusClass() {
      switch (this.apiStatus) {
        case 'healthy':
          return 'alert-success'
        case 'unhealthy':
          return 'alert-danger'
        default:
          return 'alert-warning'
      }
    },
    apiStatusIcon() {
      switch (this.apiStatus) {
        case 'healthy':
          return 'fa-check-circle'
        case 'unhealthy':
          return 'fa-exclamation-triangle'
        default:
          return 'fa-spinner fa-spin'
      }
    },
    apiStatusMessage() {
      switch (this.apiStatus) {
        case 'healthy':
          return 'API conectada e funcionando corretamente'
        case 'unhealthy':
          return 'Erro na conexão com a API. Verifique se o backend está rodando.'
        default:
          return 'Verificando conexão com a API...'
      }
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      try {
        this.loading = true
        
        // Verifica saúde da API
        const health = await paymentService.healthCheck()
        this.apiStatus = health.status
        
        if (health.status === 'healthy') {
          // Carrega dados dos pagamentos
          this.paymentSummary = await paymentService.getPaymentSummary()
        }
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
        this.apiStatus = 'unhealthy'
      } finally {
        this.loading = false
      }
    },
    formatCurrency(value) {
      return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      }).format(value)
    },
    getPersonItems(personNumber) {
      if (!this.paymentSummary) return []
      return this.paymentSummary.itens.filter(item => {
        if (personNumber === 1) {
          return item.percentual_pessoa1 > 0 || (item.conta_fixa && item.valor_manual_pessoa1 > 0)
        } else {
          return item.percentual_pessoa2 > 0 || (item.conta_fixa && item.valor_manual_pessoa2 > 0)
        }
      })
    },
    getPersonMonthlyValue(item, personNumber) {
      if (item.conta_fixa) {
        return personNumber === 1 ? item.valor_manual_pessoa1 : item.valor_manual_pessoa2
      } else {
        const percentual = personNumber === 1 ? item.percentual_pessoa1 : item.percentual_pessoa2
        return (item.valor * percentual / 100) / item.parcelas
      }
    },
    async togglePayment(itemId, personNumber, isPaid) {
      try {
        const updateData = {}
        if (personNumber === 1) {
          updateData.pago_pessoa1 = isPaid
        } else {
          updateData.pago_pessoa2 = isPaid
        }
        
        await paymentService.updateItem(itemId, updateData)
        await this.loadData() // Recarrega os dados
      } catch (error) {
        console.error('Erro ao atualizar status de pagamento:', error)
        alert('Erro ao atualizar status de pagamento. Tente novamente.')
      }
    }
  }
}
</script>

<style scoped>
.card {
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
}

.table th {
  border-top: none;
  font-weight: 600;
  color: #495057;
}

.badge {
  font-size: 0.75em;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>
