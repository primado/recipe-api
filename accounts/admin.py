from django.contrib import admin
from .models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'email', 'full_name', 'headline']
    search_fields = ["username", "full_name"]

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    full_name.short_description = "Full Name"




