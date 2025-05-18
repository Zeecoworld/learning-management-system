from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from accounts.permissions import IsAuthenticatedAndActive
from .permissions import IsCourseInstructor, IsStudentOrInstructor
from assignments.permissions import IsTeacher, IsStudent

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from accounts.permissions import IsAuthenticatedAndActive
from .permissions import IsCourseInstructor, IsStudentOrInstructor
from assignments.permissions import IsTeacher, IsStudent # changed the import


class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedAndActive]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticatedAndActive, IsTeacher]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedAndActive]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticatedAndActive, IsTeacher, IsCourseInstructor]
        return super().get_permissions()

class EnrollmentCreateView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticatedAndActive, IsStudent] #changed permission

    def perform_create(self, serializer):
        course = Course.objects.get(pk=self.kwargs['course_id'])
        if Enrollment.objects.filter(student=self.request.user, course=course).exists():
            raise permissions.PermissionDenied("You are already enrolled in this course.")
        serializer.save(student=self.request.user, course=course)

class EnrollmentListView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticatedAndActive, IsCourseInstructor]
 
    def get_queryset(self):
        user = self.request.user
        if user.role == 'STUDENT':
            # Students can see their own enrollments
            return Enrollment.objects.filter(student=user)
        elif user.role == 'TEACHER':
            # Teachers can see enrollments for *their* courses.  This is the key fix.
            return Enrollment.objects.filter(course__instructor=user)
        return Enrollment.objects.none()
