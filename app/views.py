from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Welcome To App Page')

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
    return render(request, 'app/home.html', context)