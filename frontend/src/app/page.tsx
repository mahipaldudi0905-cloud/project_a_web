import Link from 'next/link'

export default function Home() {
  return (
    <main className="page">
      <section className="hero">
        <h1>CricAuction Frontend</h1>
        <p>Connects to your FastAPI backend at <strong>http://localhost:8000</strong></p>
        <div className="cards">
          <Link className="card" href="/auth/register">Register</Link>
          <Link className="card" href="/auth/login">Login</Link>
          <Link className="card" href="/players">Players</Link>
          <Link className="card" href="/auctions">Auctions</Link>
          <Link className="card" href="/teams">Teams</Link>
          <Link className="card" href="/wallet">Wallet</Link>
        </div>
      </section>
    </main>
  )
}
