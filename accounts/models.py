from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of username.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

    def teachers(self):
        """Return queryset of all teacher users"""
        return self.filter(role='TEACHER')

    def students(self):
        """Return queryset of all student users"""
        return self.filter(role='STUDENT')


class CustomUser(AbstractUser):
    """
    Custom User model with email as the unique identifier and additional fields
    for both teachers and students.
    """
    # Role choices
    ROLE_CHOICES = (
        ('ADMIN', 'Administrator'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    )

    # Common fields for all users
    username = None  # Remove username field
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    # Contact information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Teacher-specific fields
    employee_id = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    
    # Student-specific fields
    student_id = models.CharField(max_length=20, blank=True, null=True)
    enrollment_date = models.DateField(blank=True, null=True)
    graduation_date = models.DateField(blank=True, null=True)
    major = models.CharField(max_length=100, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        """
        Override save method to ensure role-specific fields are properly handled.
        """
        # Set specific fields to None based on the role
        if self.role == 'STUDENT':
            self.employee_id = None
            self.department = None
            self.hire_date = None
            self.qualification = None
        elif self.role == 'TEACHER':
            self.student_id = None
            self.enrollment_date = None
            self.graduation_date = None
            self.major = None
        
        super().save(*args, **kwargs)
    
    def is_teacher(self):
        """Check if user is a teacher."""
        return self.role == 'TEACHER'
    
    def is_student(self):
        """Check if user is a student."""
        return self.role == 'STUDENT'
    
    def is_admin(self):
        """Check if user is an admin."""
        return self.role == 'ADMIN'
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['email']


# Related models that extend the user functionality
class TeacherProfile(models.Model):
    """Extended profile information for teachers."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    specializations = models.TextField(blank=True, null=True)
    office_location = models.CharField(max_length=100, blank=True, null=True)
    office_hours = models.TextField(blank=True, null=True)
    research_interests = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Teacher Profile: {self.user.email}"


class StudentProfile(models.Model):
    """Extended profile information for students."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    gpa = models.FloatField(blank=True, null=True)
    advisor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='advised_students', limit_choices_to={'role': 'TEACHER'})
    program = models.CharField(max_length=100, blank=True, null=True)
    year_level = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"Student Profile: {self.user.email}"