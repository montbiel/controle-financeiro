# Correção: Tela Branca no Frontend Railway

## Problema
O frontend na Railway está mostrando tela branca.

## Causas Possíveis

1. **Comando `serve` incorreto** - A ordem dos parâmetros estava errada
2. **Vue Router History Mode** - Precisa de configuração especial para SPAs
3. **Caminho base incorreto** - Pode estar tentando carregar recursos do caminho errado
4. **Firebase não configurado** - Se as variáveis de ambiente não estiverem configuradas, pode causar erro

## Correções Aplicadas

### 1. Corrigido comando `serve`
```json
"start": "npm run build && npx serve dist -s -l $PORT"
```
- Ordem correta: `serve dist -s -l $PORT`
- Flag `-s` habilita modo SPA (redireciona todas as rotas para index.html)

### 2. Adicionado `publicPath` no vue.config.js
```js
publicPath: process.env.NODE_ENV === 'production' ? '/' : '/',
```

## Verificações Necessárias na Railway

### 1. Variáveis de Ambiente do Frontend
Certifique-se de que estão configuradas:
```
VUE_APP_API_URL=https://api.montbiel.com.br
VUE_APP_FIREBASE_API_KEY=...
VUE_APP_FIREBASE_AUTH_DOMAIN=...
VUE_APP_FIREBASE_PROJECT_ID=...
VUE_APP_FIREBASE_STORAGE_BUCKET=...
VUE_APP_FIREBASE_MESSAGING_SENDER_ID=...
VUE_APP_FIREBASE_APP_ID=...
NODE_ENV=production
```

### 2. Root Directory
Deve estar configurado como: `/frontend`

### 3. Start Command
Deve estar como: `npm install && npm run start`
Ou usar o Procfile.frontend

## Como Verificar o Problema

1. **Abra o Console do Navegador (F12)**
   - Verifique se há erros JavaScript
   - Verifique se os arquivos estão sendo carregados

2. **Verifique os Logs da Railway**
   - Veja se o build foi bem-sucedido
   - Veja se o servidor está rodando

3. **Verifique a Network (F12 > Network)**
   - Veja se os arquivos JS/CSS estão sendo carregados
   - Veja se há erros 404

## Solução Alternativa (se ainda não funcionar)

Se o problema persistir, pode ser necessário usar um servidor diferente. Opções:

### Opção 1: Usar `http-server` ao invés de `serve`
```json
"start": "npm run build && npx http-server dist -p $PORT -P /"
```

### Opção 2: Criar um servidor Node.js simples
Criar `frontend/server.js`:
```js
const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, 'dist')));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
```

E no package.json:
```json
"start": "npm run build && node server.js"
```

## Próximos Passos

1. Faça commit das correções
2. Faça push para o repositório
3. A Railway deve fazer rebuild automaticamente
4. Verifique se o problema foi resolvido

