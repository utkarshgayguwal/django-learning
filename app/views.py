from django.shortcuts import render
from app.models import GeneralInfo
from app.models import Service
from app.models import Testimonial

def index(request):
    general_info = GeneralInfo.objects.first()
    services = Service.objects.all()
    testimonials = Testimonial.objects.all()
    context = {'general_info' : general_info, 'services': services, 'testimonials': testimonials}
    return render(request, 'index.html', context)