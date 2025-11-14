# Configuração do Firebase Authentication

## ✅ Implementação Concluída

A funcionalidade de login com Firebase foi implementada seguindo o planejamento. Todas as fases foram concluídas:

### Frontend
- ✅ Configuração do Firebase SDK (`frontend/src/firebase/config.js`)
- ✅ Serviço de autenticação (`frontend/src/services/auth.js`)
- ✅ Composable Vue 3 (`frontend/src/composables/useAuth.js`)
- ✅ Tela de Login (`frontend/src/views/Login.vue`)
- ✅ Proteção de rotas no router
- ✅ Interceptor para adicionar token nas requisições
- ✅ Navbar com logout e informações do usuário

### Backend
- ✅ Configuração do Firebase Admin SDK (`backend/firebase/admin.py`)
- ✅ Dependencies de autenticação (`backend/dependencies/auth.py`)
- ✅ Middleware de autenticação (`backend/middleware/auth.py`)
- ✅ Endpoints protegidos (POST, PUT, DELETE)

## 🔧 Configuração Necessária

### 1. Criar Projeto no Firebase Console

1. Acesse [Firebase Console](https://console.firebase.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Ative **Authentication** > **Sign-in method** > **Email/Password**

### 2. Configurar Frontend

#### 2.1. Obter Configuração do Firebase

No Firebase Console:
1. Vá em **Project Settings** (ícone de engrenagem)
2. Role até **Your apps** e clique em **Web** (`</>`)
3. Registre o app e copie as credenciais

#### 2.2. Configurar Variáveis de Ambiente

**Para desenvolvimento local:**

Crie um arquivo `.env` na pasta `frontend/`:

```env
VUE_APP_FIREBASE_API_KEY=your-api-key
VUE_APP_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VUE_APP_FIREBASE_PROJECT_ID=your-project-id
VUE_APP_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VUE_APP_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VUE_APP_FIREBASE_APP_ID=your-app-id
```

**Para produção (Railway):**

Configure as mesmas variáveis no painel do Railway (Frontend service):
- `VUE_APP_FIREBASE_API_KEY`
- `VUE_APP_FIREBASE_AUTH_DOMAIN`
- `VUE_APP_FIREBASE_PROJECT_ID`
- `VUE_APP_FIREBASE_STORAGE_BUCKET`
- `VUE_APP_FIREBASE_MESSAGING_SENDER_ID`
- `VUE_APP_FIREBASE_APP_ID`

### 3. Configurar Backend

#### 3.1. Obter Service Account do Firebase

No Firebase Console:
1. Vá em **Project Settings**
2. Aba **Service accounts**
3. Clique em **Generate new private key**
4. Baixe o arquivo JSON

#### 3.2. Configurar Credenciais

**Opção 1: Variável de Ambiente Base64 (Recomendado para Railway)**

```bash
# Converter o JSON para base64
base64 -i firebase-admin-credentials.json | pbcopy  # macOS
# ou
base64 firebase-admin-credentials.json | pbcopy      # Linux
```

Configure no Railway (Backend service):
- `FIREBASE_ADMIN_CREDENTIALS_BASE64` = (cole o conteúdo base64)

**Opção 2: Arquivo Local (Desenvolvimento)**

1. Copie o arquivo JSON para `backend/firebase-admin-credentials.json`
2. Adicione ao `.gitignore`:

```gitignore
backend/firebase-admin-credentials.json
```

**Opção 3: Variáveis Individuais**

Configure no Railway:
- `FIREBASE_ADMIN_PROJECT_ID`
- `FIREBASE_ADMIN_PRIVATE_KEY` (com `\n` para quebras de linha)
- `FIREBASE_ADMIN_CLIENT_EMAIL`
- `FIREBASE_ADMIN_PRIVATE_KEY_ID` (opcional)
- `FIREBASE_ADMIN_CLIENT_ID` (opcional)

### 4. Instalar Dependências

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

## 🚀 Testando a Implementação

### 1. Criar Usuário de Teste

No Firebase Console:
1. Vá em **Authentication** > **Users**
2. Clique em **Add user**
3. Digite email e senha
4. Clique em **Add user**

### 2. Testar Login

1. Inicie o backend:
```bash
cd backend
python main_service.py
```

2. Inicie o frontend:
```bash
cd frontend
npm run serve
```

3. Acesse `http://localhost:8081`
4. Você será redirecionado para `/login`
5. Faça login com o usuário criado

### 3. Funcionalidades da Tela de Login

- ✅ Campo de email com validação
- ✅ Campo de senha com botão de mostrar/ocultar (ícone de olho)
- ✅ Checkbox "Manter-me logado"
  - Marcado: usa `localStorage` (permanece logado até logout)
  - Desmarcado: usa `sessionStorage` (desloga ao fechar navegador)
- ✅ Validação de formulário
- ✅ Mensagens de erro amigáveis
- ✅ Loading state durante autenticação

## 📝 Notas Importantes

1. **Rotas Protegidas:**
   - `/` (Dashboard)
   - `/items`
   - Todas redirecionam para `/login` se não autenticado

2. **Rotas Públicas:**
   - `/login`
   - `/health` (endpoint de saúde da API)

3. **Endpoints Protegidos no Backend:**
   - `POST /payments/items`
   - `PUT /payments/items/{item_id}`
   - `PUT /payments/items/{item_id}/installments/pay`
   - `DELETE /payments/items/{item_id}`

4. **Endpoints Públicos no Backend:**
   - `GET /health`
   - `GET /payments/summary`
   - `GET /payments/items`

## 🔒 Segurança

- Tokens são validados no backend usando Firebase Admin SDK
- Tokens expirados são rejeitados automaticamente
- Erro 401 redireciona para login automaticamente
- Tokens são enviados via header `Authorization: Bearer <token>`

## 🐛 Troubleshooting

### Erro: "Firebase Admin SDK não está instalado"
```bash
cd backend
pip install firebase-admin
```

### Erro: "Variáveis de ambiente do Firebase não configuradas"
Verifique se todas as variáveis `VUE_APP_FIREBASE_*` estão configuradas.

### Erro: "Token de autenticação inválido"
- Verifique se as credenciais do Firebase Admin estão corretas
- Verifique se o token não expirou
- Verifique se o projeto Firebase está correto

### Erro: "CORS"
Verifique se `CORS_ORIGINS` no backend inclui o domínio do frontend.

