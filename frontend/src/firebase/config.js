import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'

// Configuração do Firebase
// As variáveis de ambiente serão configuradas no Railway
const firebaseConfig = {
  apiKey: process.env.VUE_APP_FIREBASE_API_KEY,
  authDomain: process.env.VUE_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.VUE_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.VUE_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.VUE_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.VUE_APP_FIREBASE_APP_ID
}

// Verificar se todas as variáveis estão configuradas
const requiredEnvVars = [
  'VUE_APP_FIREBASE_API_KEY',
  'VUE_APP_FIREBASE_AUTH_DOMAIN',
  'VUE_APP_FIREBASE_PROJECT_ID',
  'VUE_APP_FIREBASE_STORAGE_BUCKET',
  'VUE_APP_FIREBASE_MESSAGING_SENDER_ID',
  'VUE_APP_FIREBASE_APP_ID'
]

const missingVars = requiredEnvVars.filter(varName => !process.env[varName])

if (missingVars.length > 0 && process.env.NODE_ENV === 'production') {
  console.warn('Aviso: Variáveis de ambiente do Firebase não configuradas:', missingVars)
  console.warn('O sistema pode não funcionar corretamente sem essas variáveis.')
}

// Inicializar Firebase apenas se tiver configuração mínima
let app = null
try {
  if (firebaseConfig.apiKey && firebaseConfig.projectId) {
    app = initializeApp(firebaseConfig)
  } else {
    console.warn('Firebase não inicializado: configuração incompleta')
  }
} catch (error) {
  console.error('Erro ao inicializar Firebase:', error)
}

// Inicializar Firebase Authentication (apenas se app foi inicializado)
export const auth = app ? getAuth(app) : null

// Exportar app para uso futuro (se necessário)
export default app

