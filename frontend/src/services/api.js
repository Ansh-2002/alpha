import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const peopleApi = {
  getAll: () => api.get('/people'),
  getById: (id) => api.get(`/people/${id}`),
  create: (person) => api.post('/people', person),
};

export const companiesApi = {
  getAll: () => api.get('/companies'),
  getById: (id) => api.get(`/companies/${id}`),
  getSnippets: (id) => api.get(`/companies/${id}/snippets`),
};

export const enrichmentApi = {
  enrich: (personId) => api.post(`/enrich/${personId}`),
  getJobStatus: (jobId) => api.get(`/job/${jobId}`),
};

export default api;