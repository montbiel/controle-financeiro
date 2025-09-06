import os
import json
from typing import List, Dict, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

class GoogleSheetsServiceManager:
    def __init__(self):
        self.service = None
        self.spreadsheet_id = None
        self.sheet_name = os.getenv('SHEET_NAME', 'Sheet1')
        self._authenticate()
        self._get_spreadsheet_id()
    
    def _authenticate(self):
        """Autentica usando Service Account"""
        service_account_file = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'service-account.json')
        
        # Verifica se o arquivo de service account existe
        if not os.path.exists(service_account_file):
            logger.error(f"Arquivo de service account não encontrado: {service_account_file}")
            raise FileNotFoundError(f"Arquivo de service account não encontrado: {service_account_file}")
        
        try:
            # Carrega as credenciais da service account
            credentials = service_account.Credentials.from_service_account_file(
                service_account_file,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            
            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("Autenticação com Google Sheets realizada com sucesso usando Service Account")
            
        except Exception as e:
            logger.error(f"Erro na autenticação: {e}")
            raise
    
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
            if not values or len(values[0]) < 12:
                headers = [
                    'ID', 'Nome', 'Valor', 'Parcelas', 
                    'Percentual Pessoa 1', 'Percentual Pessoa 2', 
                    'Data Criação', 'Ativo', 'Conta Fixa',
                    'Valor Manual Pessoa 1', 'Valor Manual Pessoa 2',
                    'Pago Pessoa 1', 'Pago Pessoa 2'
                ]
                
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=f'{self.sheet_name}!A1:M1',
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
                        'ativo': row[7].lower() == 'true' if len(row) > 7 else True,
                        'conta_fixa': row[8].lower() == 'true' if len(row) > 8 else False,
                        'valor_manual_pessoa1': float(row[9]) if len(row) > 9 and row[9] and row[9] != 'None' else None,
                        'valor_manual_pessoa2': float(row[10]) if len(row) > 10 and row[10] and row[10] != 'None' else None,
                        'pago_pessoa1': row[11].lower() == 'true' if len(row) > 11 else False,
                        'pago_pessoa2': row[12].lower() == 'true' if len(row) > 12 else False
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
                str(item_data.get('ativo', True)),
                str(item_data.get('conta_fixa', False)),
                str(item_data.get('valor_manual_pessoa1', '')),
                str(item_data.get('valor_manual_pessoa2', '')),
                str(item_data.get('pago_pessoa1', False)),
                str(item_data.get('pago_pessoa2', False))
            ]
            
            # Adiciona a linha na planilha
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f'{self.sheet_name}!A:M',
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
            logger.info(f"Atualizando item {item_id} com dados: {item_data}")
            # Busca todos os itens para encontrar a linha do item
            items = self.get_all_items()
            
            for i, item in enumerate(items):
                if item['id'] == item_id:
                    logger.info(f"Item encontrado na linha {i + 2}")
                    # Prepara os dados atualizados
                    row_data = [
                        item_id,
                        item_data.get('nome', item['nome']),
                        str(item_data.get('valor', item['valor'])),
                        str(item_data.get('parcelas', item['parcelas'])),
                        str(item_data.get('percentual_pessoa1', item['percentual_pessoa1'])),
                        str(item_data.get('percentual_pessoa2', item['percentual_pessoa2'])),
                        item_data.get('data_criacao', item['data_criacao']),
                        str(item_data.get('ativo', item['ativo'])),
                        str(item_data.get('conta_fixa', item.get('conta_fixa', False))),
                        str(item_data.get('valor_manual_pessoa1', item.get('valor_manual_pessoa1', '')) if item_data.get('valor_manual_pessoa1', item.get('valor_manual_pessoa1', '')) is not None else ''),
                        str(item_data.get('valor_manual_pessoa2', item.get('valor_manual_pessoa2', '')) if item_data.get('valor_manual_pessoa2', item.get('valor_manual_pessoa2', '')) is not None else ''),
                        str(item_data.get('pago_pessoa1', item.get('pago_pessoa1', False))),
                        str(item_data.get('pago_pessoa2', item.get('pago_pessoa2', False)))
                    ]
                    
                    # Atualiza a linha (linha 2 + índice, pois linha 1 são os cabeçalhos)
                    row_number = i + 2
                    
                    self.service.spreadsheets().values().update(
                        spreadsheetId=self.spreadsheet_id,
                        range=f'{self.sheet_name}!A{row_number}:M{row_number}',
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
        """Remove completamente um item da planilha"""
        try:
            # Busca todos os itens para encontrar a linha do item
            items = self.get_all_items()
            
            for i, item in enumerate(items):
                if item['id'] == item_id:
                    # Calcula o número da linha (linha 2 + índice, pois linha 1 são os cabeçalhos)
                    row_number = i + 2
                    
                    # Remove a linha da planilha
                    request_body = {
                        'requests': [{
                            'deleteDimension': {
                                'range': {
                                    'sheetId': 0,  # ID da primeira aba
                                    'dimension': 'ROWS',
                                    'startIndex': row_number - 1,  # Índice baseado em 0
                                    'endIndex': row_number
                                }
                            }
                        }]
                    }
                    
                    self.service.spreadsheets().batchUpdate(
                        spreadsheetId=self.spreadsheet_id,
                        body=request_body
                    ).execute()
                    
                    logger.info(f"Item {item_id} removido completamente da planilha")
                    return True
            
            logger.warning(f"Item {item_id} não encontrado")
            return False
        
        except HttpError as error:
            logger.error(f"Erro ao deletar item: {error}")
            raise
