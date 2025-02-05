# HR System

A comprehensive Human Resource Management System with Django Ninja backend and Next.js frontend.

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

## Project Snapshots

### Dashboard

[Coming Soon]

### Employee Management

[Coming Soon]

### Leave Management

[Coming Soon]

## Tech Stack

- Backend: Django 5.1.3 + Django Ninja 1.3.0
- Frontend: Next.js 14.2
- Database: PostgreSQL
- UI: TailwindCSS 3.4
- Authentication: Django Session + CSRF
- Runtime: Bun

## Prerequisites

- Python 3.11+
- Bun 1.0+
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

1. Navigate to frontend directory

```bash
cd frontend
```

2. Install frontend dependencies

```bash
bun install
```

3. Configure frontend environment

```bash
cp .env.example .env.local
# Required variables:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

4. Run development server

```bash
bun dev
```

The application will be available at:

- Backend API: http://localhost:8000
- Frontend: http://localhost:3000

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details.
