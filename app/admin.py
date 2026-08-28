from django.contrib import admin
from app.models import GeneralInfo

@admin.register(GeneralInfo)
class GeneralInfoAdmin(admin.ModelAdmin):
    
    list_display = [
        'company_name',
        'location',
        'email'
    ]

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

