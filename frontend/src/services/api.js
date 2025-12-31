import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: parseInt(import.meta.env.VITE_API_TIMEOUT) || 10000,
})

// Request interceptor - add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear auth and redirect to login
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth endpoints
export const auth = {
  login: (email, password) =>
    api.post('/api/auth/login', { email, password }),
  register: (email, password) =>
    api.post('/api/auth/register', { email, password }),
  logout: () => {
    localStorage.removeItem('auth_token')
    return Promise.resolve()
  },
}

// Rules endpoints
export const rules = {
  getAll: () => api.get('/api/rules'),
  getById: (id) => api.get(`/api/rules/${id}`),
  create: (data) => api.post('/api/rules', data),
  update: (id, data) => api.put(`/api/rules/${id}`, data),
  delete: (id) => api.delete(`/api/rules/${id}`),
}

// Logs endpoints
export const logs = {
  getComments: (skip = 0, limit = 20) =>
    api.get('/api/logs/comments', { params: { skip, limit } }),
  getDMs: (skip = 0, limit = 20) =>
    api.get('/api/logs/dms', { params: { skip, limit } }),
  getStats: () => api.get('/api/logs/stats'),
}

// Health check
export const health = {
  check: () => api.get('/health'),
}

export default api