'use client'

import { useEffect, useState } from 'react'
import api from '@/lib/api'

type Team = {
  id: number
  name: string
  budget: number
  wallet_balance: number
  description?: string
}

export default function TeamsPage() {
  const [teams, setTeams] = useState<Team[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    async function fetchTeams() {
      try {
        const response = await api.get('/api/v1/teams')
        setTeams(response.data.data)
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Unable to load teams')
      }
    }

    fetchTeams()
  }, [])

  return (
    <main className="page">
      <section className="hero">
        <h1>Teams</h1>
        {error && <p className="error">{error}</p>}
        <div className="list-grid">
          {teams.map((team) => (
            <article key={team.id} className="card">
              <h2>{team.name}</h2>
              <p>{team.description}</p>
              <p>Budget: ₹{team.budget}</p>
              <p>Wallet: ₹{team.wallet_balance}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  )
}
