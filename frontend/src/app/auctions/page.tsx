'use client'

import { useEffect, useState } from 'react'
import api from '@/lib/api'

type Auction = {
  id: number
  title: string
  description?: string
  status: string
  minimum_increment: number
}

export default function AuctionsPage() {
  const [auctions, setAuctions] = useState<Auction[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    async function fetchAuctions() {
      try {
        const response = await api.get('/api/v1/auctions')
        setAuctions(response.data.data)
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Unable to load auctions')
      }
    }

    fetchAuctions()
  }, [])

  return (
    <main className="page">
      <section className="hero">
        <h1>Auctions</h1>
        {error && <p className="error">{error}</p>}
        <div className="list-grid">
          {auctions.map((auction) => (
            <article key={auction.id} className="card">
              <h2>{auction.title}</h2>
              <p>{auction.description}</p>
              <p>Status: {auction.status}</p>
              <p>Min Increment: ₹{auction.minimum_increment}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  )
}
