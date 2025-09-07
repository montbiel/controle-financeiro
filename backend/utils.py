from typing import List, Dict, Any
from datetime import datetime, timedelta
from models import PaymentItem, PaymentSummary, PaymentInstallment

def calculate_monthly_payments(items: List[Dict[str, Any]]) -> PaymentSummary:
    """
    Calcula os pagamentos mensais para cada pessoa baseado nos itens ativos
    """
    total_mensal_pessoa1 = 0.0
    total_mensal_pessoa2 = 0.0
    total_restante_pessoa1 = 0.0
    total_restante_pessoa2 = 0.0
    valor_atual_pessoa1 = 0.0  # Valor atual do mês (não pago)
    valor_atual_pessoa2 = 0.0  # Valor atual do mês (não pago)
    
    # Filtra apenas itens ativos
    active_items = [item for item in items if item.get('ativo', True)]
    current_month = get_current_month_year()
    
    for item in active_items:
        valor_total = item['valor']
        parcelas = item['parcelas']
        percentual_pessoa1 = item['percentual_pessoa1']
        percentual_pessoa2 = item['percentual_pessoa2']
        conta_fixa = item.get('conta_fixa', False)
        valor_manual_pessoa1 = item.get('valor_manual_pessoa1')
        valor_manual_pessoa2 = item.get('valor_manual_pessoa2')
        
        # Verifica se tem parcelas mensais (nova lógica)
        parcelas_mensais = item.get('parcelas_mensais', [])
        
        if parcelas_mensais:
            # Nova lógica com parcelas mensais
            conta_fixa = item.get('conta_fixa', False)
            
            # Calcula valores do mês atual
            parcelas_mes_atual = [p for p in parcelas_mensais if p['mes'] == current_month]
            for parcela in parcelas_mes_atual:
                total_mensal_pessoa1 += parcela['valor_pessoa1']
                total_mensal_pessoa2 += parcela['valor_pessoa2']
                
                # Valor atual (não pago)
                if not parcela.get('pago_pessoa1', False):
                    valor_atual_pessoa1 += parcela['valor_pessoa1']
                if not parcela.get('pago_pessoa2', False):
                    valor_atual_pessoa2 += parcela['valor_pessoa2']
            
            if conta_fixa:
                # CONTA FIXA: Valor restante é sempre 0 (não há valor a quitar, é mensal)
                total_restante_pessoa1 += 0
                total_restante_pessoa2 += 0
            else:
                # CONTA PARCELADA: Calcula valor restante (total - valor já pago)
                valor_total_pessoa1 = valor_total * percentual_pessoa1 / 100
                valor_total_pessoa2 = valor_total * percentual_pessoa2 / 100
                
                valor_pago_pessoa1 = sum(p['valor_pessoa1'] for p in parcelas_mensais if p.get('pago_pessoa1', False))
                valor_pago_pessoa2 = sum(p['valor_pessoa2'] for p in parcelas_mensais if p.get('pago_pessoa2', False))
                
                total_restante_pessoa1 += valor_total_pessoa1 - valor_pago_pessoa1
                total_restante_pessoa2 += valor_total_pessoa2 - valor_pago_pessoa2
                
                # Verifica se todas as parcelas foram pagas
                total_parcelas_pagas = sum(1 for p in parcelas_mensais if p.get('pago_pessoa1', False) and p.get('pago_pessoa2', False))
                if total_parcelas_pagas == len(parcelas_mensais):
                    # Todas as parcelas foram pagas, marcar como inativo
                    item['ativo'] = False
                    # TODO: Implementar atualização na planilha do status ativo
            
        else:
            # Lógica antiga (compatibilidade)
            pago_pessoa1 = item.get('pago_pessoa1', False)
            pago_pessoa2 = item.get('pago_pessoa2', False)
            
            # Calcula o valor mensal por pessoa
            if conta_fixa and valor_manual_pessoa1 is not None and valor_manual_pessoa2 is not None:
                # Conta fixa com valores manuais
                valor_mensal_pessoa1 = valor_manual_pessoa1
                valor_mensal_pessoa2 = valor_manual_pessoa2
                valor_total_pessoa1 = valor_manual_pessoa1
                valor_total_pessoa2 = valor_manual_pessoa2
            else:
                # Conta normal com percentuais
                valor_mensal_pessoa1 = (valor_total * percentual_pessoa1 / 100) / parcelas
                valor_mensal_pessoa2 = (valor_total * percentual_pessoa2 / 100) / parcelas
                valor_total_pessoa1 = valor_total * percentual_pessoa1 / 100
                valor_total_pessoa2 = valor_total * percentual_pessoa2 / 100
            
            # Soma os valores mensais
            total_mensal_pessoa1 += valor_mensal_pessoa1
            total_mensal_pessoa2 += valor_mensal_pessoa2
            
            # Calcula o valor restante (total - valor mensal)
            valor_restante_pessoa1 = valor_total_pessoa1 - valor_mensal_pessoa1
            valor_restante_pessoa2 = valor_total_pessoa2 - valor_mensal_pessoa2
            
            total_restante_pessoa1 += valor_restante_pessoa1
            total_restante_pessoa2 += valor_restante_pessoa2
            
            # Calcula valor atual (não pago)
            if not pago_pessoa1:
                valor_atual_pessoa1 += valor_mensal_pessoa1
            if not pago_pessoa2:
                valor_atual_pessoa2 += valor_mensal_pessoa2
    
    # Filtra apenas itens realmente ativos (após verificação de pagamento completo)
    truly_active_items = [item for item in active_items if item.get('ativo', True)]
    
    # Converte os itens para o modelo PaymentItem
    payment_items = []
    for item in truly_active_items:
        # Converte parcelas mensais se existirem
        parcelas_mensais = None
        if item.get('parcelas_mensais'):
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
    
    return PaymentSummary(
        pessoa1="Gabriel",
        pessoa2="Juliana",
        total_pessoa1=round(total_mensal_pessoa1, 2),
        total_pessoa2=round(total_mensal_pessoa2, 2),
        valor_restante_pessoa1=round(total_restante_pessoa1, 2),
        valor_restante_pessoa2=round(total_restante_pessoa2, 2),
        valor_atual_pessoa1=round(valor_atual_pessoa1, 2),
        valor_atual_pessoa2=round(valor_atual_pessoa2, 2),
        mes_atual=get_current_month_year(),
        itens=payment_items
    )

def validate_percentages(percentual_pessoa1: float, percentual_pessoa2: float) -> bool:
    """
    Valida se os percentuais somam 100%
    """
    total = percentual_pessoa1 + percentual_pessoa2
    return abs(total - 100.0) < 0.01  # Permite pequena diferença devido a arredondamentos

def format_currency(value: float) -> str:
    """
    Formata um valor como moeda brasileira
    """
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def get_current_month_year() -> str:
    """
    Retorna o mês e ano atual no formato MM/YYYY
    """
    now = datetime.now()
    return now.strftime("%m/%Y")

def generate_monthly_installments(
    valor_total: float, 
    parcelas: int, 
    percentual_pessoa1: float, 
    percentual_pessoa2: float,
    comecar_mes_atual: bool = True,
    conta_fixa: bool = False,
    valor_manual_pessoa1: float = None,
    valor_manual_pessoa2: float = None
) -> List[PaymentInstallment]:
    """
    Gera as parcelas mensais para um item de pagamento
    """
    parcelas_mensais = []
    
    # Calcula o valor mensal por pessoa
    if conta_fixa:
        # CONTA FIXA: Valor fixo todos os meses (não parcelado)
        if valor_manual_pessoa1 is not None and valor_manual_pessoa2 is not None:
            # Valores manuais definidos
            valor_mensal_pessoa1 = valor_manual_pessoa1
            valor_mensal_pessoa2 = valor_manual_pessoa2
        else:
            # Usa percentuais do valor total
            valor_mensal_pessoa1 = valor_total * percentual_pessoa1 / 100
            valor_mensal_pessoa2 = valor_total * percentual_pessoa2 / 100
        
        # Para conta fixa, ignoramos o número de parcelas - é infinito até ser excluído
        # Vamos gerar 120 meses (10 anos) como limite prático
        parcelas = 120
    else:
        # CONTA PARCELADA: Valor dividido pelas parcelas
        valor_pessoa1 = valor_total * percentual_pessoa1 / 100
        valor_pessoa2 = valor_total * percentual_pessoa2 / 100
        valor_mensal_pessoa1 = valor_pessoa1 / parcelas
        valor_mensal_pessoa2 = valor_pessoa2 / parcelas
    
    # Define o mês inicial
    if comecar_mes_atual:
        # Começa no mês atual
        current_date = datetime.now()
    else:
        # Começa no próximo mês
        current_date = datetime.now() + timedelta(days=32)
        current_date = current_date.replace(day=1)
    
    # Gera as parcelas
    for i in range(parcelas):
        # Calcula o mês da parcela
        month_date = current_date + timedelta(days=32 * i)
        month_date = month_date.replace(day=1)
        mes_str = month_date.strftime("%m/%Y")
        
        parcela = PaymentInstallment(
            mes=mes_str,
            valor_pessoa1=round(valor_mensal_pessoa1, 2),
            valor_pessoa2=round(valor_mensal_pessoa2, 2),
            pago_pessoa1=False,
            pago_pessoa2=False
        )
        parcelas_mensais.append(parcela)
    
    return parcelas_mensais

def get_current_month_installments(parcelas_mensais: List[PaymentInstallment]) -> List[PaymentInstallment]:
    """
    Retorna as parcelas do mês atual
    """
    current_month = get_current_month_year()
    return [p for p in parcelas_mensais if p.mes == current_month]

def get_unpaid_installments(parcelas_mensais: List[PaymentInstallment]) -> List[PaymentInstallment]:
    """
    Retorna as parcelas não pagas
    """
    return [p for p in parcelas_mensais if not p.pago_pessoa1 or not p.pago_pessoa2]
