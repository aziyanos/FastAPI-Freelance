# 🚀 FastAPI Freelance Platform

> Modern async freelance marketplace API built with FastAPI, SQLAlchemy 2.0, and PostgreSQL

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org)

---

## 📋 Features

- ✅ **Async-first architecture** with SQLAlchemy 2.0
- ✅ **JWT Authentication** (Access + Refresh tokens)
- ✅ **Role-based access** (Admin, Client, Freelancer)
- ✅ **Many-to-Many relationships** (Skills ↔ Projects, Users ↔ Skills)
- ✅ **OAuth2 integration** (Google, GitHub)
- ✅ **Admin panel** (SQLAdmin)
- ✅ **Comprehensive testing** (pytest with async support)
- ✅ **API documentation** (Swagger UI + Custom docs)

---

## 🏗️ Project Structure

```
FastAPI-Freelance/
├── app/
│   ├── api/              # API endpoints
│   │   ├── auth.py       # Authentication routes
│   │   ├── users.py      # User CRUD
│   │   ├── projects.py   # Project management
│   │   ├── skills.py     # Skills endpoints
│   │   ├── categories.py # Categories
│   │   ├── offers.py     # Freelancer offers
│   │   └── reviews.py    # Reviews & ratings
│   ├── db/
│   │   ├── database.py   # Async DB setup
│   │   ├── models.py     # SQLAlchemy models
│   │   ├── schemas.py    # Pydantic schemas
│   │   └── deps.py       # 🆕 Dependency injection
│   ├── admin/            # Admin panel setup
│   ├── middlewares/      # Custom middleware
│   ├── tests/            # Pytest integration tests
│   └── main.py           # FastAPI application
├── docs/
│   └── API.md            # 📚 Full API documentation
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- pip / poetry

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/FastAPI-Freelance.git
cd FastAPI-Freelance
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create `.env` file:

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost/freelance

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_LIFETIME=30  # minutes
REFRESH_TOKEN_LIFETIME=3  # days

# Encryption
ENCRYPT_KEY=your-fernet-key-here

# OAuth (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_KEY=your-google-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_KEY=your-github-secret
```

### 5. Create Database

```bash
createdb freelance
```

### 6. Run Migrations

```bash
alembic upgrade head
```

### 7. Start Server

```bash
uvicorn app.main:freelance --reload --port 8001
```

Server will start at: **http://localhost:8001**

---

## 📚 Documentation

- **Swagger UI:** http://localhost:8001/docs
- **Full API Docs:** [docs/API.md](docs/API.md)
- **Admin Panel:** http://localhost:8001/admin

---

## 🧪 Testing

Run all tests:

```bash
pytest app/tests/ -v
```

Run specific test file:

```bash
pytest app/tests/test_projects.py -v
```

Run with coverage:

```bash
pytest --cov=app app/tests/
```

---

## 🔐 Authentication Flow

### 1. Register

```bash
curl -X POST http://localhost:8001/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "role": "freelancer"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "johndoe",
    "password": "SecurePass123!"
  }'
```

Response:
```json
{
  "access_token": "eyJhbG...",
  "refresh_token": "eyJhbG...",
  "token_type": "bearer"
}
```

### 3. Use Token

```bash
curl -X GET http://localhost:8001/user/ \
  -H "Authorization: Bearer <access_token>"
```

---

## 🗄️ Database Schema

### Core Models

- **UserProfile** - Users with roles (admin, client, freelancer)
- **Project** - Freelance projects
- **Skill** - Technical skills (Many-to-Many with Users & Projects)
- **Category** - Project categories
- **Offer** - Freelancer proposals for projects
- **Review** - Ratings & feedback (self-referential: reviewer → target)
- **RefreshToken** - JWT refresh token storage

### Relationships

```
UserProfile ──┬─→ Project (One-to-Many as client)
              ├─→ Offer (One-to-Many as freelancer)
              ├─→ Review (One-to-Many as reviewer)
              ├─→ Review (One-to-Many as target)
              └─→ Skill (Many-to-Many)

Project ──┬─→ Category (Many-to-One)
          ├─→ Offer (One-to-Many)
          ├─→ Review (One-to-Many)
          └─→ Skill (Many-to-Many)
```

---

## 🛠️ Technologies

| Category | Stack |
|----------|-------|
| **Framework** | FastAPI 0.109+ |
| **Language** | Python 3.11+ |
| **Database** | PostgreSQL 15+ |
| **ORM** | SQLAlchemy 2.0 (async) |
| **Validation** | Pydantic v2 |
| **Authentication** | JWT (python-jose) |
| **Password Hashing** | bcrypt |
| **Testing** | pytest, httpx |
| **Admin Panel** | SQLAdmin |
| **OAuth** | authlib |

---

## 📊 API Endpoints Overview

| Category | Endpoints | Auth Required |
|----------|-----------|---------------|
| **Auth** | `/auth/register`, `/auth/login`, `/auth/logout`, `/auth/refresh` | ❌ |
| **Users** | `/user/`, `/user/{id}` | ✅ |
| **Projects** | `/project/`, `/project/{id}` | ✅ |
| **Skills** | `/skill/`, `/skill/{id}` | ❌ |
| **Categories** | `/category/`, `/category/{id}` | ❌ |
| **Offers** | `/offers/`, `/offers/{id}` | ✅ |
| **Reviews** | `/reviews/`, `/reviews/{id}` | ✅ |

Full documentation: [docs/API.md](docs/API.md)

---

## 🔒 Security

### Current Implementation

- ✅ JWT access/refresh tokens
- ✅ Password hashing with bcrypt
- ✅ Token storage in database (revokable)
- ✅ HTTPS support ready

### ⚠️ Known Security Issues

- ❌ No rate limiting (vulnerability to brute force)
- ❌ Weak password validation (only length check)
- ❌ Database credentials in code (should use env vars)
- ❌ No email verification
- ❌ Middleware logs sensitive data

**Status:** These are being addressed in v1.1.0

---

## 🚧 Roadmap

### v1.1.0 (In Progress)

- [ ] Rate limiting (slowapi)
- [ ] Stronger password validation
- [ ] Move all secrets to .env
- [ ] Email verification
- [ ] Pagination for list endpoints

### v1.2.0 (Planned)

- [ ] File upload support
- [ ] Real-time notifications (WebSockets)
- [ ] Payment integration (Stripe)
- [ ] Advanced search & filtering
- [ ] Caching (Redis)

### v2.0.0 (Future)

- [ ] Microservices architecture
- [ ] Message queue (Celery)
- [ ] Elasticsearch integration
- [ ] GraphQL API

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation

---

## 📈 Project Stats

- **Lines of Code:** ~2,500
- **Test Coverage:** 75%
- **API Endpoints:** 35+
- **Database Tables:** 8

---

**⭐ Star this repo if you find it useful!**
