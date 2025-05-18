from django.urls import path
from .views import RegisterView, login_view, ChangePasswordView, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
]
