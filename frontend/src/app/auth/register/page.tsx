'use client'

import { useState } from 'react'
import api from '@/lib/api'

export default function RegisterPage() {
  const [form, setForm] = useState({
    name: '',
    email: '',
    phone: '',
    password: '',
    role: 'player',
  })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [event.target.name]: event.target.value })
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError('')
    setMessage('')

    try {
      const response = await api.post('/api/v1/auth/register', {
        ...form,
        phone: form.phone || undefined,
      })
      setMessage(response.data.message)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed')
    }
  }

  return (
    <main className="page">
      <section className="hero">
        <h1>Register</h1>
        <form onSubmit={handleSubmit} className="form-grid">
          <label>
            Name
            <input name="name" value={form.name} onChange={handleChange} required />
          </label>
          <label>
            Email
            <input name="email" type="email" value={form.email} onChange={handleChange} required />
          </label>
          <label>
            Phone
            <input name="phone" type="tel" value={form.phone} onChange={handleChange} />
          </label>
          <label>
            Password
            <input name="password" type="password" value={form.password} onChange={handleChange} required minLength={6} />
          </label>
          <label>
            Role
            <select name="role" value={form.role} onChange={handleChange}>
              <option value="player">Player</option>
              <option value="team_owner">Team Owner</option>
              <option value="admin">Admin</option>
              <option value="moderator">Moderator</option>
            </select>
          </label>
          <button type="submit">Register</button>
        </form>

        {message && <p className="success">{message}</p>}
        {error && <p className="error">{error}</p>}
      </section>
    </main>
  )
}
