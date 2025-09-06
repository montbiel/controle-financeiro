<template>
  <div class="items">
    <!-- Header -->
    <div class="row mb-4">
      <div class="col-12">
        <h1 class="h2 mb-0">
          <i class="fas fa-list me-2 text-primary"></i>
          Gerenciar Itens
        </h1>
        <p class="text-muted">Adicione, edite ou remova itens de pagamento</p>
      </div>
    </div>

    <!-- Botão para adicionar novo item -->
    <div class="row mb-4">
      <div class="col-12">
        <button 
          class="btn btn-primary" 
          @click="showAddModal = true"
          :disabled="loading"
        >
          <i class="fas fa-plus me-2"></i>
          Adicionar Novo Item
        </button>
      </div>
    </div>

    <!-- Lista de itens -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="fas fa-list me-2"></i>
              Itens de Pagamento
            </h5>
          </div>
          <div class="card-body">
            <!-- Loading -->
            <div v-if="loading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Carregando...</span>
              </div>
              <p class="mt-3 text-muted">Carregando itens...</p>
            </div>

            <!-- Tabela de itens -->
            <div v-else-if="items.length > 0" class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Valor Total</th>
                    <th>Parcelas</th>
                    <th>Valor Mensal</th>
                    <th>Divisão</th>
                    <th>Data Criação</th>
                    <th>Status</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in items" :key="item.id">
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
                      <small class="text-muted">{{ item.data_criacao }}</small>
                    </td>
                    <td>
                      <span class="badge" :class="item.ativo ? 'bg-success' : 'bg-danger'">
                        {{ item.ativo ? 'Ativo' : 'Inativo' }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group" role="group">
                        <button 
                          class="btn btn-sm btn-outline-primary"
                          @click="editItem(item)"
                          title="Editar"
                        >
                          <i class="fas fa-edit"></i>
                        </button>
                        <button 
                          class="btn btn-sm btn-outline-danger"
                          @click="deleteItem(item)"
                          title="Remover"
                        >
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Mensagem quando não há itens -->
            <div v-else class="text-center py-5">
              <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
              <h5 class="text-muted">Nenhum item encontrado</h5>
              <p class="text-muted">Adicione seu primeiro item de pagamento.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para adicionar/editar item -->
    <div class="modal fade" :class="{ show: showAddModal || showEditModal }" 
         :style="{ display: (showAddModal || showEditModal) ? 'block' : 'none' }" 
         tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-plus me-2"></i>
              {{ isEditing ? 'Editar Item' : 'Adicionar Novo Item' }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveItem">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="nome" class="form-label">Nome do Item *</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    id="nome" 
                    v-model="form.nome"
                    required
                    placeholder="Ex: Aluguel, Internet, etc."
                  >
                </div>
                <div class="col-md-6 mb-3">
                  <label for="valor" class="form-label">Valor Total *</label>
                  <div class="input-group">
                    <span class="input-group-text">R$</span>
                    <input 
                      type="number" 
                      class="form-control" 
                      id="valor" 
                      v-model="form.valor"
                      step="0.01"
                      min="0.01"
                      required
                      placeholder="0,00"
                    >
                  </div>
                </div>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="parcelas" class="form-label">Número de Parcelas *</label>
                  <input 
                    type="number" 
                    class="form-control" 
                    id="parcelas" 
                    v-model="form.parcelas"
                    min="1"
                    required
                    placeholder="1"
                  >
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Valor Mensal</label>
                  <div class="form-control-plaintext">
                    <strong>{{ formatCurrency(monthlyValue) }}</strong>
                  </div>
                </div>
              </div>

              <!-- Checkbox para conta fixa -->
              <div class="row mb-3">
                <div class="col-12">
                  <div class="form-check">
                    <input 
                      class="form-check-input" 
                      type="checkbox" 
                      id="conta_fixa" 
                      v-model="form.conta_fixa"
                    >
                    <label class="form-check-label" for="conta_fixa">
                      <strong>Conta Fixa</strong> - Definir valores manuais para cada pessoa
                    </label>
                  </div>
                </div>
              </div>

              <!-- Campos de percentual (quando não é conta fixa) -->
              <div v-if="!form.conta_fixa" class="row">
                <div class="col-md-6 mb-3">
                  <label for="percentual_pessoa1" class="form-label">
                    Percentual Gabriel * 
                    <small class="text-muted">(ajustado automaticamente)</small>
                  </label>
                  <div class="input-group">
                    <input 
                      type="number" 
                      class="form-control" 
                      id="percentual_pessoa1" 
                      v-model="form.percentual_pessoa1"
                      step="0.01"
                      min="0"
                      max="100"
                      required
                      placeholder="50"
                    >
                    <span class="input-group-text">%</span>
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <label for="percentual_pessoa2" class="form-label">
                    Percentual Juliana * 
                    <small class="text-muted">(ajustado automaticamente)</small>
                  </label>
                  <div class="input-group">
                    <input 
                      type="number" 
                      class="form-control" 
                      id="percentual_pessoa2" 
                      v-model="form.percentual_pessoa2"
                      step="0.01"
                      min="0"
                      max="100"
                      required
                      placeholder="50"
                    >
                    <span class="input-group-text">%</span>
                  </div>
                </div>
              </div>

              <!-- Campos de valor manual (quando é conta fixa) -->
              <div v-if="form.conta_fixa" class="row">
                <div class="col-md-6 mb-3">
                  <label for="valor_manual_pessoa1" class="form-label">
                    Valor Gabriel *
                  </label>
                  <div class="input-group">
                    <span class="input-group-text">R$</span>
                    <input 
                      type="number" 
                      class="form-control" 
                      id="valor_manual_pessoa1" 
                      v-model="form.valor_manual_pessoa1"
                      step="0.01"
                      min="0"
                      required
                      placeholder="0.00"
                    >
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <label for="valor_manual_pessoa2" class="form-label">
                    Valor Juliana *
                  </label>
                  <div class="input-group">
                    <span class="input-group-text">R$</span>
                    <input 
                      type="number" 
                      class="form-control" 
                      id="valor_manual_pessoa2" 
                      v-model="form.valor_manual_pessoa2"
                      step="0.01"
                      min="0"
                      required
                      placeholder="0.00"
                    >
                  </div>
                </div>
              </div>

              <!-- Validação de percentuais -->
              <div v-if="!isPercentageValid" class="alert alert-warning">
                <i class="fas fa-exclamation-triangle me-2"></i>
                A soma dos percentuais deve ser igual a 100%
                <button type="button" class="btn btn-sm btn-outline-warning ms-2" @click="adjustPercentages">
                  <i class="fas fa-balance-scale me-1"></i>
                  Ajustar Automaticamente
                </button>
              </div>

              <!-- Resumo da divisão -->
              <div v-if="isFormValid && form.valor && form.parcelas" class="alert alert-info">
                <h6 class="mb-2">Resumo da Divisão:</h6>
                <div class="row">
                  <div class="col-6">
                    <strong>Gabriel:</strong> {{ formatCurrency(person1Monthly) }} por mês
                  </div>
                  <div class="col-6">
                    <strong>Juliana:</strong> {{ formatCurrency(person2Monthly) }} por mês
                  </div>
                </div>
                <div v-if="form.conta_fixa" class="mt-2">
                  <small class="text-muted">
                    <i class="fas fa-info-circle me-1"></i>
                    Conta fixa: Valores definidos manualmente
                  </small>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">
              Cancelar
            </button>
            <button 
              type="button" 
              class="btn btn-primary" 
              @click="saveItem"
              :disabled="!isFormValid || saving"
            >
              <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="fas fa-save me-2"></i>
              {{ isEditing ? 'Atualizar' : 'Salvar' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de confirmação para deletar -->
    <div class="modal fade" :class="{ show: showDeleteModal }" 
         :style="{ display: showDeleteModal ? 'block' : 'none' }" 
         tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-exclamation-triangle me-2 text-warning"></i>
              Confirmar Remoção
            </h5>
            <button type="button" class="btn-close" @click="showDeleteModal = false"></button>
          </div>
          <div class="modal-body">
            <p>Tem certeza que deseja remover o item <strong>{{ itemToDelete?.nome }}</strong>?</p>
            <p class="text-muted">Esta ação marcará o item como inativo.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">
              Cancelar
            </button>
            <button 
              type="button" 
              class="btn btn-danger" 
              @click="confirmDelete"
              :disabled="deleting"
            >
              <span v-if="deleting" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="fas fa-trash me-2"></i>
              Remover
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Overlay para modal -->
    <div v-if="showAddModal || showEditModal || showDeleteModal" 
         class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import { paymentService } from '../services/api'

export default {
  name: 'Items',
  data() {
    return {
      items: [],
      loading: true,
      saving: false,
      deleting: false,
      showAddModal: false,
      showEditModal: false,
      showDeleteModal: false,
      isEditing: false,
      itemToDelete: null,
      form: {
        nome: '',
        valor: '',
        parcelas: 1,
        percentual_pessoa1: 50,
        percentual_pessoa2: 50,
        conta_fixa: false,
        valor_manual_pessoa1: null,
        valor_manual_pessoa2: null
      }
    }
  },
  computed: {
    monthlyValue() {
      if (!this.form.valor || !this.form.parcelas) return 0
      return parseFloat(this.form.valor) / parseInt(this.form.parcelas)
    },
    person1Monthly() {
      if (this.form.conta_fixa) {
        return this.form.valor_manual_pessoa1 || 0
      }
      if (!this.form.valor || !this.form.parcelas || !this.form.percentual_pessoa1) return 0
      return (parseFloat(this.form.valor) * parseFloat(this.form.percentual_pessoa1) / 100) / parseInt(this.form.parcelas)
    },
    person2Monthly() {
      if (this.form.conta_fixa) {
        return this.form.valor_manual_pessoa2 || 0
      }
      if (!this.form.valor || !this.form.parcelas || !this.form.percentual_pessoa2) return 0
      return (parseFloat(this.form.valor) * parseFloat(this.form.percentual_pessoa2) / 100) / parseInt(this.form.parcelas)
    },
    isPercentageValid() {
      const p1 = parseFloat(this.form.percentual_pessoa1) || 0
      const p2 = parseFloat(this.form.percentual_pessoa2) || 0
      return Math.abs((p1 + p2) - 100) < 0.01
    },
    isFormValid() {
      const basicValid = this.form.nome && this.form.valor && this.form.parcelas
      
      if (this.form.conta_fixa) {
        return basicValid && 
               this.form.valor_manual_pessoa1 !== null && 
               this.form.valor_manual_pessoa1 > 0 &&
               this.form.valor_manual_pessoa2 !== null && 
               this.form.valor_manual_pessoa2 > 0
      } else {
        return basicValid && this.isPercentageValid
      }
    }
  },
  watch: {
    'form.percentual_pessoa1'(newValue) {
      if (newValue !== null && newValue !== undefined && newValue !== '') {
        const p1 = parseFloat(newValue)
        if (p1 >= 0 && p1 <= 100) {
          this.form.percentual_pessoa2 = (100 - p1).toFixed(2)
        }
      }
    },
    'form.percentual_pessoa2'(newValue) {
      if (newValue !== null && newValue !== undefined && newValue !== '') {
        const p2 = parseFloat(newValue)
        if (p2 >= 0 && p2 <= 100) {
          this.form.percentual_pessoa1 = (100 - p2).toFixed(2)
        }
      }
    }
  },
  async mounted() {
    await this.loadItems()
  },
  methods: {
    async loadItems() {
      try {
        this.loading = true
        this.items = await paymentService.getItems()
      } catch (error) {
        console.error('Erro ao carregar itens:', error)
        alert('Erro ao carregar itens. Verifique se o backend está rodando.')
      } finally {
        this.loading = false
      }
    },
    async saveItem() {
      if (!this.isFormValid) return

      try {
        this.saving = true
        
        const itemData = {
          nome: this.form.nome,
          valor: parseFloat(this.form.valor),
          parcelas: parseInt(this.form.parcelas),
          percentual_pessoa1: parseFloat(this.form.percentual_pessoa1),
          percentual_pessoa2: parseFloat(this.form.percentual_pessoa2),
          conta_fixa: this.form.conta_fixa,
          valor_manual_pessoa1: this.form.valor_manual_pessoa1 ? parseFloat(this.form.valor_manual_pessoa1) : null,
          valor_manual_pessoa2: this.form.valor_manual_pessoa2 ? parseFloat(this.form.valor_manual_pessoa2) : null
        }

        if (this.isEditing) {
          await paymentService.updateItem(this.editingItemId, itemData)
          alert('Item atualizado com sucesso!')
        } else {
          await paymentService.createItem(itemData)
          alert('Item criado com sucesso!')
        }

        this.closeModal()
        await this.loadItems()
      } catch (error) {
        console.error('Erro ao salvar item:', error)
        alert('Erro ao salvar item. Tente novamente.')
      } finally {
        this.saving = false
      }
    },
    editItem(item) {
      this.isEditing = true
      this.editingItemId = item.id
      this.form = {
        nome: item.nome,
        valor: item.valor.toString(),
        parcelas: item.parcelas,
        percentual_pessoa1: item.percentual_pessoa1,
        percentual_pessoa2: item.percentual_pessoa2,
        conta_fixa: item.conta_fixa || false,
        valor_manual_pessoa1: item.valor_manual_pessoa1 || null,
        valor_manual_pessoa2: item.valor_manual_pessoa2 || null
      }
      this.showEditModal = true
    },
    deleteItem(item) {
      this.itemToDelete = item
      this.showDeleteModal = true
    },
    async confirmDelete() {
      try {
        this.deleting = true
        await paymentService.deleteItem(this.itemToDelete.id)
        alert('Item removido com sucesso!')
        this.showDeleteModal = false
        await this.loadItems()
      } catch (error) {
        console.error('Erro ao deletar item:', error)
        alert('Erro ao remover item. Tente novamente.')
      } finally {
        this.deleting = false
      }
    },
    closeModal() {
      this.showAddModal = false
      this.showEditModal = false
      this.isEditing = false
      this.editingItemId = null
      this.form = {
        nome: '',
        valor: '',
        parcelas: 1,
        percentual_pessoa1: 50,
        percentual_pessoa2: 50,
        conta_fixa: false,
        valor_manual_pessoa1: null,
        valor_manual_pessoa2: null
      }
    },
    formatCurrency(value) {
      return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
      }).format(value)
    },
    adjustPercentages() {
      // Garante que os percentuais sempre somem 100%
      const p1 = parseFloat(this.form.percentual_pessoa1) || 0
      const p2 = parseFloat(this.form.percentual_pessoa2) || 0
      const total = p1 + p2
      
      if (total !== 100) {
        // Ajusta proporcionalmente
        if (total > 0) {
          this.form.percentual_pessoa1 = ((p1 / total) * 100).toFixed(2)
          this.form.percentual_pessoa2 = ((p2 / total) * 100).toFixed(2)
        } else {
          this.form.percentual_pessoa1 = 50
          this.form.percentual_pessoa2 = 50
        }
      }
    }
  }
}
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.5);
}

.table th {
  border-top: none;
  font-weight: 600;
  color: #495057;
}

.badge {
  font-size: 0.75em;
}

.btn-group .btn {
  margin-right: 2px;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

.form-control-plaintext {
  padding: 0.375rem 0;
  margin-bottom: 0;
  line-height: 1.5;
  background-color: transparent;
  border: solid transparent;
  border-width: 1px 0;
}
</style>
