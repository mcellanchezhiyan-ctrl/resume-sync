/**
 * Reusable API client for the Resume Sync Platform backend.
 *
 * In development, requests go to relative paths like `/api/health` and the
 * Vite dev server proxies them to http://localhost:8000 (see vite.config.ts).
 * For a deployed backend, set VITE_API_BASE_URL (e.g. "https://api.example.com").
 */

export const API_BASE: string = import.meta.env.VITE_API_BASE_URL ?? ''

export class ApiError extends Error {
  status: number
  detail: unknown

  constructor(status: number, detail: unknown, message?: string) {
    super(message ?? `API error ${status}`)
    this.name = 'ApiError'
    this.status = status
    this.detail = detail
  }
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(init.headers ?? {}),
    },
    ...init,
  })

  if (!response.ok) {
    let detail: unknown = null
    try {
      detail = await response.json()
    } catch {
      // Non-JSON error body; keep the plain status.
    }
    throw new ApiError(response.status, detail)
  }

  return (await response.json()) as T
}

// --- Types mirroring docs/api-contract.md ---

export interface HealthResponse {
  status: 'ok' | 'degraded'
  app: string
  version: string
  environment: string
  database: 'connected' | 'unavailable'
  time: string
}

export interface ExperienceEntry {
  company: string
  role: string
  start?: string | null
  end?: string | null
  highlights?: string[]
}

export interface EducationEntry {
  institution: string
  degree?: string | null
  start?: string | null
  end?: string | null
}

export interface Profile {
  id: number
  full_name: string | null
  headline: string | null
  location: string | null
  email: string | null
  phone: string | null
  summary: string | null
  skills: string[]
  experiences: ExperienceEntry[]
  education: EducationEntry[]
  links: Record<string, string>
  updated_at: string
}

export type SyncSource = 'github' | 'leetcode' | 'linkedin'

export interface SyncResult {
  source: SyncSource
  status: 'planned' | 'ok' | 'error' | 'skipped'
  message: string
  records_fetched: number
  started_at: string
  finished_at: string | null
}

export interface SyncHistoryEntry {
  id: number
  source: string
  status: string
  message: string | null
  records_fetched: number
  started_at: string
  finished_at: string | null
}

export interface ResumeDraft {
  title: string
  generated_at: string
  based_on_profile_id: number
  summary: string | null
  skills: string[]
  experiences: ExperienceEntry[]
  education: EducationEntry[]
  notes: string[]
}

export interface ResumeGenerateRequest {
  title?: string
  sections?: string[]
  include_external_synced_data?: boolean
}

// --- Endpoints ---

export const api = {
  health: () => request<HealthResponse>('/api/health'),

  getProfile: () => request<Profile>('/api/profile'),

  updateProfile: (payload: Partial<Profile>) =>
    request<Profile>('/api/profile', {
      method: 'PUT',
      body: JSON.stringify(payload),
    }),

  /* Syncs are planned backend features: currently the API answers 501 with a
   * SyncResult payload of status "planned"; the thrown ApiError carries it in
   * `.detail`. */
  triggerSync: (source: SyncSource, body: { username?: string; dry_run?: boolean } = {}) =>
    request<SyncResult>(`/api/sync/${source}`, {
      method: 'POST',
      body: JSON.stringify(body),
    }),

  getSyncHistory: (limit = 50) =>
    request<SyncHistoryEntry[]>(`/api/sync/history?limit=${limit}`),

  generateResume: (request_body: ResumeGenerateRequest = {}) =>
    request<ResumeDraft>('/api/resume/generate', {
      method: 'POST',
      body: JSON.stringify(request_body),
    }),
}
