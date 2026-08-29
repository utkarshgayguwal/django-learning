from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
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

        context = {
            "name" : name,
            "email" : email,
            "subject" : subject,
            "message" : message
        }

        html_content = render_to_string('email.html', context)

        try: 
            send_mail(
                subject= subject,
                message= None,    
                html_message= html_content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        except Exception as e:
            messages.error(request, "There is an error, could not send email")
        else:
            messages.success(request, "Email has been sent")

    return redirect('home')
