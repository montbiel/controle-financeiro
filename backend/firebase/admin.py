"""
Configuração do Firebase Admin SDK para validação de tokens
"""
import os
import json
import base64
import logging
try:
    from firebase_admin import initialize_app, credentials, auth
    from firebase_admin.exceptions import FirebaseError
except ImportError:
    # Firebase Admin não instalado ainda
    initialize_app = None
    credentials = None
    auth = None
    FirebaseError = Exception

logger = logging.getLogger(__name__)

# Variável global para verificar se já foi inicializado
_firebase_app = None

def get_firebase_app():
    """
    Inicializa e retorna a instância do Firebase Admin App
    """
    global _firebase_app
    
    if _firebase_app is not None:
        return _firebase_app
    
    # Verifica se firebase_admin está instalado
    if initialize_app is None:
        logger.warning("Firebase Admin SDK não está instalado. Execute: pip install firebase-admin")
        return None
    
    try:
        # Tenta primeiro ler de variável de ambiente (base64) - para Railway
        firebase_credentials_base64 = os.getenv('FIREBASE_ADMIN_CREDENTIALS_BASE64')
        
        if firebase_credentials_base64:
            # Decodifica o JSON da variável de ambiente
            credentials_dict = json.loads(base64.b64decode(firebase_credentials_base64).decode('utf-8'))
            cred = credentials.Certificate(credentials_dict)
            logger.info("Firebase Admin inicializado usando credenciais de variável de ambiente")
        else:
            # Fallback: tenta ler do arquivo (para desenvolvimento local)
            firebase_credentials_file = os.getenv('FIREBASE_ADMIN_CREDENTIALS_FILE', 'firebase-admin-credentials.json')
            
            if os.path.exists(firebase_credentials_file):
                cred = credentials.Certificate(firebase_credentials_file)
                logger.info("Firebase Admin inicializado usando arquivo de credenciais")
            else:
                # Tenta usar credenciais individuais de variáveis de ambiente
                project_id = os.getenv('FIREBASE_ADMIN_PROJECT_ID')
                private_key = os.getenv('FIREBASE_ADMIN_PRIVATE_KEY')
                client_email = os.getenv('FIREBASE_ADMIN_CLIENT_EMAIL')
                
                if project_id and private_key and client_email:
                    # Substitui \n por quebras de linha reais na chave privada
                    private_key = private_key.replace('\\n', '\n')
                    
                    cred = credentials.Certificate({
                        "type": "service_account",
                        "project_id": project_id,
                        "private_key_id": os.getenv('FIREBASE_ADMIN_PRIVATE_KEY_ID', ''),
                        "private_key": private_key,
                        "client_email": client_email,
                        "client_id": os.getenv('FIREBASE_ADMIN_CLIENT_ID', ''),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        "client_x509_cert_url": ""
                    })
                    logger.info("Firebase Admin inicializado usando variáveis de ambiente individuais")
                else:
                    raise FileNotFoundError(
                        "Credenciais do Firebase Admin não encontradas. "
                        "Configure FIREBASE_ADMIN_CREDENTIALS_BASE64, FIREBASE_ADMIN_CREDENTIALS_FILE "
                        "ou as variáveis individuais (FIREBASE_ADMIN_PROJECT_ID, FIREBASE_ADMIN_PRIVATE_KEY, FIREBASE_ADMIN_CLIENT_EMAIL)"
                    )
        
        _firebase_app = initialize_app(cred)
        logger.info("Firebase Admin SDK inicializado com sucesso")
        return _firebase_app
        
    except Exception as e:
        logger.error(f"Erro ao inicializar Firebase Admin: {e}")
        raise

def verify_id_token(token: str):
    """
    Verifica e decodifica um token ID do Firebase
    
    Args:
        token: Token ID do Firebase
        
    Returns:
        dict: Dados decodificados do token (claims)
        
    Raises:
        ValueError: Se o token for inválido
        FirebaseError: Se houver erro na verificação
    """
    try:
        app = get_firebase_app()
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except ValueError as e:
        logger.error(f"Token inválido: {e}")
        raise
    except FirebaseError as e:
        logger.error(f"Erro ao verificar token: {e}")
        raise

