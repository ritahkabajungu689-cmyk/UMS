from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('administrator', 'Administrator'),
        ('registry', 'Registry Staff'),
        ('finance', 'Finance Staff'),
        ('lecturer', 'Lecturer'),
        ('student', 'Student'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'


class StudentProfile(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admission_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    department = models.CharField(max_length=100)
    programme = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    photo = models.FileField(upload_to='student_photos/', null=True, blank=True)

    def __str__(self):
        return f'{self.admission_number} - {self.user.get_full_name() or self.user.username}'


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    credit_units = models.PositiveSmallIntegerField(default=3)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.code} - {self.name}'


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed'),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    registered_on = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course', 'semester')

    def __str__(self):
        return f'{self.student} - {self.course} ({self.semester})'


class Payment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    term = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.student} - {self.amount} ({self.term})'


class Result(models.Model):
    GRADE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    semester = models.CharField(max_length=30)
    remarks = models.CharField(max_length=200, blank=True)
    recorded_on = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course', 'semester')

    def __str__(self):
        return f'{self.student} - {self.course}: {self.grade}'
