import axios from 'axios'

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || '/api' })

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Auth
export const register = (data) => api.post('/auth/register', data)
export const login = (data) => api.post('/auth/login', data)
export const getProfile = () => api.get('/auth/profile')

// Items
export const getItems = (params) => api.get('/items/', { params })
export const getItem = (id) => api.get(`/items/${id}`)

// Ratings
export const rateItem = (data) => api.post('/ratings/', data)
export const getMyRatings = () => api.get('/ratings/my')

// Recommendations
export const getRecommendations = (params) => api.get('/recommendations/', { params })

// Wishlist
export const getWishlist = () => api.get('/wishlist/')
export const addToWishlist = (item_id) => api.post('/wishlist/', { item_id })
export const removeFromWishlist = (item_id) => api.delete(`/wishlist/${item_id}`)

// Search
export const searchItems = (params) => api.get('/search/', { params })

// Admin
export const adminAddItem = (data) => api.post('/admin/items', data)
export const adminListUsers = () => api.get('/admin/users')
export const adminDeleteUser = (id) => api.delete(`/admin/users/${id}`)
export const adminStats = () => api.get('/admin/stats')

export default api
