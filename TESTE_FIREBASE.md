# 🧪 Teste do Firebase Authentication

## ✅ Status Atual

### Frontend
- ✅ Variáveis do Firebase configuradas em `frontend/.env`
- ✅ Firebase SDK instalado
- ✅ Servidor de desenvolvimento iniciado

### Backend
- ✅ Firebase Admin SDK instalado
- ✅ Servidor iniciado e respondendo em `http://localhost:8000`
- ⚠️ **Credenciais do Firebase Admin ainda não configuradas**

## ⚠️ Importante: Configurar Credenciais do Backend

Para que a autenticação funcione completamente, você precisa configurar as credenciais do Firebase Admin no backend.

### Opção 1: Arquivo Local (Recomendado para testes)

1. Baixe o Service Account JSON do Firebase:
   - Acesse: https://console.firebase.google.com/project/controle-finaceiro-d7784/settings/serviceaccounts/adminsdk
   - Clique em **Generate new private key**
   - Baixe o arquivo JSON

2. Renomeie e mova para a pasta backend:
```bash
mv ~/Downloads/controle-finaceiro-d7784-*.json backend/firebase-admin-credentials.json
```

3. Reinicie o backend

### Opção 2: Variáveis de Ambiente (Para Railway)

Configure no Railway:
- `FIREBASE_ADMIN_CREDENTIALS_BASE64` = (base64 do JSON)

## 🚀 Como Testar

### 1. Acessar o Sistema

1. Abra o navegador em: **http://localhost:8081**
2. Você será redirecionado automaticamente para `/login`

### 2. Criar Usuário no Firebase Console

Se ainda não criou um usuário:

1. Acesse: https://console.firebase.google.com/project/controle-finaceiro-d7784/authentication/users
2. Clique em **Add user**
3. Preencha:
   - Email: `teste@exemplo.com`
   - Senha: (escolha uma senha)
4. Clique em **Add user**

### 3. Fazer Login

1. Na tela de login, digite:
   - Email: `teste@exemplo.com` (ou o email criado)
   - Senha: (a senha criada)
2. Opcionalmente, marque "Manter-me logado"
3. Clique em **Entrar**

### 4. Testar Funcionalidades

Após fazer login, você deve conseguir:
- ✅ Ver o Dashboard
- ✅ Ver a lista de Itens
- ✅ Marcar parcelas como pagas
- ✅ Ver informações do usuário no navbar
- ✅ Fazer logout

## 🔍 Verificar Logs

### Backend
Os logs do backend mostrarão:
- Se o Firebase Admin foi inicializado corretamente
- Erros de autenticação (se houver)
- Requisições recebidas

### Frontend
Abra o Console do navegador (F12) para ver:
- Erros de conexão com Firebase
- Erros de autenticação
- Logs de requisições à API

## 🐛 Troubleshooting

### Erro: "Token de autenticação inválido"
- Verifique se as credenciais do Firebase Admin estão configuradas
- Verifique se o arquivo JSON está no lugar correto
- Reinicie o backend após configurar

### Erro: "Firebase Admin SDK não está instalado"
```bash
cd backend
python3 -m pip install firebase-admin
```

### Erro: "Variáveis de ambiente do Firebase não configuradas"
- Verifique se `frontend/.env` existe
- Verifique se todas as variáveis estão preenchidas
- Reinicie o servidor de desenvolvimento

### Erro: "Email/senha incorretos"
- Verifique se o usuário existe no Firebase Console
- Verifique se Authentication > Email/Password está ativado
- Tente criar um novo usuário

### Frontend não redireciona para login
- Limpe o cache do navegador
- Verifique se o router está funcionando
- Verifique os logs do console

## 📝 Checklist de Teste

- [ ] Backend rodando em http://localhost:8000
- [ ] Frontend rodando em http://localhost:8081
- [ ] Credenciais do Firebase Admin configuradas
- [ ] Usuário criado no Firebase Console
- [ ] Authentication > Email/Password ativado
- [ ] Login funcionando
- [ ] Redirecionamento após login funcionando
- [ ] Logout funcionando
- [ ] Proteção de rotas funcionando
- [ ] API protegida funcionando

## 🎯 Próximos Passos

Após confirmar que tudo está funcionando:

1. **Testar "Manter-me logado":**
   - Faça login marcando o checkbox
   - Feche o navegador
   - Abra novamente - deve permanecer logado

2. **Testar sem "Manter-me logado":**
   - Faça login sem marcar o checkbox
   - Feche o navegador
   - Abra novamente - deve pedir login

3. **Testar proteção de rotas:**
   - Faça logout
   - Tente acessar `/` diretamente
   - Deve redirecionar para `/login`

4. **Testar API protegida:**
   - Tente fazer uma requisição sem token
   - Deve retornar 401
   - Após login, deve funcionar normalmente

