from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.core.cache import cache
from django.utils import timezone

from account.constants import OTPIntent
from account.models import User, Otp
from account.services.user_service import UserService
from utils.constants.messages import ResponseMessages, ErrorMessages
from utils.models import ModelService
from utils.util import CustomRequestUtil, generate_otp, check_time_expired


class AuthService(CustomRequestUtil):
    def __init__(self, request):
        super().__init__(request)
        self.model_service = ModelService(request)
        self.user_service = UserService(request)


    def resend_verification_otp(self, payload):
        email = payload.get("email")

        user_service = UserService(self.request)
        user_exists, user = user_service.check_email_exists(email=email)

        if user_exists:
            _ = self.send_signup_otp(user)

        return {"email": email}


    def verify_signup_otp(self, payload):
        return self.verify_otp_via_email(payload, otp_intent=OTPIntent.signup)

    def send_signup_otp(self, user):
        otp_service = OTPService(self.request)
        otp = otp_service.get_or_set_user_otp(user)
        self.request.session["email"] = user.email

        # Send OTP to Email
        # _ = send_signup_otp.delay(email=user.email, otp=otp, first_name=user.first_name)

        return ResponseMessages.otp_sent_to_email, None

    def change_password(self, payload):
        self.auth_user.password = payload.get("password")
        self.auth_user.save(update_fields=["password"])

        return ResponseMessages.successful_password_change

    def reset_password(self, payload):
        email = payload.get("email")
        password = payload.get("password")

        user_exists, user = self.user_service.check_email_exists(email)

        if user_exists:
            if not user.can_reset_password:
                return None, ErrorMessages.access_denied

            user.password = password
            user.can_reset_password = False
            user.save(update_fields=["password", "can_reset_password"])

            return ResponseMessages.successful_password_change, None

        return None, ResponseMessages.user_not_recognized

    def forgot_password(self, payload):
        email = payload.get("email")

        user_exists, user = self.user_service.check_email_exists(email)

        if user_exists:
            otp_service = OTPService(self.request)
            otp = otp_service.get_or_set_user_otp(user)

            # _ = send_password_reset.delay(email=email, first_name=user.first_name, otp=otp)

        return ResponseMessages.reset_password_email_sent, None

    def verify_otp_via_email(self, payload, otp_intent=None):
        """
        :param otp_intent: used to determine what happens after verifying otp
        :param payload: {
            otp: 4-digit code,
            email: "email@emaildomain.com"
        }
        :return: User or Message
        """
        otp = payload.get("otp")
        email = self.request.session.get("email")

        user_exists, user = self.user_service.check_email_exists(email)

        if user_exists and hasattr(user, "otp"):
            otp_service = OTPService(self.request)

            if otp_service.verify_otp(user, otp):
                if otp_intent == OTPIntent.reset_password:
                    user.can_reset_password = True
                    user.save(update_fields=["can_reset_password"])
                    return ResponseMessages.valid_otp, None

                elif otp_intent == OTPIntent.signup:
                    user.is_verified = True
                    user.save(update_fields=["is_verified"])
                    login(self.request, user)

                return user

            return None, ResponseMessages.invalid_or_expired_otp

        return None, ResponseMessages.user_not_recognized

    def verify_password_otp(self, payload):
        return self.verify_otp_via_email(payload, otp_intent=OTPIntent.reset_password)

    def login(self, payload):
        username = payload.get("email").lower()
        password = payload.get("password")

        user_exists, user = self.user_service.check_email_exists(username)

        if user and not user.is_active:
            return None, ErrorMessages.inactive_account

        authenticate_kwargs = {"username": username, "password": password}

        login_count_cache_key = self.generate_cache_key("login_count", username)

        login_count = cache.get(key=login_count_cache_key)

        if login_count and login_count >= 5:
            return None, ResponseMessages.too_many_attempts_account_blocked

        user = authenticate(**authenticate_kwargs)

        if user is None:
            login_count = 1 if login_count is None else login_count + 1
            cache.set(login_count_cache_key, login_count, timeout=1200)

            return None, ResponseMessages.invalid_credentials


        return user, None


    def logout(self):
        pass

    def register(self, payload):

        model_service = ModelService(self.request)
        user = model_service.create_model_instance(model=User, payload=payload)

        return self.send_signup_otp(user)







class OTPService(CustomRequestUtil):
    def __init__(self, request):
        super().__init__(request)

    def create(self, data):
        model_service = ModelService(self.request)

        _ = model_service.create_model_instance(model=Otp, payload=data)

        return True

    def get_or_set_user_otp(self, user):
        """Creates the OTP one-to-one relationship for the user if not existing or creates a new OTP and attaches it
        to the already existing relationship"""
        otp, hashed_otp = generate_otp()

        data = {"user": user, "otp": hashed_otp, "otp_requested_at": timezone.now()}

        if not hasattr(user, "otp"):
            _ = self.create(data)

        else:
            _ = self.update_user_otp(user, hashed_otp)

        return otp

    def update_user_otp(self, user, hashed_otp):
        user_otp = user.otp
        user_otp.otp = hashed_otp
        user_otp.trials = 0
        user_otp.otp_requested_at = timezone.now()
        user_otp.otp_verified_at = None
        user_otp.is_otp_verified = False
        user_otp.save(update_fields=["otp", "otp_requested_at", "trials", "is_otp_verified", "otp_verified_at"])

        return True

    def verify_otp(self, user, incoming_otp):
        user_otp = user.otp

        if user_otp.trials >= 3:
            return None, ResponseMessages.too_many_failed_otp_verification_attempts

        if user_otp.is_otp_verified:
            return None, ResponseMessages.invalid_or_expired_otp

        otp_requested_at = user_otp.otp_requested_at
        hashed_otp = user_otp.otp

        if check_password(incoming_otp, hashed_otp) and not check_time_expired(otp_requested_at):
            user_otp.is_otp_verified = True
            user_otp.otp_verified_at = timezone.now()
            user_otp.save(update_fields=["is_otp_verified", "otp_verified_at"])

            return True

        user_otp.trials += 1
        user_otp.save(update_fields=["trials"])

        return False
