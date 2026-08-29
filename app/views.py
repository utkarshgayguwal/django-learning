from django.shortcuts import render
from app.models import GeneralInfo

def index(request):
    general_info = GeneralInfo.objects.first()
    context = {'general_info' : general_info}
    return render(request, 'index.html', context)