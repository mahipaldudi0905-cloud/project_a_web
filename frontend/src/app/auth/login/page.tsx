'use client'

import { useState } from 'react'
import api from '@/lib/api'

export default function LoginPage() {
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [event.target.name]: event.target.value })
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError('')
    setSuccess('')

    try {
      const response = await api.post('/api/v1/auth/login', form)
      setSuccess('Login successful! Token received.')
      console.log('tokens', response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <main className="page">
      <section className="hero">
        <h1>Login</h1>
        <form onSubmit={handleSubmit} className="form-grid">
          <label>
            Email
            <input name="email" type="email" value={form.email} onChange={handleChange} required />
          </label>
          <label>
            Password
            <input name="password" type="password" value={form.password} onChange={handleChange} required />
          </label>
          <button type="submit">Login</button>
        </form>

        {success && <p className="success">{success}</p>}
        {error && <p className="error">{error}</p>}
      </section>
    </main>
  )
}
