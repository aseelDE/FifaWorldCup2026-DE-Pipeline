'use client'

import { useState, useEffect } from 'react'

const API = 'http://localhost:8000'

const tabs = [
  { id: 'standings', label: 'Group Standings', icon: '🏆' },
  { id: 'matches', label: 'Match Results', icon: '⚽' },
  { id: 'scorers', label: 'Top Scorers', icon: '🥅' },
  { id: 'teams', label: 'Team Stats', icon: '👥' },
  { id: 'knockout', label: 'Knockout', icon: '🏅' },
]

export default function Home() {
  const [activeTab, setActiveTab] = useState('standings')
  const [data, setData] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const endpoints = {
      standings: '/standings',
      matches: '/matches',
      scorers: '/top-scorers',
      teams: '/team-stats',
      knockout: '/knockout',
    }
    const fetchAll = async () => {
      setLoading(true)
      try {
        const results = await Promise.all(
          Object.entries(endpoints).map(async ([key, path]) => {
            const res = await fetch(`${API}${path}`)
            const json = await res.json()
            return [key, json]
          })
        )
        setData(Object.fromEntries(results))
      } catch (e) {
        setError('Could not connect to the API. Make sure the backend is running.')
      } finally {
        setLoading(false)
      }
    }
    fetchAll()
  }, [])

  return (
    <main className="min-h-screen" style={{ background: '#0a1628', fontFamily: "'Bebas Neue', 'Oswald', sans-serif" }}>

      {/* Hero Header */}
      <div style={{
        background: 'linear-gradient(135deg, #0a1628 0%, #1a2f4e 50%, #0d2137 100%)',
        borderBottom: '2px solid #c9a227',
        padding: '2rem 1.5rem 1.5rem',
        textAlign: 'center',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{
          position: 'absolute', inset: 0, opacity: 0.04,
          backgroundImage: 'repeating-linear-gradient(45deg, #c9a227 0, #c9a227 1px, transparent 0, transparent 50%)',
          backgroundSize: '20px 20px'
        }} />
        <div style={{ position: 'relative', zIndex: 1 }}>
          <div style={{ color: '#c9a227', fontSize: '0.8rem', letterSpacing: '0.4em', marginBottom: '0.5rem' }}>
            USA · CANADA · MEXICO
          </div>
          <h1 style={{
            color: '#ffffff', fontSize: 'clamp(2.5rem, 6vw, 4.5rem)',
            margin: '0 0 0.25rem', letterSpacing: '0.05em', lineHeight: 1
          }}>
            FIFA WORLD CUP
          </h1>
          <div style={{
            color: '#c9a227', fontSize: 'clamp(2rem, 5vw, 3.5rem)',
            letterSpacing: '0.1em', lineHeight: 1
          }}>2026</div>
          <div style={{
            marginTop: '0.75rem', color: '#7a9bc4', fontSize: '0.8rem',
            letterSpacing: '0.2em', fontFamily: 'system-ui, sans-serif'
          }}>
            DATA ENGINEERING PIPELINE — 2022 QATAR DATA
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{
        display: 'flex', overflowX: 'auto', borderBottom: '1px solid #1e3a5f',
        background: '#0d1f35', padding: '0 1rem'
      }}>
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              background: 'none', border: 'none', cursor: 'pointer',
              padding: '1rem 1.5rem', whiteSpace: 'nowrap',
              color: activeTab === tab.id ? '#c9a227' : '#4a7099',
              borderBottom: activeTab === tab.id ? '3px solid #c9a227' : '3px solid transparent',
              fontSize: '0.95rem', letterSpacing: '0.08em',
              fontFamily: "'Bebas Neue', 'Oswald', sans-serif",
              transition: 'color 0.2s'
            }}
          >
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div style={{ padding: '1.5rem', maxWidth: '1200px', margin: '0 auto' }}>
        {loading && (
          <div style={{ textAlign: 'center', padding: '4rem', color: '#c9a227', fontSize: '1.2rem', letterSpacing: '0.1em' }}>
            LOADING DATA...
          </div>
        )}
        {error && (
          <div style={{
            background: '#1a0a0a', border: '1px solid #7a1f1f', borderRadius: '8px',
            padding: '1.5rem', color: '#f08080', fontFamily: 'system-ui, sans-serif', fontSize: '0.9rem'
          }}>
            ⚠️ {error}
          </div>
        )}
        {!loading && !error && (
          <>
            {activeTab === 'standings' && <StandingsTab data={data.standings || []} />}
            {activeTab === 'matches' && <MatchesTab data={data.matches || []} />}
            {activeTab === 'scorers' && <ScorersTab data={data.scorers || []} />}
            {activeTab === 'teams' && <TeamsTab data={data.teams || []} />}
            {activeTab === 'knockout' && <KnockoutTab data={data.knockout || []} />}
          </>
        )}
      </div>
    </main>
  )
}

/* ── Group Standings ── */
function StandingsTab({ data }) {
  const groups = {}
  data.forEach(row => {
    if (!groups[row.group_name]) groups[row.group_name] = []
    groups[row.group_name].push(row)
  })

  return (
    <div>
      <SectionTitle>Group Stage Standings</SectionTitle>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: '1rem' }}>
        {Object.entries(groups).map(([group, teams]) => (
          <div key={group} style={{
            background: '#0d1f35', border: '1px solid #1e3a5f',
            borderRadius: '8px', overflow: 'hidden'
          }}>
            <div style={{
              background: '#c9a227', padding: '0.5rem 1rem',
              color: '#0a1628', fontSize: '1rem', letterSpacing: '0.1em'
            }}>
              {group}
            </div>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontFamily: 'system-ui, sans-serif' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid #1e3a5f' }}>
                  {['#', 'Team', 'P', 'W', 'D', 'L', 'Pts'].map(h => (
                    <th key={h} style={{
                      padding: '0.4rem 0.5rem', color: '#4a7099',
                      fontSize: '0.7rem', letterSpacing: '0.1em', textAlign: h === 'Team' ? 'left' : 'center'
                    }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {teams.map((team, i) => (
                  <tr key={team.team_name} style={{
                    borderBottom: '1px solid #132a44',
                    background: i < 2 ? 'rgba(201,162,39,0.05)' : 'transparent'
                  }}>
                    <td style={{ padding: '0.5rem', textAlign: 'center', color: i < 2 ? '#c9a227' : '#4a7099', fontSize: '0.8rem' }}>{team.rank}</td>
                    <td style={{ padding: '0.5rem', color: '#e8eef5', fontSize: '0.85rem' }}>{team.team_name}</td>
                    <td style={{ padding: '0.5rem', textAlign: 'center', color: '#7a9bc4', fontSize: '0.8rem' }}>{team.played}</td>
                    <td style={{ padding: '0.5rem', textAlign: 'center', color: '#7a9bc4', fontSize: '0.8rem' }}>{team.wins}</td>
                    <td style={{ padding: '0.5rem', textAlign: 'center', color: '#7a9bc4', fontSize: '0.8rem' }}>{team.draws}</td>
                    <td style={{ padding: '0.5rem', textAlign: 'center', color: '#7a9bc4', fontSize: '0.8rem' }}>{team.losses}</td>
                    <td style={{ padding: '0.5rem', textAlign: 'center', color: '#c9a227', fontWeight: 'bold', fontSize: '0.9rem' }}>{team.points}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </div>
  )
}

/* ── Match Results ── */
function MatchesTab({ data }) {
  return (
    <div>
      <SectionTitle>Match Results</SectionTitle>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {data.map((match, i) => (
          <div key={i} style={{
            background: '#0d1f35', border: '1px solid #1e3a5f',
            borderRadius: '8px', padding: '0.75rem 1rem',
            display: 'grid', gridTemplateColumns: '1fr auto 1fr auto',
            alignItems: 'center', gap: '0.5rem', fontFamily: 'system-ui, sans-serif'
          }}>
            <div style={{ textAlign: 'right', color: '#e8eef5', fontSize: '0.9rem' }}>{match.home_team}</div>
            <div style={{
              background: '#0a1628', border: '1px solid #1e3a5f',
              borderRadius: '6px', padding: '0.25rem 0.75rem',
              color: '#c9a227', fontSize: '1.1rem', fontWeight: 'bold',
              letterSpacing: '0.1em', minWidth: '60px', textAlign: 'center'
            }}>
              {match.home_goals} - {match.away_goals}
            </div>
            <div style={{ color: '#e8eef5', fontSize: '0.9rem' }}>{match.away_team}</div>
            <div style={{
              fontSize: '0.7rem', color: match.result === 'Home Win' ? '#5cb85c' : match.result === 'Away Win' ? '#d9534f' : '#f0ad4e',
              textAlign: 'right', letterSpacing: '0.05em'
            }}>
              {match.result}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

/* ── Top Scorers ── */
function ScorersTab({ data }) {
  return (
    <div>
      <SectionTitle>Top Scorers</SectionTitle>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {data.slice(0, 20).map((player, i) => (
          <div key={i} style={{
            background: '#0d1f35', border: '1px solid #1e3a5f',
            borderRadius: '8px', padding: '0.75rem 1rem',
            display: 'flex', alignItems: 'center', gap: '1rem',
            fontFamily: 'system-ui, sans-serif'
          }}>
            <div style={{
              color: i < 3 ? '#c9a227' : '#4a7099',
              fontSize: i < 3 ? '1.2rem' : '0.9rem',
              minWidth: '2rem', textAlign: 'center', fontWeight: 'bold'
            }}>
              {i + 1}
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ color: '#e8eef5', fontSize: '0.95rem' }}>{player.name}</div>
              <div style={{ color: '#4a7099', fontSize: '0.75rem' }}>{player.nationality} · {player.team}</div>
            </div>
            <div style={{
              background: '#c9a227', color: '#0a1628', borderRadius: '20px',
              padding: '0.2rem 0.8rem', fontSize: '0.9rem', fontWeight: 'bold'
            }}>
              {player.total_goals} {player.total_goals === 1 ? 'goal' : 'goals'}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

/* ── Team Stats ── */
function TeamsTab({ data }) {
  return (
    <div>
      <SectionTitle>Team Stats</SectionTitle>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '0.75rem' }}>
        {data.map((team, i) => (
          <div key={i} style={{
            background: '#0d1f35', border: '1px solid #1e3a5f',
            borderRadius: '8px', padding: '1rem',
            fontFamily: 'system-ui, sans-serif'
          }}>
            <div style={{ color: '#c9a227', fontSize: '1rem', marginBottom: '0.5rem', letterSpacing: '0.05em' }}>
              {team.team_name}
            </div>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              <Stat label="Players" value={team.total_players} />
              <Stat label="Positions" value={team.positions_count} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

/* ── Knockout Results ── */
function KnockoutTab({ data }) {
  return (
    <div>
      <SectionTitle>Knockout Stage</SectionTitle>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {data.map((match, i) => (
          <div key={i} style={{
            background: '#0d1f35', border: '1px solid #1e3a5f',
            borderLeft: '3px solid #c9a227',
            borderRadius: '8px', padding: '0.75rem 1rem',
            display: 'grid', gridTemplateColumns: '1fr auto 1fr auto',
            alignItems: 'center', gap: '0.5rem', fontFamily: 'system-ui, sans-serif'
          }}>
            <div style={{ textAlign: 'right', color: match.result === 'Home Win' ? '#e8eef5' : '#4a7099', fontSize: '0.9rem' }}>{match.home_team}</div>
            <div style={{
              background: '#0a1628', border: '1px solid #c9a227',
              borderRadius: '6px', padding: '0.25rem 0.75rem',
              color: '#c9a227', fontSize: '1.1rem', fontWeight: 'bold',
              letterSpacing: '0.1em', minWidth: '60px', textAlign: 'center'
            }}>
              {match.home_goals} - {match.away_goals}
            </div>
            <div style={{ color: match.result === 'Away Win' ? '#e8eef5' : '#4a7099', fontSize: '0.9rem' }}>{match.away_team}</div>
            <div style={{ fontSize: '0.7rem', color: '#c9a227', textAlign: 'right', letterSpacing: '0.05em' }}>
              {match.result}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

/* ── Helpers ── */
function SectionTitle({ children }) {
  return (
    <h2 style={{
      color: '#c9a227', fontSize: '1.5rem', letterSpacing: '0.1em',
      margin: '0 0 1rem', borderBottom: '1px solid #1e3a5f', paddingBottom: '0.5rem'
    }}>
      {children}
    </h2>
  )
}

function Stat({ label, value }) {
  return (
    <div style={{
      background: '#0a1628', borderRadius: '6px', padding: '0.4rem 0.75rem',
      textAlign: 'center'
    }}>
      <div style={{ color: '#c9a227', fontSize: '1rem', fontWeight: 'bold' }}>{value}</div>
      <div style={{ color: '#4a7099', fontSize: '0.65rem', letterSpacing: '0.05em' }}>{label}</div>
    </div>
  )
}