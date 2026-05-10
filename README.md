# UMS: Unified University Management System
> **The Centralized Intelligence Hub for Academic and Administrative Excellence.**

---

##  Project Overview

**UMS (University Management System)** is an enterprise-grade, role-based platform designed to streamline the complex operations of modern educational institutions. From student registration and course management to financial auditing and academic reporting, UMS provides a unified interface for students, lecturers, and administrative staff to interact with real-time data.

##  The Problem Statement

Traditional university administration often suffers from "Information Silos"—where different departments use disconnected tools to manage their specific domains.

1.  **Administrative Friction**: Manual data entry across multiple systems leads to high error rates and delayed processing of student records.
2.  **Financial Opacity**: Tracking tuition payments and outstanding balances manually is labor-intensive and prone to reconciliation issues.
3.  **Academic Disconnect**: Enrollments, results, and student profiles are often out of sync, making it difficult for lecturers to track progress and for students to view their academic standing.
4.  **Reporting Bottlenecks**: Generating institutional health reports (enrollment stats, financial performance, academic averages) often takes days instead of seconds.

---

##  The Proposed Solution: Unified Intelligence

UMS solves these challenges by centralizing all institutional data into a secure, scalable, and intuitive digital ecosystem.

### 1. Role-Based Access Control (RBAC)
Tailored experiences for five distinct institutional roles:
*   **Administrator**: Full system oversight and governance.
*   **Registry Staff**: Management of student registrations and academic data.
*   **Finance Staff**: Oversight of tuition payments and financial auditing.
*   **Lecturers**: Recording of student results and academic performance.
*   **Students**: Self-service access to profiles, results, and payment history.

### 2. Academic Lifecycle Management
Automates the entire student journey:
*   **Registration**: Streamlined student onboarding with unique admission IDs.
*   **Enrollment**: Easy registration for courses across different semesters.
*   **Results**: Instant recording and calculation of grades and academic remarks.

### 3. Financial Transparency Engine
Real-time tracking of institutional revenue and student balances:
*   **Payment Logs**: Automated recording of tuition and departmental fees.
*   **Balance Tracking**: Instant visibility into student payment status (e.g., standard tuition vs. actual paid).

### 4. Dynamic Reporting Dashboards
Real-time metrics for institutional decision-making:
*   **Visual Analytics**: Charts and stats showing student population growth, average academic scores, and revenue trends.
*   **Recent Activity Tickers**: Live feeds of the latest registrations, payments, and result entries.

---

##  Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python / Django Framework |
| **Database** | PostgreSQL (Production) / SQLite (Development) |
| **Frontend** | Semantic HTML5, Vanilla CSS3, JavaScript |
| **Storage** | Django File Storage (AWS S3 / Local) |
| **Security** | Django Auth Middleware, PBKDF2 Password Hashing |
| **Reporting** | Django ORM Aggregation (Sum, Avg), Charts.js |
| **Deployment** | Vercel Serverless Functions, WhiteNoise, Gunicorn |

---

##  Getting Started

### Prerequisites
*   Python 3.10+
*   PostgreSQL (optional, defaults to SQLite for local dev)

### Installation
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/ritahkabajungu689-cmyk/UMS.git
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Database Migration**:
    ```bash
    python manage.py migrate
    ```
4.  **Create Superuser**:
    ```bash
    python manage.py createsuperuser
    ```
5.  **Run Development Server**:
    ```bash
    python manage.py runserver
    ```

---
### **Developed by THE INTELLECTS**
*Engineering the future of academic management through scalable digital solutions.*
