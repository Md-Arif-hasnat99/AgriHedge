/**
 * API Service Layer
 * Handles all HTTP requests to the backend
 */

import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Constants from 'expo-constants';

const API_URL = Constants.expoConfig.extra.apiUrl || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response) => response.data,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = await AsyncStorage.getItem('refreshToken');
        const response = await axios.post(`${API_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const { access_token } = response.data;
        await AsyncStorage.setItem('token', access_token);

        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        await AsyncStorage.removeItem('token');
        await AsyncStorage.removeItem('refreshToken');
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Authentication APIs
export const authAPI = {
  login: (username, password) =>
    apiClient.post('/auth/login', null, {
      params: { username, password },
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),

  register: (userData) => apiClient.post('/auth/register', userData),

  getCurrentUser: () => apiClient.get('/auth/me'),

  logout: () => apiClient.post('/auth/logout'),
};

// Price APIs
export const priceAPI = {
  getCurrentPrice: (commodity) =>
    apiClient.get(`/prices/current/${commodity}`),

  getPriceHistory: (commodity, days = 30) =>
    apiClient.get(`/prices/history/${commodity}`, { params: { days } }),

  getForecast: (commodity, days = 30) =>
    apiClient.post('/forecasts/predict', { commodity, forecast_days: days }),

  getVolatility: (commodity) =>
    apiClient.get(`/prices/volatility/${commodity}`),
};

// Contract APIs
export const contractAPI = {
  getUserContracts: () => apiClient.get('/contracts'),

  createContract: (contractData) =>
    apiClient.post('/contracts', contractData),

  getContractById: (contractId) =>
    apiClient.get(`/contracts/${contractId}`),

  getContractSummary: () => apiClient.get('/contracts/summary'),

  settleContract: (contractId, finalPrice) =>
    apiClient.post(`/contracts/${contractId}/settle`, { final_price: finalPrice }),
};

// Blockchain APIs
export const blockchainAPI = {
  getBlockchainInfo: () => apiClient.get('/blockchain/info'),

  getContractBlockchain: (contractId) =>
    apiClient.get(`/blockchain/contract/${contractId}`),

  getUserBlocks: () => apiClient.get('/blockchain/user-blocks'),
};

// Alert APIs
export const alertAPI = {
  getUserAlerts: () => apiClient.get('/alerts'),

  createAlert: (alertData) => apiClient.post('/alerts', alertData),

  deleteAlert: (alertId) => apiClient.delete(`/alerts/${alertId}`),

  updateAlert: (alertId, alertData) =>
    apiClient.put(`/alerts/${alertId}`, alertData),
};

export default apiClient;
