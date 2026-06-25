# CricAuction Frontend

Next.js frontend for the CricAuction backend.

## Setup

```bash
cd frontend
npm install
npm run dev
```

## Environment

Create a `.env.local` file if you want to override the API URL:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Available pages

- `/` - Home
- `/auth/register` - User registration
- `/auth/login` - User login
- `/players` - Player list
- `/auctions` - Auction list
- `/teams` - Team list
- `/wallet` - Wallet info
