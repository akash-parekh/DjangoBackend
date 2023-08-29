from django.contrib import admin

# Register your models here.
from .models import Employee, Document, Assignment

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("emp_name", "emp_id")

class DocumentAdmin(admin.ModelAdmin):
    list_display = ("doc_name", "doc_id", "status")
    
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("doc_id", "process_emp", "review_emp", 'status')
    
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Assignment, AssignmentAdmin)