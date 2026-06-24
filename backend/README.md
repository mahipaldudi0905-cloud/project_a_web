# CricAuction Backend

Production-ready Cricket Auction Platform API built with FastAPI, SQLModel, and MySQL.

## Features

- ✅ User Authentication & Authorization (JWT)
- ✅ Player Management
- ✅ Team Management
- ✅ Real-time Auction System
- ✅ Bidding System
- ✅ Wallet & Payment Integration (Razorpay, Stripe, Cashfree)
- ✅ Transaction Management
- ✅ Notifications (Email, SMS, In-App)
- ✅ Reports & Analytics
- ✅ Role-based Access Control (RBAC)

## Tech Stack

- **Framework**: FastAPI
- **Database**: MySQL with SQLModel ORM
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Passlib with Bcrypt
- **Email**: SMTP
- **Payment**: Razorpay, Stripe, Cashfree
- **Testing**: Pytest
- **Deployment**: Docker, Docker Compose

## Project Structure

```
backend/
├── app/
│   ├── api/v1/
│   │   ├── auth/
│   │   ├── users/
│   │   ├── players/
│   │   ├── teams/
│   │   ├── auctions/
│   │   ├── bids/
│   │   ├── wallets/
│   │   ├── payments/
│   │   ├── notifications/
│   │   └── reports/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   ├── utils/
│   ├── websocket/
│   └── main.py
├── alembic/
├── tests/
├── .env.example
├── requirements.txt
├── docker-compose.yml
└── Dockerfile
```

## Installation

### Prerequisites
- Python 3.11+
- MySQL 8.0+
- Redis (optional)

### Setup

1. **Clone and setup environment**
```bash
cd backend
cp .env.example .env
```

2. **Update .env with your configuration**
```bash
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/cricsauction
SECRET_KEY=your-secret-key
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create database**
```bash
# The database and tables will be created automatically on first run
```

5. **Run the application**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Docker Deployment

Run the entire stack with Docker Compose:

```bash
docker-compose up -d
```

This will start:
- MySQL database
- Redis cache
- FastAPI application

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/change-password` - Change password

### Users
- `GET /api/v1/users` - Get all users
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### Players
- `POST /api/v1/players` - Create player
- `GET /api/v1/players` - Get all players
- `GET /api/v1/players/{id}` - Get player by ID
- `PUT /api/v1/players/{id}` - Update player
- `DELETE /api/v1/players/{id}` - Delete player

### Teams
- `POST /api/v1/teams` - Create team
- `GET /api/v1/teams` - Get all teams
- `GET /api/v1/teams/{id}` - Get team by ID
- `PUT /api/v1/teams/{id}` - Update team

### Auctions
- `POST /api/v1/auctions` - Create auction
- `GET /api/v1/auctions` - Get all auctions
- `GET /api/v1/auctions/{id}` - Get auction details
- `PUT /api/v1/auctions/{id}` - Update auction
- `POST /api/v1/auctions/{id}/start` - Start auction
- `POST /api/v1/auctions/{id}/close` - Close auction
- `POST /api/v1/auctions/{id}/cancel` - Cancel auction

### Bids
- `POST /api/v1/bids` - Place bid
- `GET /api/v1/bids` - Get all bids
- `GET /api/v1/bids/history/{player_id}` - Get bid history

### Wallet
- `GET /api/v1/wallet` - Get wallet
- `POST /api/v1/wallet/deposit` - Deposit funds
- `POST /api/v1/wallet/withdraw` - Withdraw funds
- `GET /api/v1/wallet/transactions` - Get transaction history

### Payments
- `POST /api/v1/payment/create-order` - Create payment order
- `POST /api/v1/payment/verify` - Verify payment
- `POST /api/v1/payment/webhook` - Payment webhook

### Notifications
- `GET /api/v1/notifications` - Get notifications
- `PUT /api/v1/notifications/{id}/read` - Mark as read
- `PUT /api/v1/notifications/read-all` - Mark all as read

### Reports
- `GET /api/v1/reports/auction` - Get auction reports
- `GET /api/v1/reports/revenue` - Get revenue reports
- `GET /api/v1/reports/user` - Get user reports

## API Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database

Default roles are created automatically:
- admin
- team_owner
- player
- moderator

## Testing

Run tests with pytest:

```bash
pytest
pytest --cov=app
```

## Environment Variables

See `.env.example` for all available configuration options.

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.
