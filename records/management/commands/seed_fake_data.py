from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from records.models import UserProfile, StudentProfile, Course, Enrollment, Payment, Result
from datetime import date
import random


class Command(BaseCommand):
    help = 'Generate realistic dummy data for the university records system.'

    def add_arguments(self, parser):
        parser.add_argument('--students', type=int, default=20, help='Number of fake students to create.')
        parser.add_argument('--courses', type=int, default=10, help='Number of courses to create.')
        parser.add_argument('--lecturers', type=int, default=5, help='Number of lecturer accounts to create.')
        parser.add_argument('--enrollments', type=int, default=40, help='Number of enrollments to create.')
        parser.add_argument('--payments', type=int, default=40, help='Number of payment records to create.')
        parser.add_argument('--results', type=int, default=60, help='Number of result records to create.')

    def handle(self, *args, **options):
        fake = Faker()
        Faker.seed(0)
        random.seed(0)

        self.stdout.write('Seeding fake data...')
        self._create_admin()
        self._create_lecturers(options['lecturers'], fake)
        courses = self._create_courses(options['courses'], fake)
        students = self._create_students(options['students'], fake)
        self._create_enrollments(options['enrollments'], students, courses, fake)
        self._create_payments(options['payments'], students, fake)
        self._create_results(options['results'], students, courses, fake)

        self.stdout.write(self.style.SUCCESS('Fake data successfully seeded.'))

    def _create_admin(self):
        admin_email = 'admin@university.edu'
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': admin_email, 'first_name': 'System', 'last_name': 'Administrator'}
        )
        if created:
            admin_user.set_password('admin1234')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
        UserProfile.objects.get_or_create(user=admin_user, defaults={'role': 'administrator'})

    def _unique_username(self, fake):
        for _ in range(50):
            username = fake.user_name()
            if not User.objects.filter(username=username).exists():
                return username
        raise ValueError('Unable to generate a unique username.')

    def _unique_email(self, fake):
        for _ in range(50):
            email = fake.email()
            if not User.objects.filter(email=email).exists():
                return email
        raise ValueError('Unable to generate a unique email.')

    def _unique_course_code(self, fake):
        for _ in range(50):
            code = f"{fake.lexify(text='??').upper()}{fake.random_int(min=101, max=499)}"
            if not Course.objects.filter(code=code).exists():
                return code
        raise ValueError('Unable to generate a unique course code.')

    def _unique_admission_number(self):
        current_year = date.today().year
        for _ in range(1000):
            code = f'UNI{current_year}{random.randint(1000, 9999)}'
            if not StudentProfile.objects.filter(admission_number=code).exists():
                return code
        raise ValueError('Unable to generate a unique admission number.')

    def _create_lecturers(self, lecturer_count, fake):
        roles = []
        for _ in range(lecturer_count):
            username = self._unique_username(fake)
            email = self._unique_email(fake)
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='lecturer123'
            )
            UserProfile.objects.create(user=user, role='lecturer')
            roles.append(user)
        return roles

    def _create_courses(self, course_count, fake):
        subjects = ['Computer Science', 'Business Management', 'Economics', 'Engineering', 'Mathematics', 'Biology', 'Psychology', 'Law', 'Accounting', 'Marketing']
        courses = []
        for i in range(course_count):
            code = self._unique_course_code(fake)
            course = Course.objects.create(
                code=code,
                name=fake.sentence(nb_words=3).rstrip('.'),
                credit_units=random.choice([2, 3, 4]),
                description=fake.paragraph(nb_sentences=3)
            )
            courses.append(course)
        return courses

    def _create_students(self, student_count, fake):
        students = []
        for _ in range(student_count):
            username = self._unique_username(fake)
            email = self._unique_email(fake)
            first_name = fake.first_name()
            last_name = fake.last_name()
            admission_number = self._unique_admission_number()
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password='student1234'
            )
            UserProfile.objects.create(user=user, role='student')
            student = StudentProfile.objects.create(
                user=user,
                admission_number=admission_number,
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=25),
                gender=random.choice(['Male', 'Female']),
                department=fake.random_element(elements=('Computer Science', 'Business', 'Engineering', 'Economics', 'Law', 'Biology')),
                programme=fake.random_element(elements=('BSc', 'BA', 'BEng', 'BCom', 'LLB')),
                status=random.choice(['active', 'inactive']),
                phone=fake.phone_number(),
                address=fake.address(),
            )
            students.append(student)
        return students

    def _create_enrollments(self, enrollment_count, students, courses, fake):
        terms = ['Semester 1', 'Semester 2']
        for _ in range(enrollment_count):
            student = random.choice(students)
            course = random.choice(courses)
            semester = random.choice(terms)
            Enrollment.objects.get_or_create(
                student=student,
                course=course,
                semester=semester,
                defaults={'status': random.choice(['registered', 'completed', 'dropped'])}
            )

    def _create_payments(self, payment_count, students, fake):
        terms = ['Semester 1', 'Semester 2']
        for _ in range(payment_count):
            student = random.choice(students)
            Payment.objects.create(
                student=student,
                term=random.choice(terms),
                amount=random.choice([2000.00, 2500.00, 3000.00, 3500.00]),
                description=fake.sentence(nb_words=6)
            )

    def _create_results(self, result_count, students, courses, fake):
        grades = ['A', 'B', 'C', 'D', 'F']
        terms = ['Semester 1', 'Semester 2']
        for _ in range(result_count):
            student = random.choice(students)
            course = random.choice(courses)
            semester = random.choice(terms)
            score = random.uniform(40.0, 100.0)
            grade = random.choice(grades)
            Result.objects.get_or_create(
                student=student,
                course=course,
                semester=semester,
                defaults={
                    'score': round(score, 2),
                    'grade': grade,
                    'remarks': fake.sentence(nb_words=8)
                }
            )
