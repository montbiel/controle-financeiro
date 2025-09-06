#!/usr/bin/env python3
"""
Script para iniciar o backend do Sistema de Controle de Pagamentos
"""

import sys
import os
import subprocess

def main():
    print("🚀 Iniciando Sistema de Controle de Pagamentos - Backend")
    print("=" * 60)
    
    # Verifica se o arquivo .env existe
    if not os.path.exists('.env'):
        print("❌ Arquivo .env não encontrado!")
        print("📝 Copie o arquivo env.example para .env e configure suas credenciais:")
        print("   cp env.example .env")
        print("   # Edite o arquivo .env com suas configurações")
        return 1
    
    # Verifica se o arquivo de credenciais do Google existe
    credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
    if not os.path.exists(credentials_file):
        print(f"❌ Arquivo de credenciais não encontrado: {credentials_file}")
        print("📝 Configure suas credenciais do Google Sheets API:")
        print("   1. Acesse: https://console.cloud.google.com/")
        print("   2. Crie um projeto ou selecione um existente")
        print("   3. Ative a API do Google Sheets")
        print("   4. Crie credenciais (OAuth 2.0)")
        print("   5. Baixe o arquivo JSON e renomeie para 'credentials.json'")
        return 1
    
    try:
        # Instala dependências se necessário
        print("📦 Verificando dependências...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        
        # Inicia o servidor
        print("🌐 Iniciando servidor FastAPI...")
        print("📍 URL: http://localhost:8000")
        print("📚 Documentação: http://localhost:8000/docs")
        print("🔄 Pressione Ctrl+C para parar o servidor")
        print("=" * 60)
        
        # Executa o backend
        os.chdir('backend')
        subprocess.run([sys.executable, 'main.py'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n👋 Servidor parado pelo usuário")
        return 0
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
