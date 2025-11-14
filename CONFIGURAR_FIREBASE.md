# Guia de Configuração do Firebase

## 📋 Informações do Projeto

- **Projeto Firebase:** `controle-finaceiro-d7784`
- **Service Account Email:** `firebase-adminsdk-fbsvc@controle-finaceiro-d7784.iam.gserviceaccount.com`

## 🔧 Passo 1: Obter Configuração do Frontend

### 1.1. Acessar Firebase Console

1. Acesse: https://console.firebase.google.com/
2. Selecione o projeto: **controle-finaceiro-d7784**

### 1.2. Obter Credenciais do Web App

1. Clique no **ícone de engrenagem** (⚙️) > **Project settings**
2. Role até a seção **Your apps**
3. Se já existe um app Web, clique nele
4. Se não existe, clique em **Add app** > **Web** (`</>`)
5. Registre o app (pode usar qualquer nome, ex: "Controle Pagamentos Web")
6. Copie as seguintes informações:

```
apiKey: "AIza..."
authDomain: "controle-finaceiro-d7784.firebaseapp.com"
projectId: "controle-finaceiro-d7784"
storageBucket: "controle-finaceiro-d7784.appspot.com"
messagingSenderId: "123456789"
appId: "1:123456789:web:abcdef"
```

### 1.3. Configurar Variáveis do Frontend

**Para desenvolvimento local:**

1. Copie o arquivo de exemplo:
```bash
cd frontend
cp .env.example .env
```

2. Edite o arquivo `.env` e preencha com os valores obtidos:
```env
VUE_APP_FIREBASE_API_KEY=AIza... (cole o apiKey)
VUE_APP_FIREBASE_AUTH_DOMAIN=controle-finaceiro-d7784.firebaseapp.com
VUE_APP_FIREBASE_PROJECT_ID=controle-finaceiro-d7784
VUE_APP_FIREBASE_STORAGE_BUCKET=controle-finaceiro-d7784.appspot.com
VUE_APP_FIREBASE_MESSAGING_SENDER_ID=123456789 (cole o messagingSenderId)
VUE_APP_FIREBASE_APP_ID=1:123456789:web:abcdef (cole o appId)
```

**Para produção (Railway):**

Configure as mesmas variáveis no painel do Railway (Frontend service):
- `VUE_APP_FIREBASE_API_KEY`
- `VUE_APP_FIREBASE_AUTH_DOMAIN`
- `VUE_APP_FIREBASE_PROJECT_ID`
- `VUE_APP_FIREBASE_STORAGE_BUCKET`
- `VUE_APP_FIREBASE_MESSAGING_SENDER_ID`
- `VUE_APP_FIREBASE_APP_ID`

## 🔐 Passo 2: Obter Credenciais do Backend (Firebase Admin)

### 2.1. Baixar Service Account JSON

1. No Firebase Console, vá em **Project settings** > **Service accounts**
2. Clique em **Generate new private key**
3. Confirme clicando em **Generate key**
4. O arquivo JSON será baixado automaticamente

### 2.2. Configurar Credenciais do Backend

**Opção A: Arquivo Local (Desenvolvimento)**

1. Renomeie o arquivo baixado para `firebase-admin-credentials.json`
2. Mova para a pasta `backend/`:
```bash
mv ~/Downloads/controle-finaceiro-d7784-xxxxx.json backend/firebase-admin-credentials.json
```

3. O arquivo já está no `.gitignore`, então não será commitado

**Opção B: Base64 para Railway (Produção)**

1. Converta o arquivo JSON para base64:
```bash
# macOS
base64 -i backend/firebase-admin-credentials.json | pbcopy

# Linux
base64 backend/firebase-admin-credentials.json | xclip -selection clipboard
```

2. No Railway (Backend service), adicione a variável:
   - Nome: `FIREBASE_ADMIN_CREDENTIALS_BASE64`
   - Valor: (cole o conteúdo base64 copiado)

**Opção C: Variáveis Individuais (Alternativa)**

Se preferir usar variáveis individuais no Railway:

1. Abra o arquivo `firebase-admin-credentials.json`
2. Configure no Railway:
   - `FIREBASE_ADMIN_PROJECT_ID` = `controle-finaceiro-d7784`
   - `FIREBASE_ADMIN_CLIENT_EMAIL` = `firebase-adminsdk-fbsvc@controle-finaceiro-d7784.iam.gserviceaccount.com`
   - `FIREBASE_ADMIN_PRIVATE_KEY` = (cole o valor de `private_key`, mantendo `\n` para quebras de linha)
   - `FIREBASE_ADMIN_PRIVATE_KEY_ID` = (valor de `private_key_id`)
   - `FIREBASE_ADMIN_CLIENT_ID` = (valor de `client_id`)

## ✅ Passo 3: Ativar Authentication

### 3.1. Ativar Email/Password no Firebase

1. No Firebase Console, vá em **Authentication**
2. Clique em **Get started** (se for a primeira vez)
3. Vá na aba **Sign-in method**
4. Clique em **Email/Password**
5. Ative o primeiro toggle (Email/Password)
6. Clique em **Save**

### 3.2. Criar Usuário de Teste

1. Vá em **Authentication** > **Users**
2. Clique em **Add user**
3. Digite:
   - Email: `teste@exemplo.com`
   - Senha: (escolha uma senha)
4. Clique em **Add user**

## 🚀 Passo 4: Instalar Dependências

### Backend
```bash
cd backend
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## 🧪 Passo 5: Testar

1. Inicie o backend:
```bash
cd backend
python main_service.py
```

2. Em outro terminal, inicie o frontend:
```bash
cd frontend
npm run serve
```

3. Acesse `http://localhost:8081`
4. Você será redirecionado para `/login`
5. Faça login com o usuário criado no passo 3.2

## 📝 Checklist

- [ ] Variáveis do frontend configuradas (`.env` ou Railway)
- [ ] Credenciais do backend configuradas (arquivo ou Railway)
- [ ] Authentication ativado no Firebase Console
- [ ] Usuário de teste criado
- [ ] Dependências instaladas
- [ ] Teste de login funcionando

## 🔍 Verificação Rápida

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

O arquivo deve existir (ou as variáveis devem estar no Railway).

## 🆘 Troubleshooting

### Erro: "Variáveis de ambiente do Firebase não configuradas"
- Verifique se o arquivo `.env` existe em `frontend/`
- Verifique se todas as variáveis começam com `VUE_APP_`
- Reinicie o servidor de desenvolvimento após criar/editar `.env`

### Erro: "Firebase Admin SDK não está instalado"
```bash
cd backend
pip install firebase-admin
```

### Erro: "Token de autenticação inválido"
- Verifique se as credenciais do Firebase Admin estão corretas
- Verifique se o arquivo JSON está completo
- Verifique se o base64 foi copiado completamente (pode ser muito longo)

### Erro: "Email já está em uso"
- O usuário já existe no Firebase
- Use outro email ou faça login com o existente

