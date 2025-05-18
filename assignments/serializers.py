from rest_framework import serializers
from .models import Assignment, Submission

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('id', 'course', 'title', 'description', 'due_date', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Submission
        fields = ('id', 'assignment', 'student', 'student_name', 'content', 'status', 
                  'feedback', 'submitted_at', 'reviewed_at')
        read_only_fields = ('student', 'submitted_at', 'reviewed_at', 'status')
    
    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"

class SubmissionReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'status', 'feedback', 'reviewed_at')
        read_only_fields = ('id', 'reviewed_at')