from django.urls import path

from account.views import UserLoginView, ForgotPasswordView, SignupView, VerifyOTPView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
]