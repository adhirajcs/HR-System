# HR System

A comprehensive Human Resource Management System with Django Ninja backend (Frontend planned for future development).

## Features

- HR Management
  - HR Registration and Authentication
  - HR Profile Management
  
- Employee Management
  - Complete Employee CRUD Operations
  - Employee Profile Management
  - Employee Leave Tracking
  
- Project Manager Management
  - Project Manager CRUD Operations
  - Project Manager Profile Management
  
- Leave & Holiday Management
  - Holiday Calendar Management
  - Leave Request Management
  - Leave Status Tracking

## Planning & Roadmap

### ✅ Phase 1 - Backend Development (Completed)
- ✓ Django Ninja API infrastructure
- ✓ Core database models
- ✓ API endpoints implementation
- ✓ Authentication & Authorization
- ✓ API documentation
- ✓ Test coverage

### ⏳ Phase 2 - Frontend Development (Planned for Future)
- Next.js setup and configuration
- UI/UX design implementation
- Integration with backend APIs
- User interface for all core features
- Testing and optimization

## Current API Documentation
API documentation is available at: [API_documentation](API_documentation.txt)

## Tech Stack

### Current (Backend)
- Backend: Django 5.1.3 + Django Ninja 1.3.0
- Database: PostgreSQL
- Authentication: Django Session

### Planned (Frontend)
- Framework: Next.js 14.2
- UI: TailwindCSS 3.4, Shadcn-UI
- Runtime: Bun

## Prerequisites

- Python 3.11+
- PostgreSQL 14+

## Setup

### Backend Setup

1. Clone the repository

```bash
git clone https://github.com/adhirajcs/HR-System.git
cd hr-system/backend
```

2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install backend dependencies

```bash
pip install -r requirements.txt
```

4. Configure environment variables

```bash
cp .env.example .env
# Required variables:
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
# SECRET_KEY=your-secret-key
# DEBUG=True
```

5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Start the Django development server

```bash
python manage.py runserver
```

### Frontend Setup

> Note: Frontend setup instructions will be updated once frontend development begins.

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details.
