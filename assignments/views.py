from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, Enrollment
from accounts.permissions import IsAuthenticatedAndActive
from .models import Assignment, Submission
from .serializers import AssignmentSerializer, SubmissionSerializer, SubmissionReviewSerializer
from .permissions import (
    IsTeacher, IsStudent, IsCourseTeacher, IsAssignmentTeacher,
    IsEnrolledStudent, IsSubmissionOwner
)

class AssignmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticatedAndActive]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticatedAndActive, IsTeacher, IsCourseTeacher]
        return super().get_permissions()

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        # Check if user is teacher of the course or enrolled student
        course = Course.objects.get(pk=course_id)
        if course.instructor == self.request.user:
            return Assignment.objects.filter(course_id=course_id)
        elif self.request.user.is_student and Enrollment.objects.filter(student=self.request.user, course_id=course_id).exists():
            return Assignment.objects.filter(course_id=course_id)
        return Assignment.objects.none()

    def perform_create(self, serializer):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(pk=course_id)
        serializer.save(course=course)

class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
    permission_classes = [IsAuthenticatedAndActive]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticatedAndActive, IsTeacher, IsAssignmentTeacher]
        return super().get_permissions()

    def get_object(self):
        obj = super().get_object()
        # Check if user is teacher of the course or enrolled student
        if obj.course.instructor == self.request.user:
            return obj
        elif self.request.user.is_student and Enrollment.objects.filter(student=self.request.user, course=obj.course).exists():
            return obj
        self.permission_denied(self.request)

class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticatedAndActive, IsStudent, IsEnrolledStudent]

    def perform_create(self, serializer):
        assignment_id = self.kwargs['assignment_id']
        assignment = Assignment.objects.get(pk=assignment_id)
        
        # Check if student already submitted
        if Submission.objects.filter(student=self.request.user, assignment=assignment).exists():
            raise permissions.PermissionDenied("You have already submitted for this assignment.")
        
        serializer.save(student=self.request.user, assignment=assignment)

class SubmissionListView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticatedAndActive]

    def get_queryset(self):
        assignment_id = self.kwargs['assignment_id']
        assignment = Assignment.objects.get(pk=assignment_id)
        
        # Teachers see all submissions for their course assignments
        if assignment.course.instructor == self.request.user:
            return Submission.objects.filter(assignment_id=assignment_id)
        
        # Students see only their own submissions
        elif self.request.user.is_student:
            return Submission.objects.filter(
                assignment_id=assignment_id,
                student=self.request.user
            )
        
        return Submission.objects.none()

class SubmissionDetailView(generics.RetrieveAPIView):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()
    permission_classes = [IsAuthenticatedAndActive]

    def get_object(self):
        obj = super().get_object()
        # Teacher of the course or owner of the submission
        if obj.assignment.course.instructor == self.request.user or obj.student == self.request.user:
            return obj
        self.permission_denied(self.request)

class SubmissionReviewView(generics.UpdateAPIView):
    serializer_class = SubmissionReviewSerializer
    queryset = Submission.objects.all()
    permission_classes = [IsAuthenticatedAndActive, IsTeacher, IsAssignmentTeacher]

    def perform_update(self, serializer):
        serializer.save(status='reviewed', reviewed_at=timezone.now())