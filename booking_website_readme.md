# Event Booking Website

A modern, full-stack event booking platform built with **Astro + Vue** frontend and **FastAPI** backend. Designed with modularity, abstraction, and maintainability in mind.

## 🏗️ Architecture Overview

```
📁 event-booking-platform/
├── 📁 frontend/                    # Astro + Vue Application
│   ├── 📁 src/
│   │   ├── 📁 components/          # Vue Components
│   │   ├── 📁 layouts/             # Astro Layouts
│   │   ├── 📁 pages/               # Astro Pages
│   │   ├── 📁 utils/               # Frontend Utilities
│   │   └── 📁 types/               # TypeScript Types
│   └── 📁 public/                  # Static Assets
├── 📁 backend/                     # FastAPI Application
│   ├── 📁 app/
│   │   ├── 📁 api/                 # API Routes
│   │   ├── 📁 core/                # Core Configuration
│   │   ├── 📁 models/              # Database Models
│   │   ├── 📁 schemas/             # Pydantic Schemas
│   │   ├── 📁 services/            # Business Logic
│   │   └── 📁 utils/               # Backend Utilities
│   └── 📁 tests/                   # Test Suite
└── 📁 shared/                      # Shared Types & Utilities
```

## 🚀 Features

### Frontend (Astro + Vue)
- **Homepage**: Hero section with service overview
- **Gallery**: Responsive image grid with lightbox
- **Pricing**: Service packages with clear pricing
- **Booking Form**: Comprehensive event inquiry system
- **Contact**: Business information and contact form
- **Responsive Design**: Mobile-first approach
- **TypeScript**: Full type safety
- **Tailwind CSS**: Utility-first styling

### Backend (FastAPI)
- **RESTful API**: Clean, documented endpoints
- **Form Processing**: Booking and contact form handling
- **Email Notifications**: Automated email system
- **Data Validation**: Pydantic models with validation
- **Database Integration**: SQLAlchemy with SQLite/PostgreSQL
- **Admin Interface**: Automatic API documentation
- **CORS Support**: Frontend integration ready
- **Error Handling**: Comprehensive error management

## 📋 Prerequisites

- **Node.js** (v18 or higher)
- **Python** (3.9 or higher)
- **Git**
- **VS Code** (recommended)

### Recommended VS Code Extensions
- Astro
- Vue Language Features (Volar)
- Python
- Python Docstring Generator
- Thunder Client (for API testing)
- Tailwind CSS IntelliSense

## 🛠️ Installation & Setup

### 1. Clone and Setup Project Structure

```bash
# Create project directory
mkdir event-booking-platform
cd event-booking-platform

# Initialize Git repository
git init
```

### 2. Frontend Setup (Astro + Vue)

```bash
# Create frontend directory
mkdir frontend
cd frontend

# Create Astro project with Vue integration
npm create astro@latest . -- --template minimal --typescript strict
npx astro add vue
npx astro add tailwind

# Install additional dependencies
npm install @astrojs/sitemap @astrojs/robots-txt
npm install lucide-vue-next
npm install @vueuse/core

# Development dependencies
npm install -D @types/node
```

### 3. Backend Setup (FastAPI)

```bash
# Navigate back to root and create backend
cd ..
mkdir backend
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install FastAPI and dependencies
pip install fastapi uvicorn[standard]
pip install sqlalchemy alembic
pip install python-multipart
pip install python-dotenv
pip install pydantic[email]
pip install aiosmtplib
pip install pytest pytest-asyncio httpx

# Create requirements.txt
pip freeze > requirements.txt
```

### 4. Environment Configuration

Create environment files for both frontend and backend:

#### Frontend Environment (`.env`)
```env
# API Configuration
PUBLIC_API_BASE_URL=http://localhost:8000
PUBLIC_SITE_URL=http://localhost:4321
PUBLIC_CONTACT_EMAIL=hello@example.com
```

#### Backend Environment (`.env`)
```env
# Database
DATABASE_URL=sqlite:///./booking.db
# For PostgreSQL: postgresql://user:password@localhost/booking_db

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=Event Booking

# Security
SECRET_KEY=your-super-secret-key-here
ALLOWED_ORIGINS=http://localhost:4321,http://localhost:3000

# Application
DEBUG=true
API_PREFIX=/api/v1
```

## 🏃‍♂️ Running the Application

### Development Mode

#### Terminal 1 - Backend (FastAPI)
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Frontend (Astro)
```bash
cd frontend
npm run dev
```

### Access Points
- **Frontend**: http://localhost:4321
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## 📁 Project Structure Details

### Frontend Architecture
```
frontend/src/
├── components/
│   ├── ui/                 # Reusable UI components
│   ├── forms/              # Form components
│   ├── gallery/            # Gallery components
│   └── navigation/         # Navigation components
├── layouts/
│   └── Layout.astro        # Main layout template
├── pages/
│   ├── index.astro         # Homepage
│   ├── gallery.astro       # Gallery page
│   ├── pricing.astro       # Pricing page
│   ├── contact.astro       # Contact page
│   └── booking.astro       # Booking page
├── utils/
│   ├── api.ts              # API client utilities
│   ├── validation.ts       # Form validation
│   └── constants.ts        # App constants
└── types/
    └── api.ts              # API type definitions
```

### Backend Architecture
```
backend/app/
├── api/
│   ├── routes/             # API route handlers
│   └── dependencies.py     # Dependency injection
├── core/
│   ├── config.py           # Application configuration
│   ├── database.py         # Database connection
│   └── security.py         # Security utilities
├── models/
│   ├── booking.py          # Booking database model
│   └── contact.py          # Contact database model
├── schemas/
│   ├── booking.py          # Booking Pydantic schemas
│   └── contact.py          # Contact Pydantic schemas
├── services/
│   ├── email_service.py    # Email handling
│   ├── booking_service.py  # Booking business logic
│   └── contact_service.py  # Contact business logic
└── utils/
    ├── logger.py           # Logging configuration
    ├── validators.py       # Custom validators
    └── exceptions.py       # Custom exceptions
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📦 Deployment

### Frontend (Vercel/Netlify)
```bash
cd frontend
npm run build
```

### Backend (Railway/Heroku/DigitalOcean)
```bash
cd backend
# Docker deployment
docker build -t booking-api .
docker run -p 8000:8000 booking-api
```

## 🐛 Debugging & Development

### Common Issues & Solutions

1. **CORS Errors**: Check `ALLOWED_ORIGINS` in backend `.env`
2. **Database Issues**: Run `alembic upgrade head` to apply migrations
3. **Email Not Sending**: Verify SMTP credentials and app passwords
4. **Import Errors**: Ensure virtual environment is activated

### Development Tools

- **API Testing**: Use Thunder Client extension or visit `/docs`
- **Database Inspection**: Use SQLite browser or pgAdmin
- **Logs**: Check console output in both terminals
- **Hot Reload**: Both frontend and backend support hot reloading

## 🔧 Customization

### Adding New Features
1. **New API Endpoint**: Add route in `backend/app/api/routes/`
2. **New Page**: Add `.astro` file in `frontend/src/pages/`
3. **New Component**: Add `.vue` file in `frontend/src/components/`
4. **Database Changes**: Create Alembic migration

### Styling
- Modify `tailwind.config.mjs` for custom themes
- Add global styles in `frontend/src/styles/global.css`
- Component-specific styles using Tailwind classes

## 📄 API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

### Key Endpoints
- `POST /api/v1/bookings` - Submit booking inquiry
- `POST /api/v1/contact` - Submit contact form
- `GET /api/v1/bookings` - Admin: List all bookings
- `GET /api/v1/health` - Health check

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section above
- Review API documentation at `/docs`
- Open an issue on GitHub

## 📝 License

This project is licensed under the MIT License.

---

**Built with ❤️ using Astro, Vue, FastAPI, and modern web technologies.**