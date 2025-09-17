### Hexlet tests and linter status:
[![Actions Status](https://github.com/oleg-dixon/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/oleg-dixon/python-project-52/actions)

# Task Manager
My [Task Manager](https://python-project-52-ya5h.onrender.com) this is a task management system. It allows you to set tasks, assign performers, and change their statuses. Registration and authentication are required to work with the system.

### Task management
Create, edit, and track task completion status.

### Labels and statuses
Organize tasks using labels and track their status.

### Teamwork
Assign tasks to other users and work together.

## Access
Application is deployed to [render.com](https://render.com/)
[Task Manager](https://python-project-52-ya5h.onrender.com/)

## Requirements
Python 3.12+

## Local Installation
### Clone repository
```bash
git clone https://github.com/oleg-dixon/python-project-52.git
cd python-project-52
make install # Install dependencies
make build # Buld package
```

### Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

### Install application
```bash
make install
```

### Put secrets to .env file
```
echo SECRET_KEY="{flask_secret_key}"
echo DATABASE_URL="postgresql://{user}:{password}@127.0.0.1:5432/sites"
```

### Perform migrations
```
make migrate
```

### Static Assembly
```
make collectstatic
```

### Start tests
```
make tests
```

### Start development application
```
make dev
```

### Database error
If errors occur after performing migrations and adding entities to the database, run:
```
make rmcache
```