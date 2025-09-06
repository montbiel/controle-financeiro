#!/bin/bash

echo "🚀 Iniciando Sistema de Controle de Pagamentos - Frontend"
echo "============================================================"

# Verifica se o Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado!"
    echo "📝 Instale o Node.js: https://nodejs.org/"
    exit 1
fi

# Verifica se o npm está instalado
if ! command -v npm &> /dev/null; then
    echo "❌ npm não encontrado!"
    echo "📝 Instale o npm junto com o Node.js"
    exit 1
fi

# Navega para o diretório do frontend
cd frontend

# Verifica se o package.json existe
if [ ! -f "package.json" ]; then
    echo "❌ package.json não encontrado no diretório frontend!"
    exit 1
fi

# Instala dependências se necessário
echo "📦 Instalando dependências..."
npm install

# Verifica se a instalação foi bem-sucedida
if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências!"
    exit 1
fi

echo "🌐 Iniciando servidor de desenvolvimento..."
echo "📍 URL: http://localhost:8080"
echo "🔄 Pressione Ctrl+C para parar o servidor"
echo "============================================================"

# Inicia o servidor de desenvolvimento
npm run serve
