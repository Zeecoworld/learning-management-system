from rest_framework.permissions import BasePermission

class IsCourseInstructor(BasePermission):
    """
    Check if the user is instructor of the course
    """
    def has_object_permission(self, request, view, obj):
        return obj.instructor == request.user

class IsStudentOrInstructor(BasePermission):
    """
    Check if the user is a student or instructor
    """
    def has_permission(self, request, view):
        return request.user.is_student or request.user.is_teacher