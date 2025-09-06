from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging
from datetime import datetime

from models import PaymentItem, PaymentSummary, PaymentItemCreate, PaymentItemUpdate
from google_sheets import GoogleSheetsManager
from utils import calculate_monthly_payments, validate_percentages

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title="Sistema de Controle de Pagamentos",
    description="API para controle de pagamentos mensais com integração ao Google Sheets",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instância global do gerenciador do Google Sheets
sheets_manager = None

def get_sheets_manager():
    """Dependency para obter o gerenciador do Google Sheets"""
    global sheets_manager
    if sheets_manager is None:
        try:
            sheets_manager = GoogleSheetsManager()
        except Exception as e:
            logger.error(f"Erro ao inicializar Google Sheets Manager: {e}")
            raise HTTPException(status_code=500, detail="Erro ao conectar com Google Sheets")
    return sheets_manager

@app.on_event("startup")
async def startup_event():
    """Evento de inicialização da aplicação"""
    logger.info("Iniciando Sistema de Controle de Pagamentos...")
    try:
        # Testa a conexão com Google Sheets
        manager = get_sheets_manager()
        manager.get_all_items()
        logger.info("Conexão com Google Sheets estabelecida com sucesso")
    except Exception as e:
        logger.error(f"Erro na inicialização: {e}")

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Sistema de Controle de Pagamentos",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    try:
        manager = get_sheets_manager()
        manager.get_all_items()
        return {"status": "healthy", "google_sheets": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/payments/summary", response_model=PaymentSummary)
async def get_payment_summary(manager: GoogleSheetsManager = Depends(get_sheets_manager)):
    """
    Retorna o resumo dos pagamentos mensais
    """
    try:
        items = manager.get_all_items()
        summary = calculate_monthly_payments(items)
        return summary
    except Exception as e:
        logger.error(f"Erro ao buscar resumo de pagamentos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar dados de pagamentos")

@app.get("/payments/items", response_model=List[PaymentItem])
async def get_payment_items(manager: GoogleSheetsManager = Depends(get_sheets_manager)):
    """
    Retorna todos os itens de pagamento
    """
    try:
        items = manager.get_all_items()
        payment_items = []
        
        for item in items:
            payment_item = PaymentItem(
                id=item['id'],
                nome=item['nome'],
                valor=item['valor'],
                parcelas=item['parcelas'],
                percentual_pessoa1=item['percentual_pessoa1'],
                percentual_pessoa2=item['percentual_pessoa2'],
                data_criacao=item.get('data_criacao', ''),
                ativo=item.get('ativo', True)
            )
            payment_items.append(payment_item)
        
        return payment_items
    except Exception as e:
        logger.error(f"Erro ao buscar itens de pagamento: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar itens de pagamento")

@app.post("/payments/items", response_model=PaymentItem)
async def create_payment_item(
    item: PaymentItemCreate,
    manager: GoogleSheetsManager = Depends(get_sheets_manager)
):
    """
    Cria um novo item de pagamento
    """
    try:
        # Valida os percentuais
        if not validate_percentages(item.percentual_pessoa1, item.percentual_pessoa2):
            raise HTTPException(
                status_code=400, 
                detail="A soma dos percentuais deve ser igual a 100%"
            )
        
        # Valida os dados
        if item.valor <= 0:
            raise HTTPException(status_code=400, detail="O valor deve ser maior que zero")
        
        if item.parcelas <= 0:
            raise HTTPException(status_code=400, detail="O número de parcelas deve ser maior que zero")
        
        # Prepara os dados para inserção
        item_data = {
            'nome': item.nome,
            'valor': item.valor,
            'parcelas': item.parcelas,
            'percentual_pessoa1': item.percentual_pessoa1,
            'percentual_pessoa2': item.percentual_pessoa2,
            'data_criacao': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'ativo': True
        }
        
        # Adiciona o item na planilha
        item_id = manager.add_item(item_data)
        
        # Retorna o item criado
        created_item = PaymentItem(
            id=item_id,
            nome=item.nome,
            valor=item.valor,
            parcelas=item.parcelas,
            percentual_pessoa1=item.percentual_pessoa1,
            percentual_pessoa2=item.percentual_pessoa2,
            data_criacao=item_data['data_criacao'],
            ativo=True
        )
        
        logger.info(f"Item de pagamento criado: {item.nome}")
        return created_item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao criar item de pagamento: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar item de pagamento")

@app.put("/payments/items/{item_id}", response_model=PaymentItem)
async def update_payment_item(
    item_id: str,
    item_update: PaymentItemUpdate,
    manager: GoogleSheetsManager = Depends(get_sheets_manager)
):
    """
    Atualiza um item de pagamento existente
    """
    try:
        # Busca o item atual
        items = manager.get_all_items()
        current_item = None
        
        for item in items:
            if item['id'] == item_id:
                current_item = item
                break
        
        if not current_item:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        
        # Prepara os dados atualizados
        update_data = {}
        
        if item_update.nome is not None:
            update_data['nome'] = item_update.nome
        if item_update.valor is not None:
            if item_update.valor <= 0:
                raise HTTPException(status_code=400, detail="O valor deve ser maior que zero")
            update_data['valor'] = item_update.valor
        if item_update.parcelas is not None:
            if item_update.parcelas <= 0:
                raise HTTPException(status_code=400, detail="O número de parcelas deve ser maior que zero")
            update_data['parcelas'] = item_update.parcelas
        if item_update.percentual_pessoa1 is not None:
            update_data['percentual_pessoa1'] = item_update.percentual_pessoa1
        if item_update.percentual_pessoa2 is not None:
            update_data['percentual_pessoa2'] = item_update.percentual_pessoa2
        if item_update.ativo is not None:
            update_data['ativo'] = item_update.ativo
        
        # Valida percentuais se ambos foram fornecidos
        if 'percentual_pessoa1' in update_data and 'percentual_pessoa2' in update_data:
            if not validate_percentages(update_data['percentual_pessoa1'], update_data['percentual_pessoa2']):
                raise HTTPException(
                    status_code=400, 
                    detail="A soma dos percentuais deve ser igual a 100%"
                )
        
        # Atualiza o item
        success = manager.update_item(item_id, update_data)
        
        if not success:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        
        # Busca o item atualizado
        updated_items = manager.get_all_items()
        updated_item = None
        
        for item in updated_items:
            if item['id'] == item_id:
                updated_item = item
                break
        
        if not updated_item:
            raise HTTPException(status_code=404, detail="Item não encontrado após atualização")
        
        # Retorna o item atualizado
        result_item = PaymentItem(
            id=updated_item['id'],
            nome=updated_item['nome'],
            valor=updated_item['valor'],
            parcelas=updated_item['parcelas'],
            percentual_pessoa1=updated_item['percentual_pessoa1'],
            percentual_pessoa2=updated_item['percentual_pessoa2'],
            data_criacao=updated_item.get('data_criacao', ''),
            ativo=updated_item.get('ativo', True)
        )
        
        logger.info(f"Item de pagamento atualizado: {item_id}")
        return result_item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar item de pagamento: {e}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar item de pagamento")

@app.delete("/payments/items/{item_id}")
async def delete_payment_item(
    item_id: str,
    manager: GoogleSheetsManager = Depends(get_sheets_manager)
):
    """
    Remove um item de pagamento (soft delete)
    """
    try:
        success = manager.delete_item(item_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        
        logger.info(f"Item de pagamento removido: {item_id}")
        return {"message": "Item removido com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao remover item de pagamento: {e}")
        raise HTTPException(status_code=500, detail="Erro ao remover item de pagamento")

if __name__ == "__main__":
    import uvicorn
    import os
    
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', 8000))
    
    uvicorn.run(app, host=host, port=port)
