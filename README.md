# Learning Management System API

A comprehensive API for managing educational institutions with features for students, teachers, and administrators.

![LMS Dashboard](https://via.placeholder.com/800x400?text=LMS+Dashboard)

## 🌟 Features

- **User Management**
  - Role-based authentication (Admin, Teacher, Student)
  - User profiles with role-specific fields
  - Secure password management

- **Course Management**
  - Create and manage courses
  - Course enrollment system
  - Detailed course information

- **Assignment System**
  - Create and manage assignments
  - Assignment submission handling
  - Grading and feedback functionality

## 📋 API Documentation

The LMS API provides a RESTful interface with the following main endpoints:

### Authentication & User Management
- Register new users
- Login/logout functionality
- Password management
- User profile management

### Course Management
- Create courses
- List all courses
- Manage course details
- Course enrollment

### Assignment Management
- Create assignments for courses
- Submit assignments (students)
- Review assignments (teachers)
- Grade and provide feedback

## 🛠️ Technology Stack

- **Backend**: Django with Django REST Framework
- **Authentication**: Token-based authentication
- **API Specification**: OpenAPI 3.0.3

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/lms-api.git
cd lms-api
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up the database
```bash
python manage.py migrate
```

5. Create a superuser (admin)
```bash
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## 📚 API Usage Examples

### Registration

```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "securepassword",
    "password2": "securepassword",
    "first_name": "John",
    "last_name": "Doe",
    "role": "STUDENT"
  }'
```

### Creating a Course (Teacher)

```bash
curl -X POST http://localhost:8000/api/courses/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -d '{
    "title": "Introduction to Computer Science",
    "description": "A beginner-friendly course covering the basics of computer science",
    "instructor": 1
  }'
```

### Submitting an Assignment (Student)

```bash
curl -X POST http://localhost:8000/api/assignments/assignments/1/submit/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -d '{
    "assignment": 1,
    "content": "This is my assignment submission"
  }'
```

## 📝 API Schema

The full API schema is available at `/api/schema/` endpoint when the server is running. You can view it in:
- JSON format: `/api/schema/?format=json`
- YAML format: `/api/schema/?format=yaml`

## 🔒 Authentication

The API uses token-based authentication. To obtain a token:

1. Login with valid credentials at `/api/accounts/login/`
2. Use the received token in the Authorization header for subsequent requests:
   `Authorization: Token YOUR_AUTH_TOKEN`



## 👨‍💻 Author

Isaac Yakubu - [GitHub Profile](https://github.com/isaacyakubu)

## 🙏 Acknowledgments

- Django REST Framework for the powerful API toolkit
- All contributors who participate in this project
