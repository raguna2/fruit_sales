from django.contrib import admin
from accounts.models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ['username']

admin.site.register(Employee,EmployeeAdmin)
