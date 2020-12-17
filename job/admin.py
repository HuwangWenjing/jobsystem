from django.contrib import admin

# Register your models here.
from django.contrib import admin
# Register your models here.
from .models import sign, teacher, student, course,notice



admin.site.register(sign)
admin.site.register(teacher)
admin.site.register(student)
admin.site.register(course)
