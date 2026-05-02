import axios, { type InternalAxiosRequestConfig } from 'axios'
import type { BackendGreska } from '@/types/api'

export class ApiGreska extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly status: number,
  ) {
    super(message)
    this.name = 'ApiGreska'
  }
}

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.set('Authorization', `Bearer ${token}`)
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (axios.isAxiosError(error) && error.response) {
      const data = error.response.data as Partial<BackendGreska>
      throw new ApiGreska(
        data.code ?? 'unknown_error',
        data.message ?? error.message,
        error.response.status,
      )
    }
    throw error
  },
)
