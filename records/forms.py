from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import StudentProfile, Course, Enrollment, Payment, Result, UserProfile


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20', 'placeholder': 'Password'}))


class SignupForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20', 'placeholder': 'Username'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20', 'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20', 'placeholder': 'Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20', 'placeholder': 'Password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20', 'placeholder': 'Confirm Password'}))
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, initial='student', widget=forms.Select(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}))
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}))
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, initial='student', widget=forms.Select(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}))

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}))

    DEPARTMENT_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Business Management', 'Business Management'),
        ('Economics', 'Economics'),
        ('Engineering', 'Engineering'),
        ('Mathematics', 'Mathematics'),
        ('Biology', 'Biology'),
        ('Psychology', 'Psychology'),
        ('Law', 'Law'),
        ('Accounting', 'Accounting'),
        ('Marketing', 'Marketing'),
    ]
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.Select(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}))

    PROGRAMME_CHOICES = [
        ('BSc', 'Bachelor of Science'),
        ('BA', 'Bachelor of Arts'),
        ('BEng', 'Bachelor of Engineering'),
        ('BCom', 'Bachelor of Commerce'),
        ('LLB', 'Bachelor of Laws'),
        ('MSc', 'Master of Science'),
        ('MBA', 'Master of Business Administration'),
        ('PhD', 'Doctor of Philosophy'),
    ]
    programme = forms.ChoiceField(choices=PROGRAMME_CHOICES, widget=forms.Select(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_admission_number(self):
        admission_number = self.cleaned_data.get('admission_number')
        if StudentProfile.objects.filter(admission_number=admission_number).exists():
            raise forms.ValidationError('This admission number is already registered.')
        return admission_number

    class Meta:
        model = StudentProfile
        fields = ['admission_number', 'date_of_birth', 'gender', 'department', 'programme', 'phone', 'address', 'status', 'photo']
        widgets = {
            'admission_number': forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'address': forms.Textarea(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'photo': forms.FileInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20', 'accept': 'image/*'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'credit_units', 'description']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'name': forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'credit_units': forms.NumberInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'description': forms.Textarea(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20', 'rows': 3}),
        }


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'semester', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'course': forms.Select(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'semester': forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'status': forms.Select(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'term', 'amount', 'description']
        widgets = {
            'student': forms.Select(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'term': forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'amount': forms.NumberInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'description': forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
        }


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'course', 'score', 'grade', 'semester', 'remarks']
        widgets = {
            'student': forms.Select(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'course': forms.Select(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'score': forms.NumberInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'grade': forms.Select(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'semester': forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
            'remarks': forms.TextInput(attrs={'class': 'block w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm focus:border-sidebarActive focus:ring-2 focus:ring-sidebarActive/20'}),
        }
