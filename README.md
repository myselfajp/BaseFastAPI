# FastAPI Base Project

A production-ready FastAPI base project with complete authentication system, email verification, password reset, and two-factor authentication support.

## Features

- ✅ **User Authentication**
  - JWT-based authentication
  - Email verification system
  - Password reset functionality
  - Two-factor authentication (2FA) support
  - Account lockout after failed login attempts

- ✅ **Security Features**
  - Password hashing with bcrypt
  - Rate limiting on authentication endpoints
  - Configurable email verification requirement
  - Optional forced 2FA for all users
  - Secure token-based email verification and password reset

- ✅ **Email Support**
  - Multiple email providers (AWS SES, SMTP)
  - HTML email templates
  - OTP delivery via email
  - Email verification
  - Password reset emails

- ✅ **Database**
  - PostgreSQL with SQLAlchemy ORM
  - Alembic migrations
  - Automatic database URL construction from components

- ✅ **Docker Support**
  - Docker Compose for development and production
  - Health checks
  - Volume persistence

## Project Structure

```
NewProject/
├── app/
│   ├── core/           # Core utilities (config, security, JWT, validation)
│   ├── db/             # Database configuration and session management
│   ├── model/          # SQLAlchemy models
│   ├── repository/     # Data access layer
│   ├── router/         # API endpoints
│   ├── schema/         # Pydantic schemas
│   ├── service/        # Business logic
│   └── main.py         # FastAPI application entry point
├── alembic/            # Database migrations
├── docker-compose.yml  # Development Docker setup
├── docker-compose.prod.yml  # Production Docker setup
├── Dockerfile          # Application Docker image
└── requirements.txt    # Python dependencies
```

## Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Docker and Docker Compose (optional, for containerized deployment)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd NewProject
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in all required values:

```bash
cp .env.example .env
```

Edit `.env` and configure the following:

#### Required Configuration

```env
# Project Configuration
PROJECT_NAME=Your Project Name
API_V1_PREFIX=/v1

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Database Components (DATABASE_URL will be auto-built from these)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=newproject
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-database-password

# Admin User Configuration
CREATE_ADMIN_ON_STARTUP=true
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=SecureAdminPassword123

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Email Provider Configuration
EMAIL_PROVIDER=aws_ses  # or "smtp"
SENDER_EMAIL=noreply@example.com

# AWS SES Configuration (if EMAIL_PROVIDER=aws_ses)
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_SES_REGION=eu-central-1

# SMTP Configuration (if EMAIL_PROVIDER=smtp)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=true
SMTP_USE_SSL=false

# OTP Configuration
OTP_LENGTH=6
OTP_EXPIRATION_MINUTES=10

# Email Verification Configuration
EMAIL_VERIFICATION_TOKEN_EXPIRATION_MINUTES=60
REQUIRE_EMAIL_VERIFICATION=true

# Password Reset Configuration
PASSWORD_RESET_TOKEN_EXPIRATION_MINUTES=60

# Two-Factor Authentication Configuration
FORCE_TWO_FACTOR_AUTH=false

# Site Configuration
BASE_URL=http://localhost:8000
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI): `http://localhost:8000/docs`

## Docker Deployment

### Development

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f app

# Stop services
docker compose down
```

### Production

```bash
# Build and start production containers
docker compose -f docker-compose.prod.yml up --build -d

# View logs
docker compose -f docker-compose.prod.yml logs -f app

# Stop services
docker compose -f docker-compose.prod.yml down
```

## API Endpoints

### Authentication

- `POST /v1/auth/register` - Register a new user
- `POST /v1/auth/login` - Login with email and password
- `POST /v1/auth/verify-email` - Verify email address with token
- `POST /v1/auth/forgot-password` - Request password reset
- `POST /v1/auth/reset-password` - Reset password with token

### Admin (Protected)

- `GET /v1/admin/users` - List all users (with pagination, search, filters)
- `GET /v1/admin/users/{id}` - Get user details
- `POST /v1/admin/users` - Create new user
- `PUT /v1/admin/users/{id}` - Update user
- `DELETE /v1/admin/users/{id}` - Delete user

## Configuration Options

### Email Verification

- `REQUIRE_EMAIL_VERIFICATION=true`: Enforces email verification before login
- `REQUIRE_EMAIL_VERIFICATION=false`: Email verification is optional (users still created with `is_email_verified=false`)

### Two-Factor Authentication

- `FORCE_TWO_FACTOR_AUTH=true`: 2FA is required for all users on every login
- `FORCE_TWO_FACTOR_AUTH=false`: 2FA is only required if `user.is_two_factor_enabled=true`

### Email Provider

Choose between AWS SES or SMTP:

- **AWS SES**: Set `EMAIL_PROVIDER=aws_ses` and configure AWS credentials
- **SMTP**: Set `EMAIL_PROVIDER=smtp` and configure SMTP settings (Gmail, custom SMTP, etc.)

## Database Migrations

### Create a new migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migration

```bash
alembic downgrade -1
```

## User Model

The User model includes:

- `id`: Primary key
- `email`: Unique email address
- `password_hash`: Hashed password
- `role`: User role (admin, editor, seo)
- `is_active`: Account status
- `full_name`: User's full name
- `phone_number`: Phone number
- `is_email_verified`: Email verification status
- `is_two_factor_enabled`: 2FA status
- `failed_login_attempts`: Failed login counter
- `last_failed_login`: Timestamp of last failed login
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

## Security Features

1. **Password Security**
   - Minimum 8 characters
   - Requires uppercase, lowercase, and digit
   - Bcrypt hashing

2. **Account Protection**
   - Account lockout after 3 failed login attempts
   - Rate limiting on authentication endpoints (5 requests/minute)

3. **Token Security**
   - Secure random token generation
   - Token expiration
   - One-time use tokens
   - Automatic cleanup of expired tokens

4. **Email Security**
   - Email enumeration prevention (same response for existing/non-existing emails)
   - Secure token-based verification

## Development

### Running Tests

```bash
# Add your test commands here
pytest
```

### Code Formatting

```bash
# Add formatting tools if needed
black .
isort .
```

## Production Deployment

1. Set all environment variables in `.env`
2. Use `docker-compose.prod.yml` for production
3. Configure proper CORS origins
4. Use strong JWT secret key
5. Enable HTTPS
6. Configure proper database backups
7. Set up monitoring and logging

## License

[Your License Here]

## Support

For issues and questions, please open an issue in the repository.
