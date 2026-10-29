import { useCallback, useEffect, useState } from 'react'
import { api, ApiError, type HealthResponse as HealthData } from '../lib/api'

type Phase = 'loading' | 'ready' | 'error'

interface HealthState {
  phase: Phase
  data: HealthData | null
  error: string | null
}

/**
 * Calls GET /api/health and renders the backend status.
 * Expected to show "ok" whenever the backend is running.
 */
export function HealthCheck() {
  const [state, setState] = useState<HealthState>({ phase: 'loading', data: null, error: null })

  const load = useCallback(async () => {
    try {
      const data = await api.health()
      setState({ phase: 'ready', data, error: null })
    } catch (error) {
      const message =
        error instanceof ApiError
          ? `HTTP ${error.status}`
          : 'Network error - is the backend running on http://localhost:8000?'
      setState({ phase: 'error', data: null, error: message })
    }
  }, [])

  const retry = () => {
    setState({ phase: 'loading', data: null, error: null })
    void load()
  }

  useEffect(() => {
    // setState only happens after `await api.health()` in load(); the rule is
    // not async-aware.
    // oxlint-disable-next-line react(set-state-in-effect) react-hooks/set-state-in-effect
    void load()
  }, [load])

  if (state.phase === 'loading') {
    return <span className="badge badge-loading">checking API…</span>
  }

  if (state.phase === 'error' || state.data === null) {
    return (
      <button type="button" className="badge badge-error" onClick={retry} title={state.error ?? ''}>
        API offline — retry
      </button>
    )
  }

  const healthy = state.data.status === 'ok' && state.data.database === 'connected'
  return (
    <button
      type="button"
      className={`badge ${healthy ? 'badge-ok' : 'badge-warn'}`}
      onClick={retry}
      title={`backend v${state.data.version} (${state.data.environment})`}
    >
      {healthy ? 'API healthy' : 'API degraded'} · {state.data.database}
    </button>
  )
}
