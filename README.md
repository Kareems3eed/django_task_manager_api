# Task Manager API (Django REST)

## Features
- JWT Authentication
- Task CRUD (Create, Read, Update, Delete)
- User-specific data isolation
- Validation & error handling
- Unit tests

## Tech Stack
- Django
- Django REST Framework
- SimpleJWT

## Setup

```bash
git clone <repo>
cd task-manager-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver