from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PaymentItem(BaseModel):
    id: Optional[str] = None
    nome: str
    valor: float
    parcelas: int
    percentual_pessoa1: float  # Percentual que a pessoa 1 paga
    percentual_pessoa2: float  # Percentual que a pessoa 2 paga
    data_criacao: Optional[str] = None
    ativo: bool = True
    conta_fixa: bool = False  # Se é uma conta fixa
    valor_manual_pessoa1: Optional[float] = None  # Valor manual para pessoa 1 (conta fixa)
    valor_manual_pessoa2: Optional[float] = None  # Valor manual para pessoa 2 (conta fixa)
    pago_pessoa1: bool = False  # Se a pessoa 1 já pagou
    pago_pessoa2: bool = False  # Se a pessoa 2 já pagou

class PaymentSummary(BaseModel):
    pessoa1: str = "Gabriel"
    pessoa2: str = "Juliana"
    total_pessoa1: float
    total_pessoa2: float
    valor_restante_pessoa1: float
    valor_restante_pessoa2: float
    valor_atual_pessoa1: float  # Valor atual do mês (não pago)
    valor_atual_pessoa2: float  # Valor atual do mês (não pago)
    mes_atual: str  # Mês atual no formato MM/YYYY
    itens: List[PaymentItem]

class PaymentItemCreate(BaseModel):
    nome: str
    valor: float
    parcelas: int
    percentual_pessoa1: float
    percentual_pessoa2: float
    conta_fixa: bool = False
    valor_manual_pessoa1: Optional[float] = None
    valor_manual_pessoa2: Optional[float] = None

class PaymentItemUpdate(BaseModel):
    nome: Optional[str] = None
    valor: Optional[float] = None
    parcelas: Optional[int] = None
    percentual_pessoa1: Optional[float] = None
    percentual_pessoa2: Optional[float] = None
    ativo: Optional[bool] = None
    conta_fixa: Optional[bool] = None
    valor_manual_pessoa1: Optional[float] = None
    valor_manual_pessoa2: Optional[float] = None
    pago_pessoa1: Optional[bool] = None
    pago_pessoa2: Optional[bool] = None
