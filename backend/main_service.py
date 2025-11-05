from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging
from datetime import datetime

from models import PaymentItem, PaymentSummary, PaymentItemCreate, PaymentItemUpdate
from google_sheets_service import GoogleSheetsServiceManager
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
            sheets_manager = GoogleSheetsServiceManager()
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
async def get_payment_summary(manager: GoogleSheetsServiceManager = Depends(get_sheets_manager)):
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
async def get_payment_items(manager: GoogleSheetsServiceManager = Depends(get_sheets_manager)):
    """
    Retorna todos os itens de pagamento
    """
    try:
        items = manager.get_all_items()
        payment_items = []
        
        for item in items:
            # Converte parcelas mensais se existirem
            parcelas_mensais = None
            if item.get('parcelas_mensais'):
                from models import PaymentInstallment
                parcelas_mensais = [
                    PaymentInstallment(
                        mes=p['mes'],
                        valor_pessoa1=p['valor_pessoa1'],
                        valor_pessoa2=p['valor_pessoa2'],
                        pago_pessoa1=p.get('pago_pessoa1', False),
                        pago_pessoa2=p.get('pago_pessoa2', False)
                    ) for p in item['parcelas_mensais']
                ]
            
            payment_item = PaymentItem(
                id=item['id'],
                nome=item['nome'],
                valor=item['valor'],
                parcelas=item['parcelas'],
                percentual_pessoa1=item['percentual_pessoa1'],
                percentual_pessoa2=item['percentual_pessoa2'],
                data_criacao=item.get('data_criacao', ''),
                ativo=item.get('ativo', True),
                conta_fixa=item.get('conta_fixa', False),
                valor_manual_pessoa1=item.get('valor_manual_pessoa1'),
                valor_manual_pessoa2=item.get('valor_manual_pessoa2'),
                pago_pessoa1=item.get('pago_pessoa1', False),
                pago_pessoa2=item.get('pago_pessoa2', False),
                parcelas_mensais=parcelas_mensais,
                comecar_mes_atual=item.get('comecar_mes_atual', True)
            )
            payment_items.append(payment_item)
        
        return payment_items
    except Exception as e:
        logger.error(f"Erro ao buscar itens de pagamento: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar itens de pagamento")

@app.post("/payments/items", response_model=PaymentItem)
async def create_payment_item(
    item: PaymentItemCreate,
    manager: GoogleSheetsServiceManager = Depends(get_sheets_manager)
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
        
        # Gera as parcelas mensais
        from utils import generate_monthly_installments
        parcelas_mensais = generate_monthly_installments(
            valor_total=item.valor,
            parcelas=item.parcelas,
            percentual_pessoa1=item.percentual_pessoa1,
            percentual_pessoa2=item.percentual_pessoa2,
            comecar_mes_atual=item.comecar_mes_atual,
            conta_fixa=item.conta_fixa,
            valor_manual_pessoa1=item.valor_manual_pessoa1,
            valor_manual_pessoa2=item.valor_manual_pessoa2
        )
        
        # Converte para formato de dicionário para armazenamento
        parcelas_mensais_dict = [
            {
                'mes': p.mes,
                'valor_pessoa1': p.valor_pessoa1,
                'valor_pessoa2': p.valor_pessoa2,
                'pago_pessoa1': p.pago_pessoa1,
                'pago_pessoa2': p.pago_pessoa2
            } for p in parcelas_mensais
        ]
        
        # Prepara os dados para inserção
        item_data = {
            'nome': item.nome,
            'valor': item.valor,
            'parcelas': item.parcelas,
            'percentual_pessoa1': item.percentual_pessoa1,
            'percentual_pessoa2': item.percentual_pessoa2,
            'data_criacao': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'ativo': True,
            'conta_fixa': item.conta_fixa,
            'valor_manual_pessoa1': item.valor_manual_pessoa1,
            'valor_manual_pessoa2': item.valor_manual_pessoa2,
            'pago_pessoa1': False,
            'pago_pessoa2': False,
            'parcelas_mensais': parcelas_mensais_dict,
            'comecar_mes_atual': item.comecar_mes_atual
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
            ativo=True,
            conta_fixa=item.conta_fixa,
            valor_manual_pessoa1=item.valor_manual_pessoa1,
            valor_manual_pessoa2=item.valor_manual_pessoa2,
            pago_pessoa1=False,
            pago_pessoa2=False,
            parcelas_mensais=parcelas_mensais,
            comecar_mes_atual=item.comecar_mes_atual
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
    manager: GoogleSheetsServiceManager = Depends(get_sheets_manager)
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
        if item_update.conta_fixa is not None:
            update_data['conta_fixa'] = item_update.conta_fixa
        if item_update.valor_manual_pessoa1 is not None:
            update_data['valor_manual_pessoa1'] = item_update.valor_manual_pessoa1
        if item_update.valor_manual_pessoa2 is not None:
            update_data['valor_manual_pessoa2'] = item_update.valor_manual_pessoa2
        if item_update.pago_pessoa1 is not None:
            update_data['pago_pessoa1'] = item_update.pago_pessoa1
        if item_update.pago_pessoa2 is not None:
            update_data['pago_pessoa2'] = item_update.pago_pessoa2
        if item_update.parcelas_mensais is not None:
            # Converte parcelas mensais para formato de dicionário
            parcelas_mensais_dict = [
                {
                    'mes': p.mes,
                    'valor_pessoa1': p.valor_pessoa1,
                    'valor_pessoa2': p.valor_pessoa2,
                    'pago_pessoa1': p.pago_pessoa1,
                    'pago_pessoa2': p.pago_pessoa2
                } for p in item_update.parcelas_mensais
            ]
            update_data['parcelas_mensais'] = parcelas_mensais_dict
        
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
        
        # Converte parcelas mensais se existirem
        parcelas_mensais = None
        if updated_item.get('parcelas_mensais'):
            from models import PaymentInstallment
            parcelas_mensais = [
                PaymentInstallment(
                    mes=p['mes'],
                    valor_pessoa1=p['valor_pessoa1'],
                    valor_pessoa2=p['valor_pessoa2'],
                    pago_pessoa1=p.get('pago_pessoa1', False),
                    pago_pessoa2=p.get('pago_pessoa2', False)
                ) for p in updated_item['parcelas_mensais']
            ]
        
        # Retorna o item atualizado
        result_item = PaymentItem(
            id=updated_item['id'],
            nome=updated_item['nome'],
            valor=updated_item['valor'],
            parcelas=updated_item['parcelas'],
            percentual_pessoa1=updated_item['percentual_pessoa1'],
            percentual_pessoa2=updated_item['percentual_pessoa2'],
            data_criacao=updated_item.get('data_criacao', ''),
            ativo=updated_item.get('ativo', True),
            conta_fixa=updated_item.get('conta_fixa', False),
            valor_manual_pessoa1=updated_item.get('valor_manual_pessoa1'),
            valor_manual_pessoa2=updated_item.get('valor_manual_pessoa2'),
            pago_pessoa1=updated_item.get('pago_pessoa1', False),
            pago_pessoa2=updated_item.get('pago_pessoa2', False),
            parcelas_mensais=parcelas_mensais,
            comecar_mes_atual=updated_item.get('comecar_mes_atual', True)
        )
        
        logger.info(f"Item de pagamento atualizado: {item_id}")
        return result_item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar item de pagamento: {e}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar item de pagamento")

from pydantic import BaseModel

class PaymentRequest(BaseModel):
    mes: str
    pessoa: str

@app.post("/payments/items/{item_id}/pay")
async def mark_payment(
    item_id: str,
    payment_request: PaymentRequest,
    manager: GoogleSheetsServiceManager = Depends(get_sheets_manager)
):
    """
    Marca uma parcela específica como paga
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
        
        # Verifica se tem parcelas mensais
        parcelas_mensais = current_item.get('parcelas_mensais', [])
        if not parcelas_mensais:
            raise HTTPException(status_code=400, detail="Item não possui parcelas mensais")
        
        # Encontra a parcela do mês especificado
        mes = payment_request.mes
        pessoa = payment_request.pessoa
        
        parcela_encontrada = False
        for parcela in parcelas_mensais:
            if parcela['mes'] == mes:
                if pessoa == "pessoa1":
                    parcela['pago_pessoa1'] = True
                elif pessoa == "pessoa2":
                    parcela['pago_pessoa2'] = True
                else:
                    raise HTTPException(status_code=400, detail="Pessoa deve ser 'pessoa1' ou 'pessoa2'")
                parcela_encontrada = True
                break
        
        if not parcela_encontrada:
            raise HTTPException(status_code=404, detail=f"Parcela do mês {mes} não encontrada")
        
        # Verifica se todas as parcelas foram pagas
        if not current_item.get('conta_fixa', False):  # Só para contas parceladas
            total_parcelas_pagas = sum(1 for p in parcelas_mensais if p.get('pago_pessoa1', False) and p.get('pago_pessoa2', False))
            if total_parcelas_pagas == len(parcelas_mensais):
                # Todas as parcelas foram pagas, marcar como inativo
                update_data = {'parcelas_mensais': parcelas_mensais, 'ativo': False}
                logger.info(f"Item {item_id} marcado como inativo - todas as parcelas foram pagas")
            else:
                update_data = {'parcelas_mensais': parcelas_mensais}
        else:
            update_data = {'parcelas_mensais': parcelas_mensais}
        
        success = manager.update_item(item_id, update_data)
        
        if not success:
            raise HTTPException(status_code=500, detail="Erro ao atualizar parcela")
        
        logger.info(f"Parcela {mes} marcada como paga para {pessoa} no item {item_id}")
        return {"message": f"Parcela {mes} marcada como paga para {pessoa}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao marcar parcela como paga: {e}")
        raise HTTPException(status_code=500, detail="Erro ao marcar parcela como paga")

@app.put("/payments/items/{item_id}/installments/pay")
async def mark_installment_paid(
    item_id: str,
    mes: str = Query(..., description="Mês da parcela no formato MM/YYYY (ex: 11/2025)"),
    pessoa: str = Query(..., description="Pessoa que está pagando (pessoa1 ou pessoa2)"),
    manager: GoogleSheetsServiceManager = Depends(get_sheets_manager)
):
    """
    Marca uma parcela específica como paga (rota compatível com frontend)
    """
    try:
        # Log para debug - verificar o mês recebido
        logger.info(f"Marcando parcela como paga - Item: {item_id}, Mês: {mes}, Pessoa: {pessoa}")
        
        # Busca o item atual
        items = manager.get_all_items()
        current_item = None
        
        for item in items:
            if item['id'] == item_id:
                current_item = item
                break
        
        if not current_item:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        
        # Verifica se tem parcelas mensais
        parcelas_mensais = current_item.get('parcelas_mensais', [])
        if not parcelas_mensais:
            raise HTTPException(status_code=400, detail="Item não possui parcelas mensais")
        
        # Log para debug - verificar parcelas disponíveis
        logger.info(f"Parcelas disponíveis: {[p.get('mes') for p in parcelas_mensais]}")
        
        # Encontra a parcela do mês especificado
        parcela_encontrada = False
        for parcela in parcelas_mensais:
            if parcela['mes'] == mes:
                if pessoa == "pessoa1":
                    parcela['pago_pessoa1'] = True
                elif pessoa == "pessoa2":
                    parcela['pago_pessoa2'] = True
                else:
                    raise HTTPException(status_code=400, detail="Pessoa deve ser 'pessoa1' ou 'pessoa2'")
                parcela_encontrada = True
                break
        
        if not parcela_encontrada:
            raise HTTPException(status_code=404, detail=f"Parcela do mês {mes} não encontrada")
        
        # Verifica se todas as parcelas foram pagas
        if not current_item.get('conta_fixa', False):  # Só para contas parceladas
            total_parcelas_pagas = sum(1 for p in parcelas_mensais if p.get('pago_pessoa1', False) and p.get('pago_pessoa2', False))
            if total_parcelas_pagas == len(parcelas_mensais):
                # Todas as parcelas foram pagas, marcar como inativo
                update_data = {'parcelas_mensais': parcelas_mensais, 'ativo': False}
                logger.info(f"Item {item_id} marcado como inativo - todas as parcelas foram pagas")
            else:
                update_data = {'parcelas_mensais': parcelas_mensais}
        else:
            update_data = {'parcelas_mensais': parcelas_mensais}
        
        success = manager.update_item(item_id, update_data)
        
        if not success:
            raise HTTPException(status_code=500, detail="Erro ao atualizar parcela")
        
        logger.info(f"Parcela {mes} marcada como paga para {pessoa} no item {item_id}")
        return {"message": f"Parcela {mes} marcada como paga para {pessoa}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao marcar parcela como paga: {e}")
        raise HTTPException(status_code=500, detail="Erro ao marcar parcela como paga")

@app.delete("/payments/items/{item_id}")
async def delete_payment_item(
    item_id: str,
    manager: GoogleSheetsServiceManager = Depends(get_sheets_manager)
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
