from django.views import View

from account.constants import OTPIntent
from account.services.auth_service import AuthService
from utils.util import CustomRequestUtil




class UserLoginView(View, CustomRequestUtil):
    template_name = 'login.html'
    extra_context_data = {
        "title": "Sign In",
    }

    def get(self, request, *args, **kwargs):
        return self.process_request(request)

    def post(self, request, *args, **kwargs):
        auth_service = AuthService(self.request)

        self.template_name = None
        self.template_on_error = 'login.html'

        payload = {
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
        }

        next_url = request.POST.get('next', request.GET.get('next', '/'))
        request.session["otp_type"] = OTPIntent.signup

        return self.process_request(
            request, target_view=next_url, target_function=auth_service.login, payload=payload
        )


class SignupView(View, CustomRequestUtil):
    template_name = 'signup.html'
    template_on_error = 'signup.html'
    extra_context_data = {
        "title": "Sign Up",
    }

    def get(self, request, *args, **kwargs):
        return self.process_request(request)

    def post(self, request, *args, **kwargs):
        auth_service = AuthService(self.request)
        self.template_name = None

        payload = {
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'first_name': request.POST.get('firstName'),
            'last_name': request.POST.get('lastName')
        }

        return self.process_request(
            request, target_view="verify-otp", target_function=auth_service.register, payload=payload
        )

class VerifyOTPView(View, CustomRequestUtil):
    template_name = 'verify-otp.html'
    template_on_error = 'verify-otp.html'
    extra_context_data = {
        "title": "Verify OTP",
    }

    def get(self, request, *args, **kwargs):
        return self.process_request(request)

    def post(self, request, *args, **kwargs):
        auth_service = AuthService(self.request)
        self.template_name = None

        payload = {
            'otp': request.POST.get('otp')
        }

        return self.process_request(
            request, target_view="home", target_function=auth_service.verify_signup_otp, payload=payload
        )


class ForgotPasswordView(View, CustomRequestUtil):
    template_name = 'forgot-password.html'
    template_on_error = 'forgot-password.html'

    extra_context_data = {
        "title": "Forgot Password",
    }

    def get(self, request, *args, **kwargs):
        return self.process_request(request)

    def post(self, request, *args, **kwargs):
        auth_service = AuthService(self.request)
        self.template_name = None

        payload = {
            'email': request.POST.get('email')
        }

        return self.process_request(
            request, target_view="verify-otp", target_function=auth_service.forgot_password, payload=payload
        )
