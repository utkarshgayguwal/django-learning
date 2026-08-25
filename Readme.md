# Django Learning

This repository is my personal workspace for learning Django. It contains practice projects, apps, and notes as I work through Django concepts (models, views, templates, forms, admin, ORM, etc.) step by step.

## Commonly Used Commands (Ubuntu)

### Virtual Environment

Create a virtual environment:
```bash
python3 -m venv .venv
```
(`.venv` is the name of the virtual environment being created)

Activate the virtual environment:
```bash
source .venv/bin/activate
```

Deactivate the virtual environment:
```bash
deactivate
```

### Package Management (pip)

Install a package:
```bash
python3 -m pip install <package-name>
```

Install Django:
```bash
python3 -m pip install django
```

Save installed packages to a file:
```bash
python3 -m pip freeze > requirements.txt
```

Install packages from a requirements file:
```bash
python3 -m pip install -r requirements.txt
```

### Django Project & App Management

Create a new Django project:
```bash
django-admin startproject <project_name>
```

Create a new app inside a project:
```bash
python manage.py startapp <app_name>
```

Run the development server:
```bash
python manage.py runserver
```

Create migration files based on model changes:
```bash
python manage.py makemigrations
```

Apply migrations to the database:
```bash
python manage.py migrate
```

Create a superuser (for Django admin):
```bash
python manage.py createsuperuser
```

Open the Django interactive shell:
```bash
python manage.py shell
```
