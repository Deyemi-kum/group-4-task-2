from django.contrib import admin
from .itreporting.models import Task
from .itreporting.models import Student
from .itreporting.models import Registration

admin.site.register(Task)
admin.site.register(Student)
admin.site.register(Registration)
