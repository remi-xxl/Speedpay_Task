# Digital Wallet API

A simple securedigital wallets. Supports user registration, JWT authentication, deposits, withdrawals, and transfer.

##live server
https://speedpay-task-1.onrender.com

## Features

- User registration with automatic 6-digit account number generation
- JWT-based authentication
- Wallet operations: deposit, withdraw, balance check, transfer
- Admin functionality to view all users
- Secure password hashing
- PostgreSQL database

## Requirements

- Python 3.11+
- PostgreSQL
- Docker (optional, for containerized deployment)


### Manual Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up PostgreSQL database (locally or via Docker):
   ```bash
   docker run --name postgres-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=digital_wallet -p 5432:5432 -d postgres:17
   ```

3. Update `app/core/config.py` with your database connection details.

4. Run the application:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
   ```

5. The API will be available at `http://localhost:8001`

## API Documentation

The API documentation is available at `http://localhost:8001/docs` (Swagger UI) or `http://localhost:8001/redoc` (ReDoc).

### Authentication

All wallet endpoints require JWT authentication. Obtain a token by logging in.

### Endpoints

#### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT token

#### Wallet Operations (Authenticated)

- `GET /wallet/balance` - Get current balance
- `POST /wallet/deposit` - Deposit funds
- `POST /wallet/withdraw` - Withdraw funds
- `POST /wallet/transfer` - Transfer funds to another user

#### Admin (Admin only)

- `GET /admin/users` - Get all users

### Example Usage

1. Register a user:
   ```bash
   curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"full_name": "John Doe", "email": "john@example.com", "password": "securepass123"}'
   ```

2. Login:
   ```bash
   curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john@example.com&password=securepass123"
   ```

3. Use the token for authenticated requests:
   ```bash
   curl -X GET "http://localhost:8000/wallet/balance" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
   ```

## Security

- Passwords are hashed using bcrypt
- JWT tokens expire after 30 minutes
- Users can only access their own wallet data
- Admins can view all user information
- Transfers cannot be made to the sender's own account

## Database

The application uses PostgreSQL with SQLAlchemy ORM. 

## Testing

Run tests with:
```bash
pytest
```
