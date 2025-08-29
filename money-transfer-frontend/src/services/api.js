import axios from 'axios';

// URL de ton backend Render
const API_URL = 'https://moneyTransfer-db23.onrender.com/api/';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 10000, // 10 secondes
});

// Fonction pour définir le token JWT
export const setAuthToken = (token) => {
    if (token) {
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
        delete api.defaults.headers.common['Authorization'];
    }
};

export default api;
