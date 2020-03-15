from django.contrib import admin
from .models import ResultFileUpload, Results, User, Student, Assignment, Grade
# Register your models here.

admin.site.register(ResultFileUpload)
admin.site.register(Results)
admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(User)
admin.site.register(Grade)
