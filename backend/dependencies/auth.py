"""
Dependencies do FastAPI para autenticação Firebase
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

try:
    from firebase.admin import verify_id_token
except ImportError:
    # Firebase Admin não instalado ainda
    verify_id_token = None

logger = logging.getLogger(__name__)

# Esquema de segurança HTTP Bearer
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency para obter o usuário autenticado
    
    Args:
        credentials: Credenciais HTTP Bearer (token)
        
    Returns:
        dict: Dados do usuário decodificados do token
        
    Raises:
        HTTPException: Se o token for inválido ou não fornecido
    """
    token = credentials.credentials
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação não fornecido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if verify_id_token is None:
        logger.error("Firebase Admin SDK não está instalado ou configurado")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Serviço de autenticação não configurado",
        )
    
    try:
        # Verifica e decodifica o token
        decoded_token = verify_id_token(token)
        
        # Retorna dados do usuário
        return {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "email_verified": decoded_token.get("email_verified", False),
            "name": decoded_token.get("name"),
            "picture": decoded_token.get("picture")
        }
    except ValueError as e:
        logger.error(f"Token inválido: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Erro ao verificar token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro ao verificar autenticação",
            headers={"WWW-Authenticate": "Bearer"},
        )

