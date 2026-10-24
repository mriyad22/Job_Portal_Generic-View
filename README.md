<div align="center">

# JobHub — Django Job Portal

**A role-based job portal for recruiters and job seekers, built with Django.**

[Features](#-features) · [Tech Stack](#-tech-stack) · [Getting Started](#-getting-started) · [Project Structure](#-project-structure) · [Roadmap](#-future-improvements)

</div>

---

## 📌 Overview

**JobHub** is a web-based job portal designed to connect recruiters with job seekers. Recruiters can publish and manage job vacancies, while seekers can explore opportunities, submit applications with resumes, and track their applications.

This project demonstrates practical Django development concepts, including class-based views, authentication, role-based access, model relationships, forms, file uploads, query optimization, and responsive templates.

## ✨ Features

### 👤 Accounts & Profiles
- User registration and login/logout.
- Separate account roles: **Recruiter** and **Seeker**.
- Profile viewing and profile updates.
- Password change functionality.
- Company profile details and logo upload for recruiters.
- Personal profile image and contact information for seekers.

### 💼 Job Management
- Recruiters can publish job vacancies.
- Job information includes title, category, description, required skills, shift type, openings, salary, and deadline.
- Recruiters can update or delete their own job posts.
- Job list supports keyword search and category filtering.
- Pagination keeps job listings easier to browse.

### 📄 Applications
- Seekers can apply for jobs and upload a resume.
- Seekers can view their submitted applications.
- Recruiters can view applicants for their own job posts.
- Role and ownership checks protect recruiter-only and seeker-only workflows.

### 🎨 User Interface
- Responsive templates styled with Bootstrap.
- Shared base layout and navigation.
- Job cards, forms, feedback messages, and delete confirmation pages.
- CSRF-protected logout form.

### ⚙️ Django Concepts Demonstrated
- Class-based views and generic views.
- Django authentication and messages framework.
- ModelForms and form validation.
- ForeignKey and OneToOne relationships.
- ORM query optimization with `select_related()`.
- Search, filtering, and pagination.
- File and image uploads.

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Django | Web framework, routing, ORM, authentication |
| SQLite | Default development database |
| HTML5 / CSS3 | Page structure and styling |
| Bootstrap | Responsive UI components |
| Pillow | Image handling for uploaded profile/company images |

## 🏗️ Architecture

The project follows Django's **Model–Template–View (MTV)** architecture:

- **Models** define users, profiles, job categories, job posts, and applications.
- **Views** handle requests, permissions, business logic, and responses.
- **Templates** render the UI using Django Template Language.
- **URL configuration** maps incoming paths to class-based views.
- **Django ORM** reads and writes application data.

## 🗂️ Project Structure

```text
JobHub/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── portal/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
├── templates/
│   ├── auth/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── password_change.html
│   ├── jobs/
│   │   ├── jb-list.html
│   │   └── jb-post.html
│   ├── master/
│   │   ├── base.html
│   │   └── nav.html
│   ├── candidate.html
│   ├── delete.html
│   ├── home.html
│   ├── jb-apply.html
│   ├── message.html
│   ├── my-applied.html
│   ├── profile.html
│   └── profile-update.html
├── manage.py
├── requirements.txt
└── README.md
```

## 🧩 Data Models

| Model | Responsibility |
|---|---|
| `UserModel` | Custom Django user with a `Recruiter` or `Seeker` role |
| `RecruiterProfileModel` | Recruiter/company profile, contact details, and logo |
| `SeekerProfileModel` | Seeker profile, contact details, and profile image |
| `CategoryModel` | Job category records |
| `JobPostModel` | Job details, requirements, salary, deadline, shift, and recruiter |
| `JobApplyModel` | Resume, application date, seeker, and related job |

### Relationship overview

- A user can have a recruiter profile or a seeker profile.
- A recruiter profile can publish multiple job posts.
- A category can be associated with multiple job posts.
- A seeker can submit applications to multiple jobs.
- A job post can receive applications from multiple seekers. Applications are represented by `JobApplyModel`, which also stores the uploaded resume and application date.

## 🔐 Authentication & Access Control

JobHub uses Django's authentication system and a custom user model.

- Authentication is required for protected profile and application pages.
- Recruiter-only actions are restricted to recruiter accounts.
- Recruiters can update/delete their own job posts and view applicants for their own posts.
- Job application workflows validate the seeker's role.
- Logout uses a POST form with CSRF protection.

> **Development note:** Always review and test permissions before deploying. Production deployments should also configure secure cookies, HTTPS, allowed hosts, secret management, and upload validation.

## 🔄 Typical User Workflows

### Recruiter
1. Register or sign in as a recruiter.
2. Complete the recruiter/company profile.
3. Create a job post with requirements and a deadline.
4. Manage posted jobs.
5. Open the applicant list for a job and review applications.

### Seeker
1. Register or sign in as a seeker.
2. Complete the seeker profile.
3. Search and filter available jobs.
4. Open a suitable job and submit an application with a resume.
5. Review submitted applications from the application list.

## 🚀 Getting Started

### Prerequisites

- Python **3.11 or newer**
- `pip`
- Git (optional)

### 1. Clone the repository

Replace `<repository-url>` with your repository URL:

```bash
git clone <repository-url>
cd JobHub
```

If you downloaded the ZIP instead, extract it and open a terminal in the project directory.

### 2. Create and activate a virtual environment

**Windows — Command Prompt**
```bat
python -m venv .venv
.venv\Scripts\activate
```

**Windows — PowerShell**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure the database

```bash
python manage.py makemigrations portal
python manage.py migrate
```

### 5. Create an admin account

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

Django admin is available at **http://127.0.0.1:8000/admin/** after creating a superuser.

### 7. Run basic checks

```bash
python manage.py check
```

## 🖼️ Screenshots

Add screenshots of your running application to a `screenshots/` folder, then update the paths below.

| Page | Preview |
|---|---|
| Home page | `screenshots/home.png` |
| Job listing | `screenshots/job-list.png` |
| Job details / application | `screenshots/job-application.png` |
| Recruiter dashboard or profile | `screenshots/profile.png` |

Example Markdown to enable a screenshot:

```md
![Job listing](screenshots/job-list.png)
```

## ⚙️ Configuration & Environment

The development project currently uses SQLite and project settings in `config/settings.py`.

Before production deployment:

1. Move `SECRET_KEY` to an environment variable and replace the development key.
2. Set `DEBUG = False`.
3. Configure `ALLOWED_HOSTS`.
4. Configure HTTPS and secure session/CSRF cookies.
5. Configure static and media file storage.
6. Use a production-ready database and web server where appropriate.

Example environment variable names to adopt when configuring deployment:

```text
DJANGO_SECRET_KEY=replace-with-a-long-random-secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=example.com,www.example.com
```

These are suggested names for deployment configuration; the current settings file must be updated to read them before they take effect.

## 🧪 Testing

Run the project's test suite with:

```bash
python manage.py test
```

Use the following manual test checklist before release:

- [ ] Register and log in as a recruiter.
- [ ] Complete recruiter profile and publish a job.
- [ ] Confirm a recruiter cannot edit or delete another recruiter's job.
- [ ] Register and log in as a seeker.
- [ ] Search and filter jobs.
- [ ] Submit an application with a valid resume.
- [ ] Confirm the seeker can see their applications.
- [ ] Confirm the recruiter can view applicants for their own jobs.
- [ ] Check profile updates, password change, and logout.
- [ ] Verify upload validation and responsive layouts.

## 🧠 Challenges & Learning Outcomes

This project is useful for practicing:

- Organizing views with Django's class-based and generic views.
- Designing user roles and permission checks.
- Modeling related data with `OneToOneField` and `ForeignKey`.
- Handling uploaded files and images.
- Building searchable and paginated list pages.
- Reducing unnecessary database queries with ORM relationship loading.
- Creating reusable templates with a shared base layout.

## 🛣️ Future Improvements

- Add email verification and password reset by email.
- Add application status tracking (Pending, Reviewed, Shortlisted, Rejected).
- Add recruiter dashboard analytics.
- Add advanced filters for salary, location, shift, and experience.
- Add duplicate-application prevention and stronger resume file validation.
- Add automated tests for permissions and core workflows.
- Add CI checks and production deployment documentation.
- Add a dedicated REST API if required by a frontend or mobile client.

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes.
4. Push the branch and open a pull request.

## 📄 License

No license has been specified yet. Add a `LICENSE` file and update this section before distributing the project under an open-source license.

---

<div align="center">

**Built with Django · Designed for learning and extensibility**

</div>
