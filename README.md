# Sistema de Controle de Pagamentos Mensais

Um sistema completo para controle de pagamentos mensais com divisão proporcional entre duas pessoas, desenvolvido com Python (FastAPI) e Vue.js.

## 🚀 Funcionalidades

- ✅ **Controle de Pagamentos Mensais**: Gerencia pagamentos com parcelas e divisão por percentual
- ✅ **Contas Fixas**: Suporte para contas com valores manuais por pessoa
- ✅ **Divisão Proporcional**: Ajuste automático de percentuais para manter 100%
- ✅ **Status de Pagamento**: Marcação de contas como pagas por pessoa
- ✅ **Resumo Individual**: Menu expansível com resumo por pessoa
- ✅ **Valor Atual**: Cálculo em tempo real do valor não pago
- ✅ **Persistência**: Integração com Google Sheets como banco de dados
- ✅ **Interface Moderna**: Frontend responsivo com Vue.js e Bootstrap

## 🛠️ Tecnologias

### Backend
- **Python 3.13**
- **FastAPI** - Framework web moderno e rápido
- **Google Sheets API** - Persistência de dados
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI

### Frontend
- **Vue.js 3** - Framework JavaScript reativo
- **Bootstrap 5** - Framework CSS responsivo
- **Axios** - Cliente HTTP

## 📋 Pré-requisitos

- Python 3.13+
- Node.js 16+
- Conta Google com Google Sheets API habilitada
- Service Account do Google Cloud Platform

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/montbiel/controle-financeiro.git
cd controle-financeiro
```

### 2. Configuração do Backend
```bash
cd backend
pip install -r requirements.txt
```

### 3. Configuração do Frontend
```bash
cd frontend
npm install
```

### 4. Configuração do Google Sheets
1. Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/)
2. Habilite a Google Sheets API
3. Crie uma Service Account e baixe o arquivo JSON
4. Renomeie o arquivo para `service-account.json` e coloque na pasta `backend/`
5. Compartilhe sua planilha do Google Sheets com o email da Service Account

### 5. Configuração das Variáveis de Ambiente
```bash
cp env.example .env
```

Edite o arquivo `.env` com suas configurações:
```env
GOOGLE_SHEETS_URL=https://docs.google.com/spreadsheets/d/SEU_ID_AQUI/edit
GOOGLE_SERVICE_ACCOUNT_FILE=service-account.json
SHEET_NAME=Pagamentos
```

## 🏃‍♂️ Executando o Sistema

### Backend
```bash
cd backend
python3 main_service.py
```

### Frontend
```bash
cd frontend
npm run serve
```

O sistema estará disponível em:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:8081

## 📊 Estrutura do Projeto

```
controle-financeiro/
├── backend/
│   ├── main_service.py          # Servidor FastAPI principal
│   ├── models.py                # Modelos Pydantic
│   ├── google_sheets_service.py # Integração com Google Sheets
│   ├── utils.py                 # Funções utilitárias
│   ├── requirements.txt         # Dependências Python
│   └── service-account.json     # Credenciais Google (não versionado)
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── Dashboard.vue    # Página principal
│   │   │   └── Items.vue        # Gerenciamento de itens
│   │   └── App.vue              # Componente raiz
│   ├── package.json             # Dependências Node.js
│   └── vue.config.js            # Configuração Vue CLI
├── .env                         # Variáveis de ambiente (não versionado)
├── .gitignore                   # Arquivos ignorados pelo Git
└── README.md                    # Este arquivo
```

## 🎯 Como Usar

1. **Criar Conta**: Adicione uma nova conta com nome, valor, parcelas e percentuais
2. **Conta Fixa**: Marque como "conta fixa" para definir valores manuais por pessoa
3. **Ajustar Percentuais**: O sistema ajusta automaticamente para manter 100%
4. **Marcar Pagamentos**: Use os checkboxes para marcar contas como pagas
5. **Acompanhar Resumos**: Veja o resumo individual de cada pessoa

## 🔧 API Endpoints

- `GET /health` - Status do sistema
- `GET /payments/items` - Lista todos os itens
- `POST /payments/items` - Cria novo item
- `PUT /payments/items/{id}` - Atualiza item
- `DELETE /payments/items/{id}` - Remove item
- `GET /payments/summary` - Resumo dos pagamentos

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## 📞 Suporte

Para dúvidas ou suporte, abra uma issue no repositório.