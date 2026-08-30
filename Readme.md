# Django Learning

This repository is my personal workspace for learning Django. It contains practice projects, apps, and notes as I work through Django concepts (models, views, templates, forms, admin, ORM, etc.) step by step.

## Table of Contents

- [Commonly Used Commands (Ubuntu)](#commonly-used-commands-ubuntu)
  - [Virtual Environment](#virtual-environment)
  - [Package Management (pip)](#package-management-pip)
  - [Django Project and App Management](#django-project-and-app-management)
- [Notes](#notes)
  - [MVT (Model-View-Template)](#mvt-model-view-template)
  - [Two ways to serve templates (HTML files)](#two-ways-to-serve-templates-html-files)
  - [Django Template Language (DTL) basics](#django-template-language-dtl-basics)
  - [Template inheritance (extends and block)](#template-inheritance-extends-and-block)
  - [Naming URLs and the url tag](#naming-urls-and-the-url-tag)
  - [Reusable template fragments (include)](#reusable-template-fragments-include)
  - [ModelAdmin attributes and methods](#modeladmin-attributes-and-methods)
  - [Commonly used ORM methods](#commonly-used-orm-methods)
  - [Foreign keys and relationships (ForeignKey, OneToOne, ManyToMany)](#foreign-keys-and-relationships-foreignkey-onetoone-manytomany)
  - [Pagination (Paginator and Page)](#pagination-paginator-and-page)
- [Questions and Answers](#questions-and-answers)
  - [Q: When I run `python3 manage.py migrate`, where do the default migrations come from? Where is that code written?](#q-when-i-run-python3-managepy-migrate-where-do-the-default-migrations-come-from-where-is-that-code-written)
  - [Q: What is a project and what is an app in Django?](#q-what-is-a-project-and-what-is-an-app-in-django)
  - [Q: Why does `Model.objects.get(some_id)` fail, while `Model.objects.get(pk=some_id)` works — aren't both just passing an integer?](#q-why-does-modelobjectsgetsome_id-fail-while-modelobjectsgetpksome_id-works--arent-both-just-passing-an-integer)

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

Collect all static files into `STATIC_ROOT` (needed for deployment, e.g. when serving via WhiteNoise):
```bash
python3 manage.py collectstatic
```

## Notes

### MVT (Model-View-Template)

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

### ModelAdmin attributes and methods

Common `admin.ModelAdmin` options, beyond what `GeneralInfoAdmin` (`app/admin.py`) already uses — `list_display`, `readonly_fields`, `has_add_permission`, `has_change_permission`, `has_delete_permission`.

**Display — control the list page**

**`list_display`** — columns shown in the admin list view; entries can be field names or method names. Used in `GeneralInfoAdmin`:
```python
list_display = ['company_name', 'location', 'email']
```

**`list_display_links`** — which of those columns link through to the edit page (defaults to the first column).
```python
list_display_links = ['company_name']
```

**`list_filter`** — adds a sidebar filter panel for the given fields.
```python
list_filter = ['location']
```

**`search_fields`** — enables a search box over the given fields.
```python
search_fields = ['company_name', 'email']
```

**`ordering`** — default sort order for the list view; a leading `-` means descending.
```python
ordering = ['-id']
```

**`list_per_page`** — how many rows are shown per page (default 100).
```python
list_per_page = 25
```

**`list_editable`** — fields editable directly inline in the list view, without opening the record.
```python
list_editable = ['location']
```

**`date_hierarchy`** — adds a date drill-down navigation bar; needs a `DateField`/`DateTimeField` on the model.
```python
date_hierarchy = 'created_at'
```

**Editing — control the add/change form**

**`fields`** — which fields appear on the form, and in what order.
```python
fields = ['company_name', 'location', 'email']
```

**`exclude`** — fields to hide from the form entirely.
```python
exclude = ['internal_notes']
```

**`readonly_fields`** — fields shown on the form but not editable. Used in `GeneralInfoAdmin`:
```python
readonly_fields = ['email']
```

**`fieldsets`** — groups fields into labeled sections on the form.
```python
fieldsets = (
    ('Company', {'fields': ('company_name', 'location')}),
    ('Contact', {'fields': ('email',)}),
)
```

**`prepopulated_fields`** — auto-fills a field (commonly a slug) from another field as you type.
```python
prepopulated_fields = {'slug': ('company_name',)}
```

**`autocomplete_fields`** — replaces a slow dropdown (e.g. a large foreign key) with a search-as-you-type widget.
```python
autocomplete_fields = ['owner']
```

**`raw_id_fields`** — replaces a foreign key/many-to-many dropdown with a plain ID input plus a lookup popup, useful when the related table is huge.
```python
raw_id_fields = ['owner']
```

**`inlines`** — lets you edit related (foreign-key child) records on the same page as the parent.
```python
class TaskInline(admin.TabularInline):
    model = Task

class ProjectAdmin(admin.ModelAdmin):
    inlines = [TaskInline]
```

**Permissions — control which actions are allowed**

Each returns a boolean. `GeneralInfoAdmin` uses the first three (all returning `False`) to fully lock the model down — no add, no edit, no delete — since it holds a single, pre-seeded row of site-wide info:

**`has_add_permission(self, request)`**
```python
def has_add_permission(self, request):
    return False
```

**`has_change_permission(self, request, obj=None)`**
```python
def has_change_permission(self, request, obj=None):
    return False
```

**`has_delete_permission(self, request, obj=None)`**
```python
def has_delete_permission(self, request, obj=None):
    return False
```

**`has_view_permission(self, request, obj=None)`** — controls whether the record can even be viewed, separate from editing it.
```python
def has_view_permission(self, request, obj=None):
    return request.user.is_superuser
```

**`has_module_permission(self, request)`** — whether this model's section shows up in the admin index page at all.
```python
def has_module_permission(self, request):
    return request.user.is_staff
```

**Actions — bulk operations**

**`actions`** — list of custom bulk-action functions available in the list view's "Action" dropdown.
```python
def mark_verified(modeladmin, request, queryset):
    queryset.update(verified=True)

actions = [mark_verified]
```

**`actions_on_top` / `actions_on_bottom`** — where the actions dropdown is shown on the list page.
```python
actions_on_top = True
actions_on_bottom = False
```

**Hooks — customize behavior in code**

**`save_model(self, request, obj, form, change)`** — runs on save; a hook to set fields automatically (e.g. stamping who created a record).
```python
def save_model(self, request, obj, form, change):
    if not change:
        obj.created_by = request.user
    super().save_model(request, obj, form, change)
```

**`get_queryset(self, request)`** — customize/filter which rows a given admin user sees at all.
```python
def get_queryset(self, request):
    qs = super().get_queryset(request)
    return qs if request.user.is_superuser else qs.filter(owner=request.user)
```

**`get_readonly_fields(self, request, obj=None)`** — same idea as `readonly_fields`, but computed dynamically per request/object.
```python
def get_readonly_fields(self, request, obj=None):
    return ['email'] if obj else []
```

**`formfield_for_foreignkey(self, db_field, request, **kwargs)`** — customize how a specific foreign key field's widget/queryset behaves.
```python
def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == 'owner':
        kwargs['queryset'] = User.objects.filter(is_staff=True)
    return super().formfield_for_foreignkey(db_field, request, **kwargs)
```

Full reference: [Django `ModelAdmin` options](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#modeladmin-options).

### Commonly used ORM methods

The most-used `QuerySet`/`Manager` methods, grouped by purpose. Examples use a simple two-model set (this project's own `GeneralInfo` model, `app/models.py`, has no relations, so a relational example is used here instead):

```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    published = models.DateField()
    in_stock = models.BooleanField(default=True)
```

**Retrieving objects**

**`all()`** — returns a QuerySet of every row.
```python
Book.objects.all()
```

**`get()`** — returns exactly one object; raises `DoesNotExist` if none, `MultipleObjectsReturned` if more than one. Use for lookups by a unique field (like `pk`).
```python
Book.objects.get(pk=1)
```

**`filter()`** — returns a QuerySet matching the given conditions (can be empty).
```python
Book.objects.filter(in_stock=True)
```

**`exclude()`** — opposite of `filter()`; returns everything that does *not* match.
```python
Book.objects.exclude(in_stock=True)
```

**`first()` / `last()`** — returns the first/last object or `None`, no exception raised.
```python
Book.objects.filter(author__name="Utkarsh").first()
```

**Field lookups** (used inside `filter()`/`exclude()`)

Django uses `field__lookuptype=value` syntax:
```python
Book.objects.filter(price__gt=500)              # greater than
Book.objects.filter(price__gte=500)             # greater than or equal
Book.objects.filter(price__lt=500)
Book.objects.filter(price__lte=500)
Book.objects.filter(title__icontains="django")  # case-insensitive contains
Book.objects.filter(title__startswith="The")
Book.objects.filter(published__year=2024)
Book.objects.filter(author__name__exact="Utkarsh")  # traverse relations with __
Book.objects.filter(id__in=[1, 2, 3])
Book.objects.filter(published__isnull=True)
```

**Ordering, limiting, uniqueness**

**`order_by()`** — sort results (`-` prefix = descending).
```python
Book.objects.order_by("-published", "title")
```

**Slicing** — acts like Python list slicing → `LIMIT`/`OFFSET` in SQL.
```python
Book.objects.all()[:5]    # first 5
Book.objects.all()[5:10]  # next 5
```

**`distinct()`** — removes duplicate rows (common after joins).
```python
Book.objects.filter(author__name="Utkarsh").distinct()
```

**`values()` / `values_list()`** — return dicts/tuples instead of model instances; useful for lighter queries.
```python
Book.objects.values("title", "price")          # [{'title': ..., 'price': ...}, ...]
Book.objects.values_list("title", flat=True)   # ['Book 1', 'Book 2', ...]
```

**Creating, updating, deleting**

**`create()`** — build and save in one step.
```python
Book.objects.create(title="Deep ORM", author=a1, price=499, published="2026-01-01")
```

**`save()`** — persists changes on an instance (insert or update).
```python
book = Book.objects.get(pk=1)
book.price = 599
book.save()
```

**`bulk_create()`** — insert many rows in a single query (faster than looping `.save()`).
```python
Book.objects.bulk_create([Book(title="A", ...), Book(title="B", ...)])
```

**`update()`** — updates matching rows directly in the DB without loading instances (no `save()`/signals triggered per row).
```python
Book.objects.filter(in_stock=False).update(price=0)
```

**`delete()`** — deletes matching objects.
```python
Book.objects.filter(in_stock=False).delete()
```

**`get_or_create()`** — fetch if it exists, otherwise create it. Returns `(object, created_bool)`.
```python
author, created = Author.objects.get_or_create(name="Utkarsh")
```

**`update_or_create()`** — like `get_or_create()`, but also updates fields if the object already exists.
```python
Book.objects.update_or_create(title="Deep ORM", defaults={"price": 599})
```

**Aggregation & annotation**

**`aggregate()`** — computes a single summary value across the whole QuerySet (returns a dict).
```python
from django.db.models import Avg
Book.objects.aggregate(Avg("price"))  # {'price__avg': 432.5}
```

**`annotate()`** — adds a computed value to *each* object in the QuerySet (group-by style queries).
```python
from django.db.models import Count
for author in Author.objects.annotate(book_count=Count("book")):
    print(author.name, author.book_count)
```

**`count()`** — number of rows matched; runs `COUNT()` in SQL without loading objects (more efficient than `len(qs)`).
```python
Book.objects.filter(in_stock=True).count()
```

**`exists()`** — returns `True`/`False`; more efficient than `.count() > 0` for a simple existence check.
```python
Book.objects.filter(author=a1).exists()
```

**Complex lookups**

**`Q()` objects** — for OR conditions or complex combinations (`filter()` alone only ANDs).
```python
from django.db.models import Q
Book.objects.filter(Q(price__lt=100) | Q(in_stock=False))
Book.objects.filter(Q(title__icontains="orm") & ~Q(in_stock=True))
```

**`F()` objects** — reference another field's value in a query (compare fields, or do arithmetic at the DB level without pulling data into Python).
```python
from django.db.models import F
Book.objects.filter(price__gt=F("author__id"))
Book.objects.update(price=F("price") * 1.1)  # 10% price hike, done in the DB
```

**Relations (FK / reverse FK)**

```python
book.author             # forward FK access
author.book_set.all()   # reverse FK access (default related manager)
```

**`select_related()`** — for FK/OneToOne; does a SQL JOIN to fetch related objects in the same query (avoids N+1 queries).
```python
Book.objects.select_related("author").all()
```

**`prefetch_related()`** — for ManyToMany/reverse-FK; runs a separate query and joins in Python (also avoids N+1).
```python
Author.objects.prefetch_related("book_set").all()
```

**Mental model:** `filter`/`exclude`/`order_by`/`values` return **QuerySets** — lazy and chainable, not hitting the DB until evaluated. `get`/`first`/`create`/`count`/`exists`/`aggregate` hit the DB **immediately** and return a concrete result. Chains collapse into a single SQL query, e.g. `Book.objects.filter(in_stock=True).exclude(price__lt=100).order_by("-price")[:5]`.

Full reference: [Django QuerySet API](https://docs.djangoproject.com/en/stable/ref/models/querysets/).

### Foreign keys and relationships (ForeignKey, OneToOne, ManyToMany)

Django gives three field types for linking models: `ForeignKey`, `OneToOneField`, and `ManyToManyField`.

**1. Foreign Key (One-to-Many)**

A foreign key is a column on the "child" table storing the primary key of a row on the "parent" table — **one parent row can be referenced by many child rows.**

This project's `app/models.py` has an `Author` model and a `Blog` model with a commented-out `author` field:

```python
class Blog(models.Model):
    ...
    # author = models.CharField(max_length=255)
```

That stored the author as plain text with no real link to the `Author` table. The correct fix is a `ForeignKey`:

```python
class Blog(models.Model):
    ...
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='blogs'
    )
```

- **One `Author` → many `Blog` posts.** Each `Blog` row stores an `author_id` column.
- `on_delete` is required — what happens to `Blog` rows if their `Author` is deleted:
  - `CASCADE` — delete the blogs too.
  - `PROTECT` — block deletion of the author if they have blogs.
  - `SET_NULL` — set `author` to `NULL` (requires `null=True` on the field).
  - `SET_DEFAULT` — fall back to a default author.
- `related_name='blogs'` enables backward access: `some_author.blogs.all()`. Without it, Django defaults to `blog_set`.
- Forward access is a plain attribute: `some_blog.author` returns the `Author` instance (not just an ID).

**2. One-to-One**

A `OneToOneField` is a foreign key with a `UNIQUE` constraint added — **each parent row links to at most one child row**, and vice versa.

Classic use case: splitting off optional/rarely-used data into a second table, e.g. an `AuthorProfile`:

```python
class AuthorProfile(models.Model):
    author = models.OneToOneField(
        Author,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField()
    avatar = models.CharField(max_length=255)
```

- Each `Author` has exactly one `AuthorProfile` (or none).
- Forward: `profile.author`. Backward: `some_author.profile` (singular — not `.profile_set`, since it's guaranteed unique).

**3. Many-to-Many**

A `ManyToManyField` lets **many rows on each side relate to many rows on the other side**. Django creates a hidden junction table with two foreign keys — neither model itself gets an FK column.

```python
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Blog(models.Model):
    ...
    tags = models.ManyToManyField(Tag, related_name='blogs', blank=True)
```

- No `on_delete` argument — deleting a `Tag` only removes the junction-table rows linking it, not the `Blog`s.
- Access: `some_blog.tags.all()` and `some_tag.blogs.all()`.
- Modify with `.add()`, `.remove()`, `.set()`: `some_blog.tags.add(tag1, tag2)`.
- Need extra data on the relationship itself (e.g. "date tagged")? Use a `through` model instead of a plain `ManyToManyField`.

**Quick comparison**

| Relationship | Field | DB implementation | Example |
|---|---|---|---|
| One-to-Many | `ForeignKey` | FK column on the "many" side | `Author` → many `Blog`s |
| One-to-One | `OneToOneField` | FK column with `UNIQUE` constraint | `Author` ↔ `AuthorProfile` |
| Many-to-Many | `ManyToManyField` | separate junction table | `Blog` ↔ `Tag` |

**Practical notes**

- If a model is defined later in the file than the one it references, use a string instead of the class object to avoid ordering issues: `models.ForeignKey("Author", ...)`.
- Adding any of these fields requires `python manage.py makemigrations` + `migrate`, same as the existing `0007`–`0009` migrations for `Blog`/`Author`.
- Adding a required (`null=False`) `ForeignKey` to a model that already has rows prompts Django's migration for a one-off default value.

**Status in this project:** not yet adopted — `Blog.author` is currently commented out as a plain `CharField`; converting it to a real `ForeignKey` to `Author` is the natural next step.

### Pagination (Paginator and Page)

Rendering every row of a large queryset in one page is slow to query, slow to render, and bad UX. Django's `django.core.paginator` module splits a queryset into fixed-size chunks and lets the user request one chunk (page) at a time via the URL. Used in `blogs()` (`app/views.py`) for the blog listing page.

**Two objects are involved:**

- **`Paginator(queryset, per_page)`** — knows about the *whole* collection. Building it doesn't hit the database yet; it's just told "if I split this into chunks of N, how many chunks are there." Properties like `paginator.num_pages` (total pages) and `paginator.count` (total items) only run a query the first time they're accessed.
- **`paginator.page(number)`** — returns a **`Page`** object for that specific chunk. *This* is what hits the database, running the equivalent of `LIMIT n OFFSET m`. The `Page` wraps just those rows plus metadata: `.has_next`, `.has_previous`, `.number`, `.next_page_number`, `.previous_page_number`.

```python
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def blogs(request):
    all_blogs = Blog.objects.all().order_by('-created_at')
    paginator = Paginator(all_blogs, 3)   # 3 posts per page

    page = request.GET.get('page')        # e.g. "2" from ?page=2, or None

    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)                      # no/invalid ?page= -> first page
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)     # ?page= out of range -> clamp to last page

    return render(request, 'blogs.html', {"blogs": blogs})
```

**Where the page number comes from:** `request.GET.get('page')` reads the `page` query parameter straight off the URL (`/blogs/?page=2`). There's no session or cookie involved — each Prev/Next click is a fresh GET request carrying a different `page` value, and the view recomputes the slice from scratch every time.

**Why the try/except matters:** `paginator.page()` can fail two distinct ways, and Django gives each a dedicated exception so bad input degrades gracefully instead of raising a 500:

- **`PageNotAnInteger`** — `page` isn't a valid integer (no `?page=` at all on first visit, since `request.GET.get('page')` then returns `None`, or someone typed `?page=abc`). Handled by falling back to page 1.
- **`EmptyPage`** — `page` is a valid integer but out of range (`?page=999` when there are only 5 pages). Handled by clamping to the last valid page.

Without this handling, a malformed or out-of-range `page` value in the URL — easy for a user or crawler to produce by hand — would crash the view.

**Template side (`templates/blogs.html`):** the `Page` object's attributes drive the Prev/Next controls without any arithmetic in the template:

```html
{% if blogs.has_previous %}
    <li><a href="?page={{ blogs.previous_page_number }}">Previous</a></li>
{% endif %}
<li class="active"><a href="#">{{ blogs.number }}</a></li>
{% if blogs.has_next %}
    <li><a href="?page={{ blogs.next_page_number }}">Next</a></li>
{% endif %}
```

**Current limitation:** a `Page` only knows its immediate neighbors (previous/next), not the full set of pages, so this template can't render a "1 2 3 4 5" numbered strip. That needs the `Paginator` object's `page_range` property, which isn't currently passed into the context (only `blogs` is) — passing `paginator` too and looping `{% for num in paginator.page_range %}` would add it.

**Status in this project:** adopted for the blog list (`blogs()` view + `templates/blogs.html`) — numbered page links not yet added.

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

### Q: Why does `Model.objects.get(some_id)` fail, while `Model.objects.get(pk=some_id)` works — aren't both just passing an integer?

No — `.get()`/`.filter()` don't accept "the value to look up" as a positional argument at all. Positional args are reserved for `Q` objects; keyword args are how you specify field lookups.

Internally, `get`/`filter` forward whatever you pass into `Q(*args, **kwargs)`, which stores its conditions as a list of "children":

```python
class Q(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(children=list(args) + sorted(kwargs.items()), ...)
```

- `kwargs.items()` naturally produces `(field_lookup, value)` tuples — `id=20` becomes `('id', 20)`.
- `*args` is meant for passing in **other `Q` objects**, so conditions can be combined with `&`/`|` (e.g. `Blog.objects.get(Q(id=20) | Q(slug='foo'))`).

So `Blog.objects.get(20)` doesn't treat `20` as "the id" — it lands in that same `children` list as if it were already a `(key, value)` tuple or another `Q`/`Node`. When the query compiler later walks that tree to build SQL, it does roughly:

```python
for child in q_object.children:
    if isinstance(child, Node):
        ...  # nested Q, recurse
    else:
        key, value = child   # expects a 2-tuple
```

`20` is a plain `int`, not a 2-tuple, so `key, value = 20` raises exactly this: **`TypeError: cannot unpack non-iterable int object`**.

**Fix:** use a keyword argument so `kwargs.items()` produces the `(key, value)` pair it expects:
```python
Blog.objects.get(pk=blog_id)   # kwargs.items() -> [('pk', blog_id)]
```

`pk` means "whatever the primary key field is" (`id` here) — it's the portable spelling that keeps working even if the primary key is later renamed or switched to a UUID.
