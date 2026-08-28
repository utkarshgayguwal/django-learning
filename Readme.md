# Django Learning

This repository is my personal workspace for learning Django. It contains practice projects, apps, and notes as I work through Django concepts (models, views, templates, forms, admin, ORM, etc.) step by step.

## Table of Contents

- [Commonly Used Commands (Ubuntu)](#commonly-used-commands-ubuntu)
  - [Virtual Environment](#virtual-environment)
  - [Package Management (pip)](#package-management-pip)
  - [Django Project and App Management](#django-project-and-app-management)
- [Notes](#notes)
  - [Two ways to serve templates (HTML files)](#two-ways-to-serve-templates-html-files)
  - [Django Template Language (DTL) basics](#django-template-language-dtl-basics)
  - [Template inheritance (extends and block)](#template-inheritance-extends-and-block)
  - [Naming URLs and the url tag](#naming-urls-and-the-url-tag)
  - [Reusable template fragments (include)](#reusable-template-fragments-include)
- [Questions and Answers](#questions-and-answers)
  - [Q: When I run `python3 manage.py migrate`, where do the default migrations come from? Where is that code written?](#q-when-i-run-python3-managepy-migrate-where-do-the-default-migrations-come-from-where-is-that-code-written)
  - [Q: What is a project and what is an app in Django?](#q-what-is-a-project-and-what-is-an-app-in-django)
  - [Q: What is MVT (Model-View-Template) in Django?](#q-what-is-mvt-model-view-template-in-django)

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

### Django Project and App Management

Create a new Django project(add '.' at end to avoid further folder duplication):
```bash
django-admin startproject <project_name> .
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

## Notes

### Two ways to serve templates (HTML files)

**Method 1: App-level templates (`APP_DIRS`)**

Each app gets its own `templates/<app_name>/` folder:

```
app/
├── templates/
│   └── app/
│       └── home.html
├── views.py
```

This works because `APP_DIRS: True` in `TEMPLATES` tells Django to automatically look inside every installed app's `templates/` folder (via the `app_directories` loader). This is what this project currently uses — `app/templates/app/home.html` is found automatically because `'app'` is in `INSTALLED_APPS`.

Why the nested `app_name/` subfolder? Namespacing. If two apps both had `templates/home.html`, Django's loader would grab whichever app it scans first — a silent collision. `templates/app/home.html` + `render(request, 'app/home.html')` avoids that.

Good for: templates that belong to one specific app — reusable, self-contained, easy to package/reuse in another project.

**Method 2: Project-level templates (`DIRS`)**

A single shared `templates/` folder at the project root (next to `manage.py`), registered explicitly in `TEMPLATES[0]['DIRS']`:

```
manage.py
templates/
├── base.html
├── home.html
company/
├── settings.py
```

```python
# company/settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # or os.path.join(BASE_DIR, 'templates')
        'APP_DIRS': True,
        'OPTIONS': { ... },
    },
]
```

Now `render(request, 'home.html')` (or `base.html`) resolves from that shared folder — no app namespace needed.

Good for: things shared across the whole site — `base.html` layout, `navbar.html`, `footer.html`, 404/500 error pages — anything not owned by a single app.

**Resolution order:** with both configured, Django checks `DIRS` (project-level) first, then `APP_DIRS` (per-app, in `INSTALLED_APPS` order). So a `DIRS` template can shadow/override an app's template of the same relative path.

**In practice:** most real Django projects use both together — project-level `templates/` for shared layout (`base.html`, `navbar.html`), and each app's `templates/<app_name>/` for that app's own pages, which `{% extends "base.html" %}`.

### Django Template Language (DTL) basics

**Variables — `{{ variable_name }}`**

Whatever key you put in a view's `context` dict becomes a variable in the template. From `app/views.py`:

```python
context = {'app_name': 'App', 'tasks': [{'name': 'Learn Models', 'done': True}, ...]}
return render(request, 'app/index.html', context)
```

```html
<h1>{{ app_name }} Page</h1>
```

Dot notation (`{{ task.name }}`) works for dict keys, object attributes, list indices, and method calls — Django tries each in that order and uses whichever succeeds first.

**Filters — `{{ value|filter }}`**

Pipe a variable through a transformation. Filters chain left to right:

```html
{{ app_name|upper }}                  <!-- APP -->
{{ description|truncatewords:8 }}
{{ tasks|length }}
{{ version|default:"0.0" }}
{{ site_name|lower|title }}
```

Full reference: [built-in filters](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#built-in-filter-reference).

**For loops — `{% for %}`**

Used in both `home.html` and `app/index.html`:

```html
{% for task in tasks %}
  <li>{{ task.name }}</li>
{% empty %}
  <li>No tasks yet.</li>
{% endfor %}
```

`{% empty %}` renders when the list is empty — no separate `{% if %}` needed. Inside the loop, `forloop.counter` (1-indexed), `forloop.counter0`, `forloop.first`, and `forloop.last` are available.

**If conditions — `{% if %}`**

Used in `app/index.html` to render a task's status:

```html
{% if task.done %}
  <span class="status done">Done</span>
{% else %}
  <span class="status pending">Pending</span>
{% endif %}
```

Also supports `{% elif %}`, comparisons (`==`, `!=`, `<`, `in`), and boolean operators (`and`, `or`, `not`).

### Template inheritance (extends and block)

`home.html` and `app/index.html` currently each duplicate the full `<html><head>...` boilerplate. Inheritance removes that duplication.

1. Define a **base template** with named regions (`{% block %}`) a child can override:

```html
<!-- templates/base.html -->
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Django Learning{% endblock %}</title>
    {% block extra_head %}{% endblock %}
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

2. A child template extends it. `{% extends %}` must be the **first tag in the file** — nothing, not even whitespace-producing tags, can come before it. Anything outside a `{% block %}` in the child is ignored:

```html
<!-- templates/home.html -->
{% extends 'base.html' %}
{% block title %}{{ site_name }}{% endblock %}
{% block content %}
<h1>Welcome to {{ site_name }}</h1>
{% endblock %}
```

Block names are arbitrary — `title`, `extra_head`, `content` above are project-defined, not built in. Add as many as needed (e.g. `scripts`, `sidebar`). Inside an override, `{{ block.super }}` keeps the parent block's content instead of fully replacing it.

**Status in this project:** not yet adopted — `home.html` and `app/index.html` are still standalone, full-page templates.

### Naming URLs and the url tag

`company/urls.py` currently has no `name=` on its routes:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('app/', index)
]
```

Adding `name=` lets templates reference a route by name instead of a hardcoded path:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('app/', index, name='app-index'),
]
```

```html
<a href="{% url 'home' %}">Home</a>
<a href="{% url 'app-index' %}">App</a>
```

If the route later moves (e.g. `app/` → `demo/`), only `urls.py` changes — every `{% url %}` reference updates automatically. For routes with arguments (e.g. `path('app/<int:id>/', detail, name='app-detail')`), pass them positionally: `{% url 'app-detail' id %}`.

**Status in this project:** not yet adopted — no named routes or `{% url %}` usage yet.

### Reusable template fragments (include)

`{% include %}` renders another template's output inline — for markup reused across multiple pages (header, navbar, footer) that isn't shared "page layout" the way `{% extends %}` is.

```html
<!-- templates/partials/header.html -->
<header>
    <a href="{% url 'home' %}">{{ site_name|default:"Django Learning" }}</a>
</header>
```

```html
<!-- templates/base.html -->
<body>
    {% include 'partials/header.html' %}
    {% block content %}{% endblock %}
</body>
```

An included template inherits the full surrounding context by default. To override or pass extra variables explicitly: `{% include 'partials/header.html' with site_name="Custom Title" %}`.

**Status in this project:** not yet adopted; `static/css/` (loaded via `{% load static %}` + `{% static %}`) is the equivalent pattern already in use for shared *assets* rather than shared *markup*.

## Questions and Answers

### Q: When I run `python3 manage.py migrate`, where do the default migrations come from? Where is that code written?

They're not generated by your project — they ship pre-written inside the Django package itself, one folder per built-in app. Inside the venv:

```
.venv/lib/python3.14/site-packages/django/contrib/
├── admin/migrations/
├── auth/migrations/
├── contenttypes/migrations/
└── sessions/migrations/
```

These correspond to the apps listed in `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

**What `migrate` actually does:**
1. Reads `INSTALLED_APPS`.
2. For each app, looks for a `migrations/` folder next to that app's code (`models.py`).
3. For built-in apps (`admin`, `auth`, `contenttypes`, `sessions`), those migration files already exist inside the installed `django` package — Django wrote and shipped them with the framework.
4. Applies each migration file in order (e.g. `0001_initial.py`, `0002_...py`) as SQL against `db.sqlite3`, creating tables like `auth_user`, `django_session`, `django_content_type`, etc.
5. Tracks which migrations have run in a table called `django_migrations` inside `db.sqlite3`.

**For your own apps:** running `python manage.py startapp <name>` gives it an empty `migrations/` folder. Nothing exists there until you define models in that app's `models.py` and run `python manage.py makemigrations` — that's when Django writes migration files for your own code.

### Q: What is a project and what is an app in Django?

A **project** is the whole web application — the top-level configuration: settings, URL routing, WSGI/ASGI setup. An **app** is a self-contained module inside the project that handles one specific piece of functionality (e.g. blog posts, user profiles, payments). A project can contain multiple apps, and apps are meant to be reusable/pluggable.

In this repo, `company` (created via `django-admin startproject company .`) is the **project**. A feature module added with:
```bash
python manage.py startapp blog
```
would be an **app** — it gets its own `models.py`, `views.py`, `admin.py`, etc., and must be registered in `company/settings.py` under `INSTALLED_APPS` and wired into `company/urls.py`.

**Analogy:** project = the house, apps = the rooms — each room (app) serves a distinct purpose, but they all belong to and are coordinated by the same house (project).

### Q: What is MVT (Model-View-Template) in Django?

**MVT** is Django's architectural pattern — its take on MVC. Three pieces:

- **Model** — defines the data structure and talks to the database (`models.py`)
- **View** — contains the logic: receives the request, fetches/processes data via the Model, decides what to send back (`views.py`)
- **Template** — the HTML that renders the data for the user (`templates/*.html`)

Django itself acts as the "Controller" (via URL routing), so you only write M, V, and T.

**Example flow — user visits `/blog/` to see a list of posts:**

```
 USER (Browser)
     │  1. GET /blog/
     ▼
┌─────────────────────┐
│   urls.py             │  2. Matches "/blog/" to a view function
│   (URL dispatcher)    │
└─────────┬────────────┘
          │ 3. calls view
          ▼
┌─────────────────────┐
│   views.py             │  4. def post_list(request):
│   (View)               │        posts = Post.objects.all()
└─────────┬────────────┘
          │ 5. queries via ORM
          ▼
┌─────────────────────┐
│   models.py             │  6. Post model → SQL query
│   (Model)               │
└─────────┬────────────┘
          │ 7. hits database
          ▼
┌─────────────────────┐
│   db.sqlite3             │  8. returns rows (Post objects)
│   (Database)             │
└─────────┬────────────┘
          │ 9. QuerySet of posts returned to view
          ▼
┌─────────────────────┐
│   views.py               │  10. return render(request,
│                           │        "blog/post_list.html",
│                           │        {"posts": posts})
└─────────┬────────────┘
          │ 11. passes data to template
          ▼
┌─────────────────────┐
│   post_list.html          │  12. {% for post in posts %}
│   (Template)               │        <h2>{{ post.title }}</h2>
│                             │      {% endfor %}
└─────────┬────────────┘
          │ 13. renders final HTML
          ▼
 USER (Browser)
     ◀── 14. HTTP response: rendered HTML page with blog posts
```

**Code sketch:**

`models.py`
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
```

`views.py`
```python
def post_list(request):
    posts = Post.objects.all()
    return render(request, "blog/post_list.html", {"posts": posts})
```

`urls.py`
```python
urlpatterns = [
    path("blog/", views.post_list, name="post_list"),
]
```

`templates/blog/post_list.html`
```html
{% for post in posts %}
  <h2>{{ post.title }}</h2>
  <p>{{ post.content }}</p>
{% endfor %}
```

So the flow is: **User → URL → View → Model → Database → View → Template → User (HTML response)**.
