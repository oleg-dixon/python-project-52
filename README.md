# Task Manager

[![Actions Status](https://github.com/oleg-dixon/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/oleg-dixon/python-project-52/actions) 
[![Python CI](https://github.com/oleg-dixon/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/oleg-dixon/python-project-52/actions/workflows/pyci.yml)

A comprehensive task management system built with Django that allows you to set tasks, assign performers, and track their statuses. Registration and authentication are required to work with the system.

🌐 **Live Demo**: [Task Manager on Render](https://python-project-52-ya5h.onrender.com)

## ✨ Features

- **Task Management** - Create, edit, and track task completion status
- **Labels & Statuses** - Organize tasks using labels and track their status
- **User Management** - Register, authenticate, and manage user profiles
- **Team Collaboration** - Assign tasks to other users and work together
- **Access Control** - Secure authentication and authorization system

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL
- UV package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/oleg-dixon/python-project-52.git
cd python-project-52
```

2. **Install UV (if not already installed)**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

3. **Install dependencies**
```bash
make install
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings:
# SECRET_KEY="your-secret-key"
# DATABASE_URL="postgresql://user:password@localhost:5432/task_manager"
```

5. **Setup database**
```bash
make migrate
make collectstatic
```

6. **Run the application**
```bash
make start
```

## 🛠️ Development

**Running Tests**
```bash
make test
```

**Code Quality**
```bash
make lint    # Run linters
make format  # Auto-format code
```

**Build Package**
```bash
make build
```

## 📦 Tech Stack

### Core
- Python 3.12+ - Programming language
- Django 5.2+ - Web framework

### Database
- PostgreSQL - Primary database
- Psycopg2-binary - PostgreSQL adapter
- Dj-database-url - Database URL parsing

### UI & Forms
- Django-bootstrap5 - Bootstrap 5 integration
- Django-filter - Filtering support

### Development
- Flake8 - Code linting
- Ruff - Fast Python linter
- Pytest - Testing framework
- Dotenv - Environment variables

### Production
- Gunicorn - WSGI server
- Rollbar - Error monitoring

## 🔧 Available Make Commands
- make install - Install dependencies
- make start - Run development server
- make test - Run test suite
- make lint - Run code linters
- make migrate - Run database migrations
- make collectstatic - Collect static files
- make build - Build package

## 🌐 Deployment
The application is deployed on [Render.com](https://render.com) and available at:

**Live Demo**: [https://python-project-52-ya5h.onrender.com](https://python-project-52-ya5h.onrender.com)

## 📝 License
This project is part of the Hexlet educational program.