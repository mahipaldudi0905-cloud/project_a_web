'use client'

import { useEffect, useState } from 'react'
import api from '@/lib/api'

type Player = {
  id: number
  user_id: number
  age: number
  sport: string
  city: string
  state: string
  experience_years: number
  base_price: number
}

export default function PlayersPage() {
  const [players, setPlayers] = useState<Player[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    async function fetchPlayers() {
      try {
        const response = await api.get('/api/v1/players')
        setPlayers(response.data.data)
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Unable to load players')
      }
    }

    fetchPlayers()
  }, [])

  return (
    <main className="page">
      <section className="hero">
        <h1>Players</h1>
        {error && <p className="error">{error}</p>}
        <div className="list-grid">
          {players.map((player) => (
            <article key={player.id} className="card">
              <h2>{player.sport}</h2>
              <p>{player.city}, {player.state}</p>
              <p>Age: {player.age}</p>
              <p>Experience: {player.experience_years} years</p>
              <p>Base Price: ₹{player.base_price}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  )
}
