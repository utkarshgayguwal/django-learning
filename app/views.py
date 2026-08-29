from django.shortcuts import render
from app.models import GeneralInfo
from app.models import Service

def index(request):
    general_info = GeneralInfo.objects.first()
    services = Service.objects.all()
    context = {'general_info' : general_info, 'services': services}
    return render(request, 'index.html', context)