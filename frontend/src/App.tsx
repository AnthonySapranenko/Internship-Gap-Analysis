import { useEffect, useState } from 'react'

type ApiStatus =
  | { state: 'loading' }
  | { state: 'ok'; version: string }
  | { state: 'error' }

function App() {
  const [apiStatus, setApiStatus] = useState<ApiStatus>({ state: 'loading' })

  useEffect(() => {
    fetch('/api/health')
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        return response.json() as Promise<{ version: string }>
      })
      .then((data) => setApiStatus({ state: 'ok', version: data.version }))
      .catch(() => setApiStatus({ state: 'error' }))
  }, [])

  return (
    <main>
      <h1>Internship Skill Gap Analyzer</h1>
      <p className="muted">
        Turn internship requirements into an actionable plan for becoming a stronger candidate.
      </p>

      <div className="status">
        {apiStatus.state === 'loading' && <span>Checking backend…</span>}
        {apiStatus.state === 'ok' && (
          <span className="status-ok">Backend connected (v{apiStatus.version})</span>
        )}
        {apiStatus.state === 'error' && (
          <span className="status-error">
            Backend unreachable. Start it with <code>uvicorn</code> (see README).
          </span>
        )}
      </div>
    </main>
  )
}

export default App
