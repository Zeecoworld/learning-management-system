from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

import random
import string

def generate_token(length=64):
    """Generate a random token."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Create the appropriate profile when a user is created."""
    if created:
        if instance.role == 'TEACHER':
            TeacherProfile.objects.create(user=instance)
        elif instance.role == 'STUDENT':
            StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """Save the appropriate profile when a user is saved."""
    if instance.role == 'TEACHER' and hasattr(instance, 'teacher_profile'):
        instance.teacher_profile.save()
    elif instance.role == 'STUDENT' and hasattr(instance, 'student_profile'):
        instance.student_profile.save()