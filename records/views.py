from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (CourseForm, EnrollmentForm, LoginForm, PaymentForm, ResultForm,
                    StudentRegistrationForm, SignupForm)
from .models import (Course, Enrollment, Payment, Result, StudentProfile,
                     UserProfile)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user_profile = UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'records/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('dashboard')

    return render(request, 'records/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def create_user_profile(user, role):
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.role = role
    profile.save()
    return profile


@login_required(login_url='login')
def profile_view(request):
    try:
        user_profile = request.user.userprofile
        role = user_profile.role
    except UserProfile.DoesNotExist:
        role = 'student'

    student_profile = None
    try:
        student_profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        pass

    return render(request, 'records/profile.html', {
        'role': role,
        'student_profile': student_profile,
    })


@login_required(login_url='login')
def upload_photo(request):
    if request.method == 'POST' and request.FILES.get('photo'):
        try:
            student_profile = request.user.studentprofile
            student_profile.photo = request.FILES['photo']
            student_profile.save()
            messages.success(request, 'Photo updated successfully!')
        except StudentProfile.DoesNotExist:
            messages.error(request, 'No student profile found. Contact the Registry office.')
    return redirect('profile')


@login_required(login_url='login')
def dashboard(request):
    try:
        user_profile = request.user.userprofile
        role = user_profile.role
    except UserProfile.DoesNotExist:
        role = 'student'

    context = {'role': role}

    # Global stats for all roles now
    context['stats'] = {
        'students': StudentProfile.objects.count(),
        'courses': Course.objects.count(),
        'enrollments': Enrollment.objects.count(),
        'payments': Payment.objects.count(),
        'results': Result.objects.count(),
    }
    context['students_with_balance'] = StudentProfile.objects.filter(payment__isnull=True).distinct().count()
    context['recent_payments'] = Payment.objects.select_related('student__user').order_by('-id')[:5]
    context['recent_students'] = StudentProfile.objects.select_related('user').order_by('-id')[:5]
    context['recent_results'] = Result.objects.select_related('student__user', 'course').order_by('-id')[:5]

    # Fetch student profile for logged-in student
    context['student_profile'] = None
    if role == 'student':
        try:
            from django.db.models import Sum, Avg
            sp = request.user.studentprofile
            context['student_profile'] = sp
            context['student_stats'] = {
                'courses_enrolled':  Enrollment.objects.filter(student=sp).count(),
                'results_count':     Result.objects.filter(student=sp).count(),
                'payments_count':    Payment.objects.filter(student=sp).count(),
                'total_paid':        Payment.objects.filter(student=sp).aggregate(t=Sum('amount'))['t'] or 0,
                'courses_completed': Enrollment.objects.filter(student=sp, status='completed').count(),
                'avg_score':         Result.objects.filter(student=sp).aggregate(a=Avg('score'))['a'] or 0,
            }
            # Student-specific history (most recent 6 of each)
            context['recent_results'] = Result.objects.filter(
                student=sp
            ).select_related('course').order_by('-id')[:6]
            context['recent_payments'] = Payment.objects.filter(
                student=sp
            ).select_related('student__user').order_by('-paid_on')[:6]
        except StudentProfile.DoesNotExist:
            context['student_stats'] = {}

    return render(request, 'records/dashboard.html', context)



@login_required(login_url='login')
def student_list(request):
    students = StudentProfile.objects.select_related('user').all()
    return render(request, 'records/student_list.html', {'students': students})


@login_required(login_url='login')
def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user_data = {
                'username': form.cleaned_data['username'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
            }
            password = form.cleaned_data['password']
            admission_number = form.cleaned_data.get('admission_number')

            if StudentProfile.objects.filter(admission_number=admission_number).exists():
                form.add_error('admission_number', 'This admission number is already registered.')
            else:
                try:
                    user = User.objects.create_user(**user_data, password=password)
                except IntegrityError as e:
                    if User.objects.filter(username=user_data['username']).exists():
                        form.add_error('username', 'A user with that username already exists.')
                    elif User.objects.filter(email=user_data['email']).exists():
                        form.add_error('email', 'A user with that email already exists.')
                    else:
                        form.add_error(None, 'Unable to create user. Please try again.')
                else:
                    role = form.cleaned_data['role']
                    create_user_profile(user, role)
                    student = form.save(commit=False)
                    student.user = user
                    try:
                        student.save()
                    except IntegrityError:
                        form.add_error('admission_number', 'This admission number is already registered.')
                    else:
                        messages.success(request, 'Student profile created successfully.')
                        return redirect('student_list')
    else:
        form = StudentRegistrationForm()

    return render(request, 'records/student_form.html', {'form': form})


@login_required(login_url='login')
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'records/course_list.html', {'courses': courses})


@login_required(login_url='login')
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course saved successfully.')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'records/course_form.html', {'form': form})


@login_required(login_url='login')
def enrollment_list(request):
    enrollments = Enrollment.objects.select_related('student__user', 'course').all()
    return render(request, 'records/enrollment_list.html', {'enrollments': enrollments})


@login_required(login_url='login')
def create_enrollment(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enrollment created successfully.')
            return redirect('enrollment_list')
    else:
        form = EnrollmentForm()
    return render(request, 'records/enrollment_form.html', {'form': form})


@login_required(login_url='login')
def payment_list(request):
    from django.db.models import Sum
    try:
        role = request.user.userprofile.role
        if role == 'student':
            payments = Payment.objects.filter(student__user=request.user).select_related('student__user').order_by('-paid_on')
            total_ugx = payments.aggregate(total=Sum('amount'))['total'] or 0
            # Build per-term totals for the chart
            from collections import defaultdict
            term_totals = defaultdict(float)
            for p in payments:
                term_totals[p.term] += float(p.amount)
            payment_summary = {
                'total_paid': total_ugx,
                'total_due': max(0, 1800000 - float(total_ugx)),  # standard tuition = 1,800,000 UGX
                'total_payable': 1800000,
                'term_totals': dict(term_totals),
            }
        else:
            payments = Payment.objects.select_related('student__user').order_by('-paid_on')
            total_ugx = payments.aggregate(total=Sum('amount'))['total'] or 0
            payment_summary = None
    except UserProfile.DoesNotExist:
        payments = Payment.objects.none()
        total_ugx = 0
        payment_summary = None
    return render(request, 'records/payment_list.html', {
        'payments': payments,
        'total_ugx': total_ugx,
        'payment_summary': payment_summary,
    })


@login_required(login_url='login')
def create_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment recorded successfully.')
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'records/payment_form.html', {'form': form})


@login_required(login_url='login')
def result_list(request):
    try:
        if request.user.userprofile.role == 'student':
            results = Result.objects.filter(student__user=request.user).select_related('student__user', 'course')
        else:
            results = Result.objects.select_related('student__user', 'course').all()
    except UserProfile.DoesNotExist:
        results = Result.objects.none()
    return render(request, 'records/result_list.html', {'results': results})


@login_required(login_url='login')
def create_result(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Result recorded successfully.')
            return redirect('result_list')
    else:
        form = ResultForm()
    return render(request, 'records/result_form.html', {'form': form})


@login_required(login_url='login')
def overall_report(request):
    from django.db.models import Sum
    stats = {
        'students': StudentProfile.objects.count(),
        'courses': Course.objects.count(),
        'enrollments': Enrollment.objects.count(),
        'payments': Payment.objects.count(),
        'results': Result.objects.count(),
    }
    recent_payments = Payment.objects.select_related('student__user').order_by('-paid_on')[:10]
    recent_results = Result.objects.select_related('student__user', 'course').order_by('-id')[:10]
    return render(request, 'records/report_dashboard.html', {
        'stats': stats,
        'recent_payments': recent_payments,
        'recent_results': recent_results,
    })
