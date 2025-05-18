from rest_framework.permissions import BasePermission
from courses.models import Course, Enrollment
from .models import Assignment, Submission

class IsTeacher(BasePermission):
    """
    Permission check for teacher role
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_teacher

class IsStudent(BasePermission):
    """
    Permission check for student role
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_student

class IsCourseTeacher(BasePermission):
    """
    Check if the user is the teacher of the course
    """
    def has_permission(self, request, view):
        course_id = view.kwargs.get('course_id')
        if not course_id:
            return False
        
        try:
            course = Course.objects.get(pk=course_id)
            return course.instructor == request.user
        except Course.DoesNotExist:
            return False

class IsAssignmentTeacher(BasePermission):
    """
    Check if the user is the teacher of the assignment's course
    """
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Assignment):
            return obj.course.instructor == request.user
        elif isinstance(obj, Submission):
            return obj.assignment.course.instructor == request.user
        return False

class IsEnrolledStudent(BasePermission):
    """
    Check if the student is enrolled in the course
    """
    def has_permission(self, request, view):
        course_id = view.kwargs.get('course_id')
        if not course_id:
            return False
        
        try:
            return Enrollment.objects.filter(
                student=request.user,
                course_id=course_id
            ).exists()
        except Exception:
            return False

class IsSubmissionOwner(BasePermission):
    """
    Check if the user is the owner of the submission
    """
    def has_object_permission(self, request, view, obj):
        return obj.student == request.user