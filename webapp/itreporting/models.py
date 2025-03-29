from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Task Model
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Course Model
class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Module Model
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    code = models.CharField(max_length=20, unique=True)  # Unique code for the module
    name = models.CharField(max_length=200)
    description = models.TextField()
    is_open_for_registration = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.course.name})"

# Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username

# Registration Model
class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'module')  # Enforce unique registration per module

    def __str__(self):
        return f"{self.student.user.username} registered for {self.module.name}"

# Signal to Create Student Profile Automatically
@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)

# Signal to Automatically Register a Student to a Module
@receiver(post_save, sender=Module)
def auto_register_student(sender, instance, created, **kwargs):
    if created:
        # Example logic: Automatically register the first student to the module
        student = Student.objects.first()  # Replace with actual logic
        if student:
            Registration.objects.get_or_create(student=student, module=instance)