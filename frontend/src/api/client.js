import axios from 'axios'

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
})

export async function getHealth() {
  const { data } = await api.get('/health')
  return data
}

export async function getModelInfo() {
  const { data } = await api.get('/model-info')
  return data
}

export async function predict(clientFeatures) {
  const { data } = await api.post('/predict', clientFeatures)
  return data
}

export async function getStats() {
  const { data } = await api.get('/stats')
  return data
}
