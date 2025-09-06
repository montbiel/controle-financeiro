# Configuração do Sistema de Controle de Pagamentos

Este guia irá te ajudar a configurar o sistema completo de controle de pagamentos.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Node.js 16 ou superior
- Conta Google com acesso ao Google Sheets
- Projeto no Google Cloud Console

## 🔧 Configuração do Google Sheets API

### 1. Criar Projeto no Google Cloud Console

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Ative a API do Google Sheets:
   - Vá para "APIs & Services" > "Library"
   - Procure por "Google Sheets API"
   - Clique em "Enable"

### 2. Configurar Credenciais

1. Vá para "APIs & Services" > "Credentials"
2. Clique em "Create Credentials" > "OAuth 2.0 Client IDs"
3. Configure o tipo de aplicação como "Desktop application"
4. Baixe o arquivo JSON das credenciais
5. Renomeie o arquivo para `credentials.json`
6. Coloque o arquivo na raiz do projeto

### 3. Criar Planilha no Google Sheets

1. Acesse [Google Sheets](https://sheets.google.com/)
2. Crie uma nova planilha
3. Copie a URL da planilha (exemplo: `https://docs.google.com/spreadsheets/d/1ABC123.../edit`)
4. A planilha será configurada automaticamente pelo sistema

## ⚙️ Configuração do Projeto

### 1. Configurar Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite o arquivo .env com suas configurações
nano .env
```

Configure as seguintes variáveis no arquivo `.env`:

```env
# Google Sheets Configuration
GOOGLE_SHEETS_URL=https://docs.google.com/spreadsheets/d/SEU_SHEET_ID/edit
GOOGLE_CREDENTIALS_FILE=credentials.json
SHEET_NAME=Pagamentos

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### 2. Instalar Dependências Python

```bash
pip install -r requirements.txt
```

### 3. Instalar Dependências do Frontend

```bash
cd frontend
npm install
cd ..
```

## 🚀 Executando o Sistema

### Opção 1: Scripts Automáticos

**Backend:**
```bash
python start_backend.py
```

**Frontend:**
```bash
./start_frontend.sh
```

### Opção 2: Manual

**Backend:**
```bash
cd backend
python main.py
```

**Frontend:**
```bash
cd frontend
npm run serve
```

## 🌐 Acessando o Sistema

- **Frontend:** http://localhost:8080
- **Backend API:** http://localhost:8000
- **Documentação da API:** http://localhost:8000/docs

## 📊 Estrutura da Planilha

O sistema criará automaticamente as seguintes colunas na planilha:

| Coluna | Descrição |
|--------|-----------|
| ID | Identificador único do item |
| Nome | Nome do item de pagamento |
| Valor | Valor total do item |
| Parcelas | Número de parcelas |
| Percentual Pessoa 1 | Percentual que a pessoa 1 paga |
| Percentual Pessoa 2 | Percentual que a pessoa 2 paga |
| Data Criação | Data e hora de criação |
| Ativo | Status do item (True/False) |

## 🔍 Funcionalidades

### Dashboard
- Visualização dos pagamentos mensais por pessoa
- Cálculo de valores restantes
- Resumo total dos pagamentos
- Lista de itens ativos

### Gerenciamento de Itens
- Adicionar novos itens de pagamento
- Editar itens existentes
- Remover itens (soft delete)
- Validação de percentuais
- Cálculo automático de valores mensais

### Integração com Google Sheets
- Sincronização automática com a planilha
- Backup automático dos dados
- Acesso aos dados de qualquer lugar

## 🛠️ Solução de Problemas

### Erro de Autenticação Google
- Verifique se o arquivo `credentials.json` está na raiz do projeto
- Certifique-se de que a API do Google Sheets está ativada
- Execute o sistema uma vez para completar o fluxo de autenticação

### Erro de Conexão com API
- Verifique se o backend está rodando na porta 8000
- Confirme se o arquivo `.env` está configurado corretamente
- Verifique se a URL da planilha está correta

### Erro no Frontend
- Verifique se o Node.js está instalado
- Execute `npm install` no diretório frontend
- Verifique se o backend está rodando

## 📝 Exemplo de Uso

1. **Adicionar um novo item:**
   - Nome: "Aluguel"
   - Valor: R$ 1.200,00
   - Parcelas: 12
   - Percentual Pessoa 1: 60%
   - Percentual Pessoa 2: 40%

2. **Resultado:**
   - Valor mensal total: R$ 100,00
   - Pessoa 1 paga: R$ 60,00/mês
   - Pessoa 2 paga: R$ 40,00/mês

## 🔒 Segurança

- As credenciais do Google são armazenadas localmente
- O sistema usa OAuth 2.0 para autenticação
- Os dados são armazenados na sua própria planilha do Google
- Não há coleta de dados pessoais

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs do console
2. Confirme se todas as dependências estão instaladas
3. Verifique se as credenciais estão configuradas corretamente
4. Teste a conexão com a API do Google Sheets
