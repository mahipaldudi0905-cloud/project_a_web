'use client'

import { useEffect, useState } from 'react'
import api from '@/lib/api'

type Wallet = {
  balance: number
  locked_balance: number
}

export default function WalletPage() {
  const [wallet, setWallet] = useState<Wallet | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    async function fetchWallet() {
      try {
        const response = await api.get('/api/v1/wallet')
        setWallet(response.data)
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Unable to load wallet')
      }
    }

    fetchWallet()
  }, [])

  return (
    <main className="page">
      <section className="hero">
        <h1>Wallet</h1>
        {error && <p className="error">{error}</p>}
        {wallet ? (
          <div className="card">
            <p>Balance: ₹{wallet.balance}</p>
            <p>Locked: ₹{wallet.locked_balance}</p>
          </div>
        ) : (
          <p>Loading wallet...</p>
        )}
      </section>
    </main>
  )
}
