import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
})

export const hcpApi = {
  list: () => api.get('/hcps/').then((r) => r.data),
  create: (payload) => api.post('/hcps/', payload).then((r) => r.data),
}

export const interactionApi = {
  listForHcp: (hcpId) =>
    api.get('/interactions/', { params: { hcp_id: hcpId } }).then((r) => r.data),
  create: (payload) => api.post('/interactions/', payload).then((r) => r.data),
  update: (id, payload) => api.put(`/interactions/${id}`, payload).then((r) => r.data),
}

export const chatApi = {
  send: (message, threadId) =>
    api.post('/ai/chat', { message, thread_id: threadId }).then((r) => r.data),
}
