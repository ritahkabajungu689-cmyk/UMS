from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/upload-photo/', views.upload_photo, name='upload_photo'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('students/', views.student_list, name='student_list'),
    path('students/new/', views.register_student, name='register_student'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/new/', views.course_create, name='course_create'),
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enrollments/new/', views.create_enrollment, name='create_enrollment'),
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/new/', views.create_payment, name='create_payment'),
    path('results/', views.result_list, name='result_list'),
    path('results/new/', views.create_result, name='create_result'),
    path('reports/', views.overall_report, name='overall_report'),
]
