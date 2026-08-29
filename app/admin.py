from django.contrib import admin
from app.models import GeneralInfo
from app.models import Service
from app.models import Testimonial
from app.models import FrequentlyAskedQuestion

@admin.register(GeneralInfo)
class GeneralInfoAdmin(admin.ModelAdmin):
    
    list_display = [
        'company_name',
        'location',
        'email'
    ]

    list_display_links = ['company_name']

    # list_filter = ['location', 'phone']

    search_fields = ['company_name']

    readonly_fields = [
        'email'
    ]

    # disallow adding new GeneralInfo entries from the admin
    # def has_add_permission(self, request):
    #     return False

    # disallow editing existing GeneralInfo entries from the admin
    # def has_change_permission(self, request, obj=None):
    #     return False

    # disallow deleting GeneralInfo entries from the admin
    # def has_delete_permission(self, request, obj=None):
    #     return False

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description'
    ]

    search_fields = [
        'title',
        'description'
    ]

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = [
        'username', 
        'user_job_title',
        'display_rating_count'
    ]

    def display_rating_count(self, obj):
        return '*' * obj.rating_count
    
    display_rating_count.short_description = "Rating"

@admin.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestionAdmin(admin.ModelAdmin):
    list_display = [
        'question'
    ]

    search_fields = [
        'question'
    ]