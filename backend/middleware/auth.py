"""
Middleware de autenticação para FastAPI
"""
from fastapi import Request, HTTPException, status
from firebase.admin import verify_id_token
import logging

logger = logging.getLogger(__name__)

async def verify_token_middleware(request: Request, call_next):
    """
    Middleware para verificar token Firebase em todas as requisições
    
    Nota: Este middleware é opcional. A validação pode ser feita
    via dependencies do FastAPI (recomendado).
    """
    # Lista de rotas públicas que não precisam de autenticação
    public_routes = [
        "/",
        "/health",
        "/docs",
        "/openapi.json",
        "/redoc"
    ]
    
    # Verifica se a rota é pública
    if request.url.path in public_routes or request.url.path.startswith("/docs"):
        return await call_next(request)
    
    # Verifica se há token no header
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação não fornecido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = auth_header.split("Bearer ")[1]
    
    try:
        # Verifica o token
        decoded_token = verify_id_token(token)
        # Adiciona dados do usuário ao request state
        request.state.user = decoded_token
    except Exception as e:
        logger.error(f"Erro ao verificar token no middleware: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return await call_next(request)

