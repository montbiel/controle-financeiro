import os
import json
from typing import List, Dict, Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Escopo necessário para acessar Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class GoogleSheetsManager:
    def __init__(self):
        self.service = None
        self.spreadsheet_id = None
        self.sheet_name = os.getenv('SHEET_NAME', 'Pagamentos')
        self._authenticate()
        self._get_spreadsheet_id()
    
    def _authenticate(self):
        """Autentica com a API do Google Sheets"""
        creds = None
        credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
        
        # Verifica se o arquivo de credenciais existe
        if not os.path.exists(credentials_file):
            logger.error(f"Arquivo de credenciais não encontrado: {credentials_file}")
            raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {credentials_file}")
        
        # Verifica se já temos credenciais salvas
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # Se não há credenciais válidas, faz o fluxo de autenticação
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Salva as credenciais para próximas execuções
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('sheets', 'v4', credentials=creds)
        logger.info("Autenticação com Google Sheets realizada com sucesso")
    
    def _get_spreadsheet_id(self):
        """Extrai o ID da planilha da URL"""
        sheets_url = os.getenv('GOOGLE_SHEETS_URL')
        if not sheets_url:
            raise ValueError("GOOGLE_SHEETS_URL não configurada no arquivo .env")
        
        # Extrai o ID da planilha da URL
        if '/d/' in sheets_url:
            self.spreadsheet_id = sheets_url.split('/d/')[1].split('/')[0]
        else:
            raise ValueError("URL da planilha inválida")
        
        logger.info(f"ID da planilha: {self.spreadsheet_id}")
    
    def _ensure_headers(self):
        """Garante que os cabeçalhos existam na planilha"""
        try:
            # Verifica se a planilha tem dados
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f'{self.sheet_name}!A1:Z1'
            ).execute()
            
            values = result.get('values', [])
            
            # Se não há dados ou não tem cabeçalhos, cria os cabeçalhos
            if not values or len(values[0]) < 7:
                headers = [
                    'ID', 'Nome', 'Valor', 'Parcelas', 
                    'Percentual Pessoa 1', 'Percentual Pessoa 2', 
                    'Data Criação', 'Ativo'
                ]
                
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=f'{self.sheet_name}!A1:H1',
                    valueInputOption='RAW',
                    body={'values': [headers]}
                ).execute()
                
                logger.info("Cabeçalhos criados na planilha")
        
        except HttpError as error:
            logger.error(f"Erro ao verificar/criar cabeçalhos: {error}")
            raise
    
    def get_all_items(self) -> List[Dict[str, Any]]:
        """Busca todos os itens da planilha"""
        try:
            self._ensure_headers()
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f'{self.sheet_name}!A2:Z'
            ).execute()
            
            values = result.get('values', [])
            items = []
            
            for row in values:
                if len(row) >= 7:  # Garante que a linha tem todos os campos necessários
                    item = {
                        'id': row[0] if len(row) > 0 else '',
                        'nome': row[1] if len(row) > 1 else '',
                        'valor': float(row[2]) if len(row) > 2 and row[2] else 0.0,
                        'parcelas': int(row[3]) if len(row) > 3 and row[3] else 1,
                        'percentual_pessoa1': float(row[4]) if len(row) > 4 and row[4] else 0.0,
                        'percentual_pessoa2': float(row[5]) if len(row) > 5 and row[5] else 0.0,
                        'data_criacao': row[6] if len(row) > 6 else '',
                        'ativo': row[7].lower() == 'true' if len(row) > 7 else True
                    }
                    items.append(item)
            
            logger.info(f"Carregados {len(items)} itens da planilha")
            return items
        
        except HttpError as error:
            logger.error(f"Erro ao buscar itens: {error}")
            raise
    
    def add_item(self, item_data: Dict[str, Any]) -> str:
        """Adiciona um novo item à planilha"""
        try:
            self._ensure_headers()
            
            # Gera um ID único baseado no timestamp
            import time
            item_id = str(int(time.time() * 1000))
            
            # Prepara os dados para inserção
            row_data = [
                item_id,
                item_data['nome'],
                str(item_data['valor']),
                str(item_data['parcelas']),
                str(item_data['percentual_pessoa1']),
                str(item_data['percentual_pessoa2']),
                item_data.get('data_criacao', ''),
                str(item_data.get('ativo', True))
            ]
            
            # Adiciona a linha na planilha
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f'{self.sheet_name}!A:H',
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body={'values': [row_data]}
            ).execute()
            
            logger.info(f"Item adicionado com ID: {item_id}")
            return item_id
        
        except HttpError as error:
            logger.error(f"Erro ao adicionar item: {error}")
            raise
    
    def update_item(self, item_id: str, item_data: Dict[str, Any]) -> bool:
        """Atualiza um item existente na planilha"""
        try:
            # Busca todos os itens para encontrar a linha do item
            items = self.get_all_items()
            
            for i, item in enumerate(items):
                if item['id'] == item_id:
                    # Prepara os dados atualizados
                    row_data = [
                        item_id,
                        item_data.get('nome', item['nome']),
                        str(item_data.get('valor', item['valor'])),
                        str(item_data.get('parcelas', item['parcelas'])),
                        str(item_data.get('percentual_pessoa1', item['percentual_pessoa1'])),
                        str(item_data.get('percentual_pessoa2', item['percentual_pessoa2'])),
                        item_data.get('data_criacao', item['data_criacao']),
                        str(item_data.get('ativo', item['ativo']))
                    ]
                    
                    # Atualiza a linha (linha 2 + índice, pois linha 1 são os cabeçalhos)
                    row_number = i + 2
                    
                    self.service.spreadsheets().values().update(
                        spreadsheetId=self.spreadsheet_id,
                        range=f'{self.sheet_name}!A{row_number}:H{row_number}',
                        valueInputOption='RAW',
                        body={'values': [row_data]}
                    ).execute()
                    
                    logger.info(f"Item {item_id} atualizado com sucesso")
                    return True
            
            logger.warning(f"Item {item_id} não encontrado")
            return False
        
        except HttpError as error:
            logger.error(f"Erro ao atualizar item: {error}")
            raise
    
    def delete_item(self, item_id: str) -> bool:
        """Marca um item como inativo (soft delete)"""
        try:
            return self.update_item(item_id, {'ativo': False})
        except Exception as error:
            logger.error(f"Erro ao deletar item: {error}")
            raise
