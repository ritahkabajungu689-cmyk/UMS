from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from records.models import (
    UserProfile, StudentProfile, Course, Enrollment, Payment, Result
)
from datetime import date, timedelta
import random


CS_COURSES = [
    ("CS101", "Introduction to Programming", 3),
    ("CS102", "Data Structures and Algorithms", 4),
    ("CS201", "Object-Oriented Programming", 3),
    ("CS202", "Database Management Systems", 3),
    ("CS203", "Web Development Fundamentals", 3),
    ("CS301", "Operating Systems", 4),
    ("CS302", "Computer Networks", 3),
    ("CS303", "Software Engineering", 3),
    ("CS304", "Artificial Intelligence", 4),
    ("CS305", "Machine Learning", 4),
    ("CS401", "Cloud Computing", 3),
    ("CS402", "Cybersecurity and Ethical Hacking", 3),
    ("CS403", "Mobile Application Development", 3),
    ("CS404", "Computer Architecture", 3),
    ("CS405", "Human-Computer Interaction", 2),
    ("MATH101", "Discrete Mathematics", 3),
    ("MATH102", "Probability and Statistics", 3),
    ("CS406", "Compiler Design", 3),
    ("CS407", "Distributed Systems", 4),
    ("CS408", "Capstone Project", 6),
]

STUDENTS_DATA = [
    ("alice.nakato", "Alice", "Nakato", "alice@university.ac.ug", "2024/CS/001", "Computer Science", "BSc", "F", "0701234567"),
    ("bob.okello", "Bob", "Okello", "bob@university.ac.ug", "2024/CS/002", "Computer Science", "BSc", "M", "0702345678"),
    ("cathy.atim", "Cathy", "Atim", "cathy@university.ac.ug", "2024/CS/003", "Computer Science", "BSc", "F", "0703456789"),
    ("david.mugisha", "David", "Mugisha", "david@university.ac.ug", "2024/CS/004", "Computer Science", "BSc", "M", "0704567890"),
    ("esther.nabirye", "Esther", "Nabirye", "esther@university.ac.ug", "2024/CS/005", "Computer Science", "BSc", "F", "0705678901"),
]

GRADES = ["A", "B", "B", "C", "A", "B", "C", "A"]
SEMESTERS = ["Semester 1 2025/26", "Semester 2 2025/26"]
PAYMENT_TERMS = ["Tuition Sem 1", "Tuition Sem 2", "Registration Fee", "Library Fee", "Lab Fee"]


class Command(BaseCommand):
    help = "Seed mock data: CS courses, students, payments, results"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding CS Courses...")
        courses = []
        for code, name, credits in CS_COURSES:
            c, created = Course.objects.get_or_create(code=code, defaults={
                "name": name, "credit_units": credits
            })
            courses.append(c)
            if created:
                self.stdout.write(f"  + Course: {code} - {name}")

        self.stdout.write("\nSeeding Students...")
        students = []
        for username, first, last, email, adm, dept, prog, gender, phone in STUDENTS_DATA:
            user, _ = User.objects.get_or_create(username=username, defaults={
                "first_name": first, "last_name": last, "email": email
            })
            user.set_password("pass1234")
            user.save()
            UserProfile.objects.get_or_create(user=user, defaults={"role": "student"})
            sp, created = StudentProfile.objects.get_or_create(
                user=user,
                defaults={
                    "admission_number": adm,
                    "department": dept,
                    "programme": prog,
                    "gender": gender,
                    "phone": phone,
                    "status": "active",
                }
            )
            students.append(sp)
            if created:
                self.stdout.write(f"  + Student: {first} {last} ({adm})")

        self.stdout.write("\nSeeding Payments (in UGX)...")
        amounts = [1500000, 850000, 200000, 150000, 100000]
        for i, sp in enumerate(students):
            for j, (term, amount) in enumerate(zip(PAYMENT_TERMS, amounts)):
                if not Payment.objects.filter(student=sp, term=term).exists():
                    p = Payment.objects.create(
                        student=sp,
                        term=term,
                        amount=amount,
                        description=f"{term} - {sp.admission_number}",
                    )
                    # backdate paid_on using update (auto_now_add skips create)
                    Payment.objects.filter(pk=p.pk).update(
                        paid_on=date.today() - timedelta(days=random.randint(5, 90))
                    )
                    self.stdout.write(f"  + Payment: {sp.admission_number} - {term} UGX {amount:,}")

        self.stdout.write("\nSeeding Results...")
        selected_courses = courses[:8]
        for sp in students:
            for course in selected_courses:
                for sem in SEMESTERS:
                    if not Result.objects.filter(student=sp, course=course, semester=sem).exists():
                        grade = random.choice(GRADES)
                        score = {"A": random.uniform(80, 100), "B": random.uniform(65, 79),
                                 "C": random.uniform(50, 64), "D": random.uniform(40, 49),
                                 "F": random.uniform(0, 39)}[grade]
                        Result.objects.create(
                            student=sp, course=course, grade=grade,
                            score=round(score, 2), semester=sem
                        )
            self.stdout.write(f"  + Results for {sp.admission_number}")

        self.stdout.write(self.style.SUCCESS("\n✅ Seed complete!"))
