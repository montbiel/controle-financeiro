# Planejamento: Implementação de Login com Firebase

## Objetivo

Implementar autenticação de usuários usando Firebase Authentication para proteger o acesso ao sistema de controle de pagamentos.

## Análise do Sistema Atual

### Estado Atual
- ✅ Sistema sem autenticação (acesso público)
- ✅ Frontend Vue.js 3 com Vue Router
- ✅ Backend FastAPI sem proteção de rotas
- ✅ Integração com Google Sheets (Service Account)
- ✅ Sistema funcionando em produção (Railway)
- ✅ Padrão visual estabelecido (Bootstrap 5, cores primárias, Font Awesome)

### Requisitos da Implementação
- 🔐 Autenticação via Firebase (Email/Password)
- 🛡️ Proteção de rotas no frontend
- 🔒 Validação de tokens no backend
- 👤 Gerenciamento de usuários
- 🔄 Manutenção da funcionalidade existente

## Especificações da Tela de Login

### Conceito Principal
- **Tela de entrada:** A tela de login será uma nova página que **precede a entrada no app**
- **Fluxo:** Usuário deve fazer login antes de acessar qualquer funcionalidade do sistema
- **Redirecionamento:** Todas as rotas protegidas redirecionam para `/login` se não autenticado

### Design e Padrão Visual
- **Consistência:** Seguir o padrão visual já construído no projeto
- **Framework:** Bootstrap 5 (já utilizado)
- **Cores:** Usar cores primárias do projeto (`bg-primary`, `text-primary`)
- **Componentes:** Cards com sombra e bordas arredondadas (padrão do projeto)
- **Ícones:** Font Awesome (já utilizado no projeto)

### Funcionalidades da Tela de Login

#### 1. Campo de Email
- Input type="email"
- Validação de formato de email
- Placeholder: "Digite seu email"
- Ícone Font Awesome: `fa-envelope`

#### 2. Campo de Senha com Mostrar/Ocultar
- Input type="password" por padrão
- **Botão discreto com ícone de olho:**
  - Posicionado dentro do input (usar `input-group` do Bootstrap)
  - Ícone: `fa-eye` quando senha oculta, `fa-eye-slash` quando senha visível
  - Estilo discreto (botão sem borda, apenas ícone)
  - Ao clicar: alterna entre mostrar/ocultar senha
- Placeholder: "Digite sua senha"

#### 3. Checkbox "Manter-me logado"
- **Posicionamento:** Abaixo do campo de senha
- **Funcionalidade:**
  - Se marcado: Usuário permanece logado até fazer logout manual (usar `localStorage`)
  - Se desmarcado: Usuário é deslogado ao fechar o navegador (usar `sessionStorage`)
- **Texto:** "Manter-me logado"
- **Estilo:** Seguir padrão Bootstrap de checkboxes

#### 4. Botão de Login
- Estilizado com `btn btn-primary` (padrão do projeto)
- Texto: "Entrar" ou "Login"
- Ícone: `fa-sign-in-alt` ou `fa-lock`
- Estado de loading: Mostrar spinner e desabilitar durante autenticação
- Largura: 100% do container (ou tamanho adequado)

#### 5. Tratamento de Erros
- Alertas Bootstrap (`alert alert-danger`)
- Mensagens de erro amigáveis traduzidas
- Exibir erros do Firebase de forma clara
- Posicionamento: Acima do formulário ou abaixo dos campos

#### 6. Layout da Tela
- Card centralizado na tela
- Título: "Login" ou "Acesso ao Sistema"
- Subtítulo opcional: "Sistema de Controle de Pagamentos"
- Responsivo: Funcionar bem em mobile e desktop
- Background: Pode usar cor de fundo suave ou gradiente (seguir padrão do projeto)

## Arquitetura Proposta

### Frontend (Vue.js)
1. **Firebase SDK** - Integração com Firebase Auth
2. **Composables/Services** - Gerenciamento de autenticação
3. **Router Guards** - Proteção de rotas
4. **Componentes** - Login, Logout, Perfil
5. **Store/State** - Estado de autenticação

### Backend (FastAPI)
1. **Firebase Admin SDK** - Validação de tokens
2. **Middleware** - Verificação de autenticação
3. **Dependencies** - Proteção de endpoints
4. **Modelos** - Dados de usuário (se necessário)

## Estrutura de Implementação

### 1. Configuração Inicial

#### 1.1. Criar Projeto Firebase
- [ ] Criar projeto no Firebase Console
- [ ] Habilitar Authentication (Email/Password)
- [ ] Obter configuração do Firebase (firebaseConfig)
- [ ] Configurar domínios autorizados (montbiel.com.br, localhost)

#### 1.2. Instalar Dependências

**Frontend:**
```json
{
  "firebase": "^10.7.0"
}
```

**Backend:**
```txt
firebase-admin>=6.0.0
```

### 2. Frontend - Estrutura de Arquivos

```
frontend/src/
├── firebase/
│   └── config.js          # Configuração do Firebase
├── services/
│   ├── auth.js            # Serviço de autenticação
│   └── api.js             # Atualizar para incluir token
├── composables/
│   └── useAuth.js         # Composable para autenticação
├── router/
│   └── index.js           # Adicionar guards de rota
├── views/
│   ├── Login.vue          # Página de login
│   └── Dashboard.vue      # Proteger com autenticação
├── components/
│   └── AuthGuard.vue      # Componente de proteção (opcional)
└── App.vue                 # Adicionar lógica de autenticação
```

### 3. Backend - Estrutura de Arquivos

```
backend/
├── firebase/
│   └── admin.py           # Inicialização Firebase Admin
├── middleware/
│   └── auth.py            # Middleware de autenticação
├── dependencies/
│   └── auth.py            # Dependencies para FastAPI
└── main_service.py        # Adicionar proteção nas rotas
```

## Implementação Detalhada

### Fase 1: Configuração Base

#### 1.1. Frontend - Configuração Firebase
- Criar `frontend/src/firebase/config.js`
- Inicializar Firebase App
- Exportar `auth` e `db` (se necessário)

#### 1.2. Backend - Configuração Firebase Admin
- Criar `backend/firebase/admin.py`
- Inicializar Firebase Admin SDK
- Usar Service Account ou variável de ambiente

### Fase 2: Serviço de Autenticação (Frontend)

#### 2.1. Criar `frontend/src/services/auth.js`
- Funções: `login()`, `logout()`, `register()`, `getCurrentUser()`
- Gerenciar estado de autenticação
- **Persistir sessão:**
  - Se checkbox "Manter-me logado" estiver marcado: usar `localStorage` (persiste após fechar navegador)
  - Se não estiver marcado: usar `sessionStorage` (apenas durante a sessão)
  - Implementar lógica de "remember me" para manter usuário logado até logout manual

#### 2.2. Criar `frontend/src/composables/useAuth.js`
- Composable Vue 3 para usar em componentes
- Estado reativo de autenticação
- Métodos de login/logout

### Fase 3: Proteção de Rotas (Frontend)

#### 3.1. Atualizar `frontend/src/router/index.js`
- Adicionar `beforeEach` guard
- Verificar autenticação antes de acessar rotas
- **Tela de login como entrada:** Todas as rotas protegidas redirecionam para `/login` se não autenticado
- Criar rota `/login` como rota pública
- Rota `/login` redireciona para `/dashboard` se já estiver autenticado

#### 3.2. Criar `frontend/src/views/Login.vue`
- **Tela de entrada:** Nova tela que precede a entrada no app
- **Padrão visual:** Seguir o padrão visual já construído no projeto (Bootstrap 5, cards, cores primárias)
- **Formulário de login:**
  - Campo de email
  - Campo de senha com funcionalidade de mostrar/ocultar
  - Botão discreto com ícone de olho para exibir/ocultar senha
  - Checkbox "Manter-me logado" (remember me)
  - Botão de login estilizado seguindo padrão do projeto
- **Validação de campos:**
  - Email válido
  - Senha não vazia
  - Feedback visual de erros
- **Tratamento de erros:**
  - Mensagens de erro amigáveis
  - Exibir erros do Firebase de forma clara
- **Redirecionamento após login:**
  - Redirecionar para `/dashboard` após login bem-sucedido
  - Se houver rota de destino salva, redirecionar para ela

### Fase 4: Proteção de API (Backend)

#### 4.1. Criar `backend/middleware/auth.py`
- Função para verificar token Firebase
- Extrair token do header Authorization
- Validar token com Firebase Admin

#### 4.2. Criar `backend/dependencies/auth.py`
- Dependency do FastAPI para proteger rotas
- Retornar dados do usuário autenticado
- Lançar HTTPException se não autenticado

#### 4.3. Atualizar `backend/main_service.py`
- Adicionar dependency de autenticação nas rotas
- Proteger endpoints sensíveis:
  - POST /payments/items
  - PUT /payments/items/{id}
  - DELETE /payments/items/{id}
  - PUT /payments/items/{id}/installments/pay
- Manter GET endpoints públicos (ou proteger também)

### Fase 5: Integração Frontend-Backend

#### 5.1. Atualizar `frontend/src/services/api.js`
- Adicionar interceptor para incluir token
- Adicionar token no header Authorization
- Tratar erros 401 (não autenticado)
- Redirecionar para login em caso de erro

#### 5.2. Atualizar `frontend/src/App.vue`
- Adicionar botão de logout no navbar
- Mostrar informações do usuário logado
- Gerenciar estado de autenticação

### Fase 6: Melhorias e UX

#### 6.1. Componentes Visuais da Tela de Login
- **Design consistente:**
  - Usar Bootstrap 5 (já utilizado no projeto)
  - Cores primárias do projeto (bg-primary, text-primary)
  - Cards com sombra e bordas arredondadas
  - Ícones Font Awesome (já utilizado no projeto)
- **Campo de senha:**
  - Input type="password" por padrão
  - Botão discreto com ícone de olho (`fa-eye` / `fa-eye-slash`)
  - Posicionado dentro do input (input-group)
  - Alternar entre mostrar/ocultar senha ao clicar
- **Checkbox "Manter-me logado":**
  - Estilizado seguindo padrão Bootstrap
  - Texto claro: "Manter-me logado"
  - Posicionado abaixo do campo de senha
- **Loading state:**
  - Spinner durante autenticação
  - Desabilitar botão durante processo
- **Mensagens de erro:**
  - Alertas Bootstrap (alert-danger)
  - Mensagens amigáveis traduzidas
  - Feedback visual claro

#### 6.2. Persistência de Sessão
- **"Manter-me logado" implementado:**
  - Checkbox marcado: usar `localStorage` (persiste indefinidamente até logout)
  - Checkbox desmarcado: usar `sessionStorage` (apenas durante sessão do navegador)
  - Verificar sessão salva ao iniciar app
  - Logout manual limpa ambos os storages
- **Gerenciar expiração de token:**
  - Verificar validade do token ao iniciar
  - Refresh automático de token quando necessário
  - Redirecionar para login se token expirado

## Variáveis de Ambiente

### Frontend (Railway)
```
VUE_APP_FIREBASE_API_KEY=...
VUE_APP_FIREBASE_AUTH_DOMAIN=...
VUE_APP_FIREBASE_PROJECT_ID=...
VUE_APP_FIREBASE_STORAGE_BUCKET=...
VUE_APP_FIREBASE_MESSAGING_SENDER_ID=...
VUE_APP_FIREBASE_APP_ID=...
```

### Backend (Railway)
```
FIREBASE_ADMIN_CREDENTIALS_BASE64=... (JSON em base64)
# OU
FIREBASE_ADMIN_PROJECT_ID=...
FIREBASE_ADMIN_PRIVATE_KEY=...
FIREBASE_ADMIN_CLIENT_EMAIL=...
```

## Fluxo de Autenticação

### Login
1. Usuário acessa `/login`
2. Preenche email e senha
3. Firebase Auth valida credenciais
4. Retorna token ID
5. Token é armazenado (localStorage)
6. Redireciona para `/dashboard`
7. Token é enviado em todas as requisições

### Acesso a Rota Protegida
1. Usuário tenta acessar rota protegida
2. Router guard verifica autenticação
3. Se não autenticado → redireciona para `/login`
4. Se autenticado → permite acesso

### Requisição à API
1. Frontend faz requisição
2. Interceptor adiciona token no header
3. Backend recebe requisição
4. Middleware valida token com Firebase Admin
5. Se válido → processa requisição
6. Se inválido → retorna 401

## Decisões de Design

### Rotas Protegidas
- ✅ Dashboard (`/`) - Proteger
- ✅ Items (`/items`) - Proteger
- ❌ Login (`/login`) - Público
- ❌ Health (`/health`) - Público (para monitoramento)

### Endpoints Protegidos
- ✅ POST /payments/items - Criar item
- ✅ PUT /payments/items/{id} - Atualizar item
- ✅ DELETE /payments/items/{id} - Deletar item
- ✅ PUT /payments/items/{id}/installments/pay - Marcar como pago
- ❓ GET /payments/summary - Decidir (pode ser público ou protegido)
- ❓ GET /payments/items - Decidir (pode ser público ou protegido)

### Gerenciamento de Usuários
- Opção 1: Apenas Firebase Auth (sem banco próprio)
- Opção 2: Sincronizar usuários com Google Sheets
- Opção 3: Criar tabela de usuários no Google Sheets

**Recomendação:** Opção 1 (mais simples, Firebase gerencia tudo)

## Testes Necessários

### Frontend
- [ ] Login com credenciais válidas
- [ ] Login com credenciais inválidas
- [ ] Logout funciona corretamente
- [ ] Rotas protegidas redirecionam se não autenticado
- [ ] Token é enviado nas requisições
- [ ] Sessão persiste após refresh

### Backend
- [ ] Token válido permite acesso
- [ ] Token inválido retorna 401
- [ ] Token expirado retorna 401
- [ ] Requisições sem token retornam 401
- [ ] Endpoints públicos funcionam sem token

## Migração e Compatibilidade

### Estratégia de Migração
1. Implementar em branch separada (✅ já feito)
2. Manter funcionalidade existente funcionando
3. Adicionar autenticação de forma incremental
4. Testar em ambiente de desenvolvimento
5. Fazer merge apenas quando estável

### Compatibilidade
- ✅ Sistema atual continua funcionando
- ✅ Autenticação é opcional inicialmente (pode fazer gradual)
- ✅ Dados existentes não são afetados

## Próximos Passos

1. ✅ Criar branch `feature/firebase-login`
2. ⏭️ Configurar projeto Firebase
3. ⏭️ Instalar dependências
4. ⏭️ Implementar configuração base
5. ⏭️ Implementar serviço de autenticação (frontend)
6. ⏭️ Implementar proteção de rotas (frontend)
7. ⏭️ Implementar validação de token (backend)
8. ⏭️ Proteger endpoints (backend)
9. ⏭️ Testar integração completa
10. ⏭️ Fazer merge na main

## Referências

- [Firebase Authentication Docs](https://firebase.google.com/docs/auth)
- [Firebase Admin SDK Python](https://firebase.google.com/docs/admin/setup)
- [Vue Router Navigation Guards](https://router.vuejs.org/guide/advanced/navigation-guards.html)
- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

