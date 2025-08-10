from django.contrib import admin
from .models import Student, Course, Attendance

# Register your models here.
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Attendance)