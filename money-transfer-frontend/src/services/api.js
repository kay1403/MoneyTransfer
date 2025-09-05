import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || '/api/';

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  withCredentials: true, // pour cookies httpOnly
});

// --- Auth Token helpers ---
export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    localStorage.setItem('access', token);
  } else {
    delete api.defaults.headers.common['Authorization'];
    localStorage.removeItem('access');
  }
};

export const getToken = () => {
  return localStorage.getItem('access');
};

// --- Auth ---
export const login = async (credentials) => {
  const response = await api.post('core/login/', credentials);
  return response.data.user; // user info seulement
};

// logout : juste supprimer côté frontend
export const logout = () => {
  setAuthToken(null);
  window.location.href = '/';
};

// --- Transactions ---
export const getTransactions = async () => {
  const response = await api.get('core/transactions/');
  return response.data;
};

export const createTransaction = async (formData) => {
  const response = await api.post('core/transactions/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

// --- Currency conversion ---
export const convertCurrency = async (fromCurrency, toCurrency, amount) => {
  const response = await api.post('core/convert/', { from_currency: fromCurrency, to_currency: toCurrency, amount });
  return response.data;
};

// --- Download PDF receipt ---
export const downloadReceipt = async (transactionId) => {
  const token = getToken();
  const response = await fetch(`${API_URL}transactions/receipt/${transactionId}/`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!response.ok) throw new Error('Failed to download receipt');
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `receipt_${transactionId}.pdf`;
  document.body.appendChild(a);
  a.click();
  a.remove();
};

export default api;

// --- Interceptor refresh automatique ---
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        await api.post('core/token/refresh/', {}, { withCredentials: true });
        return api(originalRequest); // retry request
      } catch (err) {
        logout();
        return Promise.reject(err);
      }
    }
    return Promise.reject(error);
  }
);
