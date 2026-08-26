from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'app_name': 'App',
        'description': 'This page is served from the app-level template folder: app/templates/app/index.html.',
        'tasks': [
            {'name': 'Learn Models', 'done': True},
            {'name': 'Learn Views', 'done': True},
            {'name': 'Learn Templates', 'done': False},
            {'name': 'Learn Forms', 'done': False},
        ],
        'version': '0.1',
    }
    return render(request, 'app/index.html', context)

def home(request):
    context = {
        'site_name': 'Django Learning',
        'tagline': 'Practice projects, apps, and notes as I learn Django.',
        'features': [
            {'title': 'Models', 'description': 'Define data structures and talk to the database.'},
            {'title': 'Views', 'description': 'Handle request logic and decide what to send back.'},
            {'title': 'Templates', 'description': 'Render HTML for the user.'},
        ],
        'visitor_count': 128,
    }
    return render(request, 'home.html', context)