from django.urls import path
from .views import RegistrationView, LoginView, ActivationView, LogoutView, ChangePasswordView, ForgotPasswordView, RebuildForgottenPasswordView


urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/',ChangePasswordView.as_view()),
    path('pass_forgot/', ForgotPasswordView.as_view()),
    path('inst-forgotten-pass/', RebuildForgottenPasswordView.as_view()),
]

