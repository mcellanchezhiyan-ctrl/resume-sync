import { HealthCheck } from './components/HealthCheck'

/**
 * Minimal dashboard scaffold. The full profile/sync/resume UIs will be built
 * on the `feature/frontend-ui` branch - see docs/DEVELOPMENT.md.
 */

interface ModuleCard {
  title: string
  description: string
  status: 'Planned' | 'In progress'
}

const MODULES: ModuleCard[] = [
  {
    title: 'Profile',
    description: 'The user-approved resume data served by GET/PUT /api/profile.',
    status: 'Planned',
  },
  {
    title: 'Activity syncs',
    description: 'GitHub, LeetCode and LinkedIn imports, reviewed before they touch approved data.',
    status: 'Planned',
  },
  {
    title: 'Resume generator',
    description: 'Builds drafts from approved data via POST /api/resume/generate (preview available).',
    status: 'In progress',
  },
]

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <div>
          <h1>Resume Sync Platform</h1>
          <p className="tagline">Sync developer activity. Curate your story. Generate resumes.</p>
        </div>
        <HealthCheck />
      </header>

      <main className="dashboard">
        <section className="cards" aria-label="Product modules">
          {MODULES.map((module) => (
            <article key={module.title} className="card">
              <div className="card-head">
                <h2>{module.title}</h2>
                <span className={`pill ${module.status === 'Planned' ? 'pill-planned' : 'pill-progress'}`}>
                  {module.status}
                </span>
              </div>
              <p>{module.description}</p>
            </article>
          ))}
        </section>

        <p className="hint">
          Frontend scaffold only - the resume builder UI is developed on{' '}
          <code>feature/frontend-ui</code>. API contract: <code>docs/api-contract.md</code>.
        </p>
      </main>
    </div>
  )
}

export default App
