from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
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

def contact_form(request):
    print(request)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        print(f"name: {name}\nemail: {email}\nsubject: {subject}\nmessage: {message}")
        
        send_mail(
            subject= subject,
            message= f"{name} - {email} - {message}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

   
    print("User has submitted contact form")
    return redirect('home')
