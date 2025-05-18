from django.contrib import admin
from .models import Assignment, Submission

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'created_at')
    list_filter = ('course', 'due_date')
    search_fields = ('title', 'description', 'course__title')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'status', 'submitted_at', 'reviewed_at')
    list_filter = ('status', 'submitted_at', 'reviewed_at', 'assignment')
    search_fields = ('student__email', 'assignment__title', 'content')