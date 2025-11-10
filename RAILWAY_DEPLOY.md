# Guia de Deploy na Railway

Este guia explica como fazer deploy do Sistema de Controle de Pagamentos na Railway com o domínio montbiel.com.br.

## Estrutura de Serviços

O projeto precisa de **dois serviços separados** na Railway:

1. **Backend** (Python/FastAPI) - API REST
2. **Frontend** (Vue.js) - Interface web

## Configuração do Backend

### 1. Criar Serviço Backend no Railway

1. Acesse [Railway](https://railway.app)
2. Crie um novo projeto
3. Adicione um novo serviço
4. Conecte ao repositório GitHub
5. Selecione a branch `main`

### 2. Configurar Build e Start

**Root Directory:** `/backend` (ou deixe vazio se usar Procfile)

**Start Command:** 
```
python main_service.py
```

Ou use o `Procfile.backend` renomeado para `Procfile` na raiz do projeto.

### 3. Variáveis de Ambiente do Backend

Configure as seguintes variáveis de ambiente no Railway:

```
GOOGLE_SHEETS_URL=https://docs.google.com/spreadsheets/d/SEU_ID_AQUI/edit
GOOGLE_SERVICE_ACCOUNT_BASE64=<base64_do_service_account_json>
SHEET_NAME=Pagamentos
CORS_ORIGINS=https://montbiel.com.br,https://www.montbiel.com.br,http://localhost:8081
```

**Para obter o base64 do service-account.json:**

```bash
# No terminal, execute:
base64 -i backend/service-account.json | pbcopy  # macOS
# ou
base64 backend/service-account.json | pbcopy   # Linux
```

Cole o resultado na variável `GOOGLE_SERVICE_ACCOUNT_BASE64`.

**Nota:** A variável `PORT` é fornecida automaticamente pelo Railway.

### 4. Configurar Domínio do Backend

1. No serviço backend, vá em **Settings** > **Domains**
2. Adicione um domínio customizado: `api.montbiel.com.br`
3. Configure o DNS conforme instruções do Railway

## Configuração do Frontend

### 1. Criar Serviço Frontend no Railway

1. No mesmo projeto Railway, adicione outro serviço
2. Conecte ao mesmo repositório GitHub
3. Selecione a branch `main`

### 2. Configurar Build e Start

**Root Directory:** `/frontend`

**Start Command:**
```
npm install && npm run start
```

Ou use o `Procfile.frontend` renomeado para `Procfile` na pasta frontend.

### 3. Variáveis de Ambiente do Frontend

Configure as seguintes variáveis de ambiente no Railway:

```
VUE_APP_API_URL=https://api.montbiel.com.br
NODE_ENV=production
```

**Nota:** Substitua `api.montbiel.com.br` pela URL real do seu backend no Railway.

### 4. Configurar Domínio do Frontend

1. No serviço frontend, vá em **Settings** > **Domains**
2. Adicione um domínio customizado: `montbiel.com.br`
3. Configure o DNS conforme instruções do Railway

## Configuração DNS

Configure os seguintes registros DNS no seu provedor de domínio:

```
Tipo: CNAME
Nome: api
Valor: <cname_do_railway_backend>

Tipo: CNAME
Nome: @ (ou montbiel.com.br)
Valor: <cname_do_railway_frontend>
```

## Desenvolvimento Local

Para desenvolvimento local, continue usando:

**Backend:**
```bash
cd backend
python main_service.py
```

**Frontend:**
```bash
cd frontend
npm run serve
```

O sistema detecta automaticamente o ambiente e usa:
- `http://localhost:8000` para a API em desenvolvimento
- `http://localhost:8081` para o frontend em desenvolvimento

## Verificação

Após o deploy:

1. Acesse `https://montbiel.com.br` - deve carregar o frontend
2. O frontend deve se conectar automaticamente a `https://api.montbiel.com.br`
3. Verifique os logs no Railway para garantir que não há erros

## Troubleshooting

### Backend não inicia
- Verifique se a variável `PORT` está sendo usada (Railway fornece automaticamente)
- Verifique os logs no Railway
- Certifique-se de que `GOOGLE_SERVICE_ACCOUNT_BASE64` está configurado corretamente

### Frontend não encontra a API
- Verifique se `VUE_APP_API_URL` está configurado corretamente
- Verifique se o CORS no backend permite o domínio do frontend
- Verifique os logs do frontend no navegador (F12 > Console)

### Erro de CORS
- Verifique se `CORS_ORIGINS` inclui o domínio do frontend
- Certifique-se de que está usando HTTPS em produção

