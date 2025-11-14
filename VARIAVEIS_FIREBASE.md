# Variáveis do Firebase - Referência Rápida

## 📋 Informações do Projeto

- **Projeto Firebase:** `controle-finaceiro-d7784`
- **Service Account Email:** `firebase-adminsdk-fbsvc@controle-finaceiro-d7784.iam.gserviceaccount.com`
- **Auth Domain:** `controle-finaceiro-d7784.firebaseapp.com`
- **Storage Bucket:** `controle-finaceiro-d7784.appspot.com`

## 🔧 Frontend - Variáveis Necessárias

Crie o arquivo `frontend/.env` com:

```env
VUE_APP_FIREBASE_API_KEY=<obter no Firebase Console>
VUE_APP_FIREBASE_AUTH_DOMAIN=controle-finaceiro-d7784.firebaseapp.com
VUE_APP_FIREBASE_PROJECT_ID=controle-finaceiro-d7784
VUE_APP_FIREBASE_STORAGE_BUCKET=controle-finaceiro-d7784.appspot.com
VUE_APP_FIREBASE_MESSAGING_SENDER_ID=<obter no Firebase Console>
VUE_APP_FIREBASE_APP_ID=<obter no Firebase Console>
```

### Onde obter as variáveis faltantes:

1. Acesse: https://console.firebase.google.com/project/controle-finaceiro-d7784/settings/general
2. Role até **Your apps** > **Web app**
3. Se não existe, clique em **Add app** > **Web** (`</>`)
4. Copie:
   - `apiKey` → `VUE_APP_FIREBASE_API_KEY`
   - `messagingSenderId` → `VUE_APP_FIREBASE_MESSAGING_SENDER_ID`
   - `appId` → `VUE_APP_FIREBASE_APP_ID`

## 🔐 Backend - Configuração

### Opção 1: Arquivo Local (Desenvolvimento)

1. Baixe o Service Account JSON:
   - Acesse: https://console.firebase.google.com/project/controle-finaceiro-d7784/settings/serviceaccounts/adminsdk
   - Clique em **Generate new private key**
   - Baixe o arquivo JSON

2. Renomeie e mova:
```bash
mv ~/Downloads/controle-finaceiro-d7784-*.json backend/firebase-admin-credentials.json
```

### Opção 2: Base64 para Railway (Produção)

1. Converta o JSON para base64:
```bash
base64 -i backend/firebase-admin-credentials.json | pbcopy
```

2. No Railway (Backend service), adicione:
   - Nome: `FIREBASE_ADMIN_CREDENTIALS_BASE64`
   - Valor: (cole o base64 copiado)

### Opção 3: Variáveis Individuais (Railway)

Configure no Railway:
- `FIREBASE_ADMIN_PROJECT_ID` = `controle-finaceiro-d7784`
- `FIREBASE_ADMIN_CLIENT_EMAIL` = `firebase-adminsdk-fbsvc@controle-finaceiro-d7784.iam.gserviceaccount.com`
- `FIREBASE_ADMIN_PRIVATE_KEY` = (do arquivo JSON, campo `private_key`)
- `FIREBASE_ADMIN_PRIVATE_KEY_ID` = (do arquivo JSON, campo `private_key_id`)
- `FIREBASE_ADMIN_CLIENT_ID` = (do arquivo JSON, campo `client_id`)

## ✅ Checklist Rápido

- [ ] Frontend: Criar `frontend/.env` com todas as variáveis
- [ ] Backend: Baixar Service Account JSON ou configurar no Railway
- [ ] Firebase: Ativar Authentication > Email/Password
- [ ] Firebase: Criar usuário de teste
- [ ] Instalar dependências: `pip install -r requirements.txt` e `npm install`

## 🚀 Teste Rápido

```bash
# Terminal 1 - Backend
cd backend
python main_service.py

# Terminal 2 - Frontend
cd frontend
npm run serve
```

Acesse: http://localhost:8081

