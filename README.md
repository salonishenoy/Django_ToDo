# Django Todo API

A simple API for managing todo tasks built with Django.

## Features
- Create, read, update, and delete todo tasks
- Priority levels for tasks
- Task completion status

## Installation
1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver`

## API Endpoints
- GET /api/tasks/ - List all tasks
- POST /api/tasks/ - Create a new task
- GET /api/tasks/<id>/ - Retrieve a specific task
- PUT /api/tasks/<id>/ - Update a specific task
- DELETE /api/tasks/<id>/ - Delete a specific task
