# 🎯 Como Obter as Variáveis do Firebase

## Passo a Passo Visual

### 1️⃣ Acessar Firebase Console

1. Acesse: https://console.firebase.google.com/
2. Faça login (se necessário)
3. Selecione o projeto: **controle-finaceiro-d7784**

### 2️⃣ Obter Variáveis do Frontend

#### 2.1. Ir para Configurações do Projeto

1. Clique no **ícone de engrenagem** (⚙️) no canto superior esquerdo
2. Clique em **Project settings**

#### 2.2. Encontrar ou Criar App Web

1. Role a página até a seção **Your apps**
2. Se já existe um app Web:
   - Clique no app Web existente
   - As configurações aparecerão abaixo
3. Se **NÃO existe** um app Web:
   - Clique no botão **Add app** ou no ícone `</>`
   - Escolha **Web**
   - Dê um nome (ex: "Controle Pagamentos")
   - Clique em **Register app**
   - As configurações aparecerão

#### 2.3. Copiar as Variáveis

Você verá um código JavaScript como este:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyC...",
  authDomain: "controle-finaceiro-d7784.firebaseapp.com",
  projectId: "controle-finaceiro-d7784",
  storageBucket: "controle-finaceiro-d7784.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef123456"
};
```

**Mapeamento para o arquivo `.env`:**

| Firebase Config | Variável .env | Valor |
|----------------|---------------|-------|
| `apiKey` | `VUE_APP_FIREBASE_API_KEY` | Cole o valor entre aspas |
| `authDomain` | `VUE_APP_FIREBASE_AUTH_DOMAIN` | `controle-finaceiro-d7784.firebaseapp.com` |
| `projectId` | `VUE_APP_FIREBASE_PROJECT_ID` | `controle-finaceiro-d7784` |
| `storageBucket` | `VUE_APP_FIREBASE_STORAGE_BUCKET` | `controle-finaceiro-d7784.appspot.com` |
| `messagingSenderId` | `VUE_APP_FIREBASE_MESSAGING_SENDER_ID` | Cole o valor numérico |
| `appId` | `VUE_APP_FIREBASE_APP_ID` | Cole o valor completo |

### 3️⃣ Editar o Arquivo .env

1. Abra o arquivo `frontend/.env`
2. Preencha as 3 variáveis que estão vazias:
   - `VUE_APP_FIREBASE_API_KEY` (cole o `apiKey`)
   - `VUE_APP_FIREBASE_MESSAGING_SENDER_ID` (cole o `messagingSenderId`)
   - `VUE_APP_FIREBASE_APP_ID` (cole o `appId`)

**Exemplo de arquivo `.env` preenchido:**

```env
VUE_APP_FIREBASE_API_KEY=AIzaSyC1234567890abcdefghijklmnopqrstuvwxyz
VUE_APP_FIREBASE_AUTH_DOMAIN=controle-finaceiro-d7784.firebaseapp.com
VUE_APP_FIREBASE_PROJECT_ID=controle-finaceiro-d7784
VUE_APP_FIREBASE_STORAGE_BUCKET=controle-finaceiro-d7784.appspot.com
VUE_APP_FIREBASE_MESSAGING_SENDER_ID=123456789012
VUE_APP_FIREBASE_APP_ID=1:123456789012:web:abcdef123456
```

### 4️⃣ Obter Credenciais do Backend

#### 4.1. Acessar Service Accounts

1. No Firebase Console, vá em **Project settings**
2. Clique na aba **Service accounts**
3. Você verá a seção **Firebase Admin SDK**

#### 4.2. Gerar Nova Chave Privada

1. Clique no botão **Generate new private key**
2. Uma mensagem aparecerá explicando sobre a chave privada
3. Clique em **Generate key**
4. Um arquivo JSON será baixado automaticamente

#### 4.3. Configurar no Backend

**Opção A: Arquivo Local (Desenvolvimento)**

1. Renomeie o arquivo baixado para `firebase-admin-credentials.json`
2. Mova para a pasta `backend/`:
```bash
mv ~/Downloads/controle-finaceiro-d7784-*.json backend/firebase-admin-credentials.json
```

**Opção B: Base64 para Railway**

1. Converta para base64:
```bash
base64 -i backend/firebase-admin-credentials.json | pbcopy
```

2. No Railway (Backend service):
   - Adicione variável: `FIREBASE_ADMIN_CREDENTIALS_BASE64`
   - Cole o valor copiado

### 5️⃣ Ativar Authentication

1. No Firebase Console, vá em **Authentication**
2. Se for a primeira vez, clique em **Get started**
3. Vá na aba **Sign-in method**
4. Clique em **Email/Password**
5. Ative o primeiro toggle (Email/Password)
6. Clique em **Save**

### 6️⃣ Criar Usuário de Teste

1. Vá em **Authentication** > **Users**
2. Clique em **Add user**
3. Preencha:
   - Email: `teste@exemplo.com`
   - Senha: (escolha uma senha forte)
4. Clique em **Add user**

## ✅ Verificação Final

### Frontend
```bash
cd frontend
cat .env | grep VUE_APP_FIREBASE
```

Deve mostrar todas as 6 variáveis preenchidas.

### Backend
```bash
cd backend
ls -la firebase-admin-credentials.json
```

O arquivo deve existir (ou variáveis configuradas no Railway).

## 🚀 Pronto para Testar!

Agora você pode:
1. Iniciar o backend: `cd backend && python main_service.py`
2. Iniciar o frontend: `cd frontend && npm run serve`
3. Acessar: http://localhost:8081
4. Fazer login com o usuário criado

