from django.urls import path
from . views import *


urlpatterns = [
  path("signup/", SignupView.as_view()),
  path("profile", GetUserView.as_view()),
  path("user/update/", UpdateUserProfile.as_view()),
  path('verify/email/', VerifyEmailView.as_view(), name='verify-email'),
   path('setpassword/<uid>/<token>/', SetNewPasswordView.as_view(), name='set-new-password'),
]