from typing import List, Dict, Any
from datetime import datetime
from models import PaymentItem, PaymentSummary

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
    
    for item in active_items:
        valor_total = item['valor']
        parcelas = item['parcelas']
        percentual_pessoa1 = item['percentual_pessoa1']
        percentual_pessoa2 = item['percentual_pessoa2']
        conta_fixa = item.get('conta_fixa', False)
        valor_manual_pessoa1 = item.get('valor_manual_pessoa1')
        valor_manual_pessoa2 = item.get('valor_manual_pessoa2')
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
    
    # Converte os itens para o modelo PaymentItem
    payment_items = []
    for item in active_items:
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
            pago_pessoa2=item.get('pago_pessoa2', False)
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
