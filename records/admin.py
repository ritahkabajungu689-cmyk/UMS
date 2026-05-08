from django.contrib import admin
from .models import UserProfile, StudentProfile, Course, Enrollment, Payment, Result

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'user', 'department', 'status')
    search_fields = ('user__username', 'admission_number', 'user__first_name', 'user__last_name')
    list_filter = ('department', 'status')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'credit_units')
    search_fields = ('code', 'name')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'status')
    list_filter = ('semester', 'status')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'term', 'amount', 'paid_on')
    search_fields = ('student__user__username', 'term')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'grade', 'semester')
    list_filter = ('semester', 'grade')
