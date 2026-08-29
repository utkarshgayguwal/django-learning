from django.shortcuts import render
from app.models import (
    GeneralInfo,
    Service,
    Testimonial,
    FrequentlyAskedQuestion,
)


def index(request):
    general_info = GeneralInfo.objects.first()
    services = Service.objects.all()
    testimonials = Testimonial.objects.all()
    faqs = FrequentlyAskedQuestion.objects.all()
    context = {
        "general_info": general_info,
        "services": services,
        "testimonials": testimonials,
        "faqs": faqs,
    }
    return render(request, "index.html", context)
