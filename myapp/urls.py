from django.urls import path
from myapp.views import UserRegistrationView, UserLoginView, UserProfileView, UserchangePassword, SendPasswordResetMailView, UserResetPasswordView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name='login'),
    path("profile/", UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserchangePassword.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetMailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserResetPasswordView.as_view(), name='reset-password')
]
