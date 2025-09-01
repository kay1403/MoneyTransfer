import axios from 'axios';

// URL du backend : utilise VITE_API_URL ou fallback sur le proxy /api/
const API_URL = import.meta.env.VITE_API_URL || '/api/';

// Instance Axios centrale (ne pas forcer Content-Type globalement pour permettre FormData)
const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
});

// Helper token local
const getToken = () => {
  try {
    return localStorage.getItem('token');
  } catch (e) {
    return null;
  }
};

export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    try { localStorage.setItem('token', token); } catch (e) {}
  } else {
    delete api.defaults.headers.common['Authorization'];
    try { localStorage.removeItem('token'); } catch (e) {}
  }
};

// Attacher automatiquement le token si présent
api.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token && !(config.headers && config.headers.Authorization)) {
      config.headers = config.headers || {};
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// --- AUTHENTIFICATION ---
// Note : backend expose /api/accounts/... via project urls.py
export const login = async (credentials) => {
  const response = await api.post('accounts/login/', credentials);
  return response.data; // { access, refresh } ou selon ton implémentation
};

export const register = async (userData) => {
  const response = await api.post('accounts/register/', userData);
  return response.data;
};

// --- TRANSACTIONS ---
export const getTransactions = async () => {
  const response = await api.get('transactions/');
  return response.data;
};

export const createTransaction = async (transactionData) => {
  // Si FormData, envoyer en multipart/form-data
  if (typeof FormData !== 'undefined' && transactionData instanceof FormData) {
    const response = await api.post('transactions/', transactionData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }
  const response = await api.post('transactions/', transactionData);
  return response.data;
};

// --- CONVERSION DE DEVISE ---
// route exposée sous /api/core/convert/
export const convertCurrency = async (fromCurrency, toCurrency, amount) => {
  const response = await api.post('core/convert/', {
    from_currency: fromCurrency,
    to_currency: toCurrency,
    amount,
  });
  return response.data;
};

// --- USERS ---
export const getUserProfile = async () => {
  // endpoint attendu : /api/accounts/me/ (à adapter si ton backend diffère)
  const response = await api.get('accounts/me/');
  return response.data;
};

// --- Déconnexion ---
export const logout = () => {
  setAuthToken(null);
};

export { getToken };
export default api;
