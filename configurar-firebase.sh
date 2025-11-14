#!/bin/bash

# Script para configurar variáveis do Firebase
# Uso: ./configurar-firebase.sh

echo "🔥 Configuração do Firebase"
echo "================================"
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se está no diretório correto
if [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    echo "❌ Erro: Execute este script na raiz do projeto"
    exit 1
fi

echo "📋 Informações do Projeto Firebase:"
echo "   Projeto: controle-finaceiro-d7784"
echo "   Service Account: firebase-adminsdk-fbsvc@controle-finaceiro-d7784.iam.gserviceaccount.com"
echo ""

# Frontend
echo "${YELLOW}🔧 Configuração do Frontend${NC}"
echo ""

if [ -f "frontend/.env" ]; then
    echo "⚠️  Arquivo frontend/.env já existe. Deseja sobrescrever? (s/N)"
    read -r resposta
    if [ "$resposta" != "s" ] && [ "$resposta" != "S" ]; then
        echo "Pulando configuração do frontend..."
    else
        rm frontend/.env
    fi
fi

if [ ! -f "frontend/.env" ]; then
    echo "Criando frontend/.env..."
    cat > frontend/.env << 'EOF'
# Firebase Configuration
# Obtenha essas informações no Firebase Console: Project Settings > Your apps > Web app

VUE_APP_FIREBASE_API_KEY=AIzaSyBgkE1IwEhTSDTDitmIV4hmswRebTiFayE
VUE_APP_FIREBASE_AUTH_DOMAIN=controle-finaceiro-d7784.firebaseapp.com
VUE_APP_FIREBASE_PROJECT_ID=controle-finaceiro-d7784
VUE_APP_FIREBASE_STORAGE_BUCKET=controle-finaceiro-d7784.appspot.com
VUE_APP_FIREBASE_MESSAGING_SENDER_ID=637919390276
VUE_APP_FIREBASE_APP_ID=1:637919390276:web:7a7b718850579323c7ea11
EOF
    echo "${GREEN}✅ Arquivo frontend/.env criado${NC}"
    echo ""
    echo "📝 Preencha as variáveis no arquivo frontend/.env:"
    echo "   - VUE_APP_FIREBASE_API_KEY"
    echo "   - VUE_APP_FIREBASE_MESSAGING_SENDER_ID"
    echo "   - VUE_APP_FIREBASE_APP_ID"
    echo ""
    echo "   Obtenha essas informações em:"
    echo "   https://console.firebase.google.com/project/controle-finaceiro-d7784/settings/general"
    echo ""
fi

# Backend
echo "${YELLOW}🔐 Configuração do Backend${NC}"
echo ""

if [ -f "backend/firebase-admin-credentials.json" ]; then
    echo "${GREEN}✅ Arquivo backend/firebase-admin-credentials.json já existe${NC}"
else
    echo "📥 Para configurar o backend:"
    echo ""
    echo "1. Acesse: https://console.firebase.google.com/project/controle-finaceiro-d7784/settings/serviceaccounts/adminsdk"
    echo "2. Clique em 'Generate new private key'"
    echo "3. Baixe o arquivo JSON"
    echo "4. Renomeie para 'firebase-admin-credentials.json'"
    echo "5. Mova para a pasta 'backend/'"
    echo ""
    echo "   OU configure no Railway usando FIREBASE_ADMIN_CREDENTIALS_BASE64"
    echo ""
fi

# Verificar dependências
echo "${YELLOW}📦 Verificando dependências${NC}"
echo ""

# Backend
if command -v pip &> /dev/null; then
    echo "Verificando firebase-admin..."
    if pip show firebase-admin &> /dev/null; then
        echo "${GREEN}✅ firebase-admin instalado${NC}"
    else
        echo "⚠️  firebase-admin não instalado. Execute: cd backend && pip install -r requirements.txt"
    fi
else
    echo "⚠️  pip não encontrado"
fi

# Frontend
if [ -d "frontend/node_modules" ]; then
    if [ -d "frontend/node_modules/firebase" ]; then
        echo "${GREEN}✅ Firebase SDK instalado${NC}"
    else
        echo "⚠️  Firebase SDK não instalado. Execute: cd frontend && npm install"
    fi
else
    echo "⚠️  node_modules não encontrado. Execute: cd frontend && npm install"
fi

echo ""
echo "${GREEN}✅ Configuração concluída!${NC}"
echo ""
echo "📚 Próximos passos:"
echo "1. Preencha as variáveis no frontend/.env"
echo "2. Configure as credenciais do backend (arquivo ou Railway)"
echo "3. Ative Authentication no Firebase Console"
echo "4. Crie um usuário de teste"
echo "5. Execute: cd backend && python main_service.py"
echo "6. Execute: cd frontend && npm run serve"
echo ""
echo "📖 Veja CONFIGURAR_FIREBASE.md para instruções detalhadas"

