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
  console.error('Erro: Variáveis de ambiente do Firebase não configuradas:', missingVars)
  throw new Error(`Variáveis de ambiente do Firebase não configuradas: ${missingVars.join(', ')}`)
}

// Inicializar Firebase
const app = initializeApp(firebaseConfig)

// Inicializar Firebase Authentication
export const auth = getAuth(app)

// Exportar app para uso futuro (se necessário)
export default app

