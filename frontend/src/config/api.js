// Configuração da API para diferentes ambientes
const getBackendUrl = () => {
  // Em desenvolvimento, usar localhost
  if (process.env.NODE_ENV === 'development') {
    return 'http://localhost:5000';
  }
  
  // Em produção, usar a variável de ambiente ou fallback
  return process.env.REACT_APP_BACKEND_URL || 'https://chat-lleria.onrender.com';
};

export const API_CONFIG = {
  BASE_URL: getBackendUrl(),
  ENDPOINTS: {
    CHAT: '/chat',
    ROLES: '/roles',
    ROLE_EXAMPLES: (roleId) => `/roles/${roleId}/examples`,
    HEALTH: '/health',
    CACHE_STATS: '/cache/stats',
    RATE_LIMIT_STATS: '/rate-limit/stats'
  }
};

export const getApiUrl = (endpoint) => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
}; 