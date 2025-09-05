import api, { setAuthToken, getToken } from './api';

// --- LOGIN ---
export const loginUser = async (credentials) => {
  try {
    const res = await api.post('accounts/login/', credentials);
    const token = res.data.access || res.data.token; // selon backend
    if (token) setAuthToken(token);
    return res.data;
  } catch (err) {
    throw err;
  }
};

// --- LOGOUT ---
export const logoutUser = () => {
  setAuthToken(null);
};

// --- CHECK IF LOGGED IN ---
export const isAuthenticated = () => {
  const token = getToken();
  return !!token;
};

// --- GET CURRENT USER PROFILE ---
export const getCurrentUser = async () => {
  try {
    const res = await api.get('accounts/me/');
    return res.data;
  } catch (err) {
    throw err;
  }
};

// --- REFRESH TOKEN (si JWT refresh côté backend) ---
export const refreshToken = async () => {
  try {
    const refresh = localStorage.getItem('refresh');
    if (!refresh) return null;

    const res = await api.post('accounts/token/refresh/', { refresh });
    const access = res.data.access;
    setAuthToken(access);
    return access;
  } catch (err) {
    logoutUser();
    throw err;
  }
};
