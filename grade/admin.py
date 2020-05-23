from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ResultFileUpload, Results, User, Student, Assignment, Grade, ResultCase
# Register your models here.


admin.site.register(User, UserAdmin)
admin.site.register(Grade)
