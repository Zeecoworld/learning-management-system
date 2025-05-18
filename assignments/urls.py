from django.urls import path
from .views import (
    AssignmentListCreateView, AssignmentDetailView,
    SubmissionCreateView, SubmissionListView,
    SubmissionDetailView, SubmissionReviewView
)

urlpatterns = [
    # Assignment URLs
    path('courses/<int:course_id>/assignments/', AssignmentListCreateView.as_view(), name='assignment-list-create'),
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
    
    # Submission URLs
    path('assignments/<int:assignment_id>/submissions/', SubmissionListView.as_view(), name='submission-list'),
    path('assignments/<int:assignment_id>/submit/', SubmissionCreateView.as_view(), name='submission-create'),
    path('submissions/<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),
    path('submissions/<int:pk>/review/', SubmissionReviewView.as_view(), name='submission-review'),
]