import logging
import random
import string
import traceback
from functools import wraps
from typing import Union, TypeVar

from django.conf import settings

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.contrib import messages
import phonenumbers
from django.utils import timezone
from django.utils.timezone import is_aware, make_aware

T = TypeVar("T")


def generate_code(length):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code


class AppLogger:
    # Configure logger once
    _logger = None

    @classmethod
    def _get_logger(cls):
        if cls._logger is None:
            cls._logger = logging.getLogger('app_logger')
            cls._logger.setLevel(logging.DEBUG)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_format = logging.Formatter('%(levelname)s - %(message)s')
            console_handler.setFormatter(console_format)

            # File handler for errors
            try:
                file_handler = logging.FileHandler('logs/errors.log')
                file_handler.setLevel(logging.ERROR)
                file_format = logging.Formatter(
                    '%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                file_handler.setFormatter(file_format)
                cls._logger.addHandler(file_handler)
            except FileNotFoundError:
                # If logs directory doesn't exist, just skip file logging
                pass

            cls._logger.addHandler(console_handler)

        return cls._logger

    @classmethod
    def report(cls, error, error_position=None):
        """
        Report an error with full traceback and optional context

        Args:
            error: Exception object or error message string
            error_position: Optional string describing where the error occurred
        """
        logger = cls._get_logger()

        # Build error message
        if error_position:
            message = f"[{error_position}] {str(error)}"
        else:
            message = str(error)

        # Log with traceback if it's an exception
        if isinstance(error, Exception):
            logger.error(message, exc_info=True)
        else:
            logger.error(message)
            # If we have a traceback in the current context, log it
            tb = traceback.format_exc()
            if tb and tb != 'NoneType: None\n':
                logger.error(f"Traceback:\n{tb}")

    @classmethod
    def info(cls, message):
        """Log informational message"""
        logger = cls._get_logger()
        logger.info(message)

    @classmethod
    def warning(cls, message):
        """Log warning message"""
        logger = cls._get_logger()
        logger.warning(message)

    @classmethod
    def debug(cls, message):
        """Log debug message"""
        logger = cls._get_logger()
        logger.debug(message)

    @staticmethod
    def print(*message):
        """Print to console (for debugging)"""
        print(*message)


class CustomPermissionRequired(PermissionRequiredMixin):
    def has_permission(self) -> bool:
        perms = self.get_permission_required()
        user = self.request.user

        if user.is_anonymous:
            return False

        if user.is_staff:
            return user.is_superuser or user.has_permission(perms)

        client = user.get_active_client()

        return client.has_permission(perms)


class CustomRequestUtil(CustomPermissionRequired):
    context: dict = None
    context_object_name = None
    template_name = None
    template_on_error = None
    extra_context_data: dict = None
    view_on_error = None

    def __init__(self, request):
        self.request = request
        self.permission_required = None


    @property
    def auth_user(self):
        user = self.request.user if self.request and self.request.user else None
        if isinstance(user, AnonymousUser):
            user = None

        return user


    def log_error(self, error):
        print(error)

    def make_error(self, message=None, error=None):
        if error:
            self.log_error(error)
        return message

    def process_request(self, request, target_view=None, errors=None, target_function=None, **extra_args):

        if not self.context:
            self.context = dict()


        self.context['request'] = request


        if self.permission_required:
            if not self.has_permission():
                response_raw_data = (None, "You do not have permission to perform this action.")
                return self.__handle_request_response(response_raw_data, target_view)

        if self.extra_context_data:
            for key, val in self.extra_context_data.items():
                self.context[key] = val

        if errors:
            self.context['form_errors'] = errors
            return render(request, self.template_on_error, self.context)

        response_raw_data = None

        if target_function:
            response_raw_data: Union[tuple, T] = target_function(**extra_args)

        return self.__handle_request_response(response_raw_data, target_view)

    def __handle_request_response(self, response_raw_data, target_view):
        response, error_detail = None, None

        if isinstance(response_raw_data, tuple):
            response, error_detail = response_raw_data
        else:
            response = response_raw_data

        if error_detail and not response:
            messages.error(self.request, error_detail)
            if self.template_on_error:
                return render(self.request, self.template_on_error, self.context)

            if self.view_on_error:
                return redirect(self.view_on_error)

        elif response and not error_detail:
            if isinstance(response, str):
                messages.success(self.request, response)
            else:
                self.context[self.context_object_name] = response

        elif response and error_detail:
            messages.error(self.request, error_detail)
            return redirect(response)


        if self.template_name:
            return render(self.request, self.template_name, self.context)

        if target_view:
            return redirect(target_view)

        return redirect('/')


    def generate_cache_key(self, instance_id=None, model=None, name=None):
        if model:
            if isinstance(model, str):
                model_name = model.lower()
            else:
                model_name = model._meta.model_name
        else:
            model_name = ""

        if instance_id:
            if isinstance(instance_id, str):
                instance_id = instance_id.lower()
            elif isinstance(instance_id, list):
                instance_id = "".join(map(str, instance_id))
            elif isinstance(instance_id, int):
                instance_id = str(instance_id)
        else:
            instance_id = ""

        if not name:
            name = ""

        return f"{model_name}:{instance_id}:{name}"

    def clear_temp_cache(self, instance_id=None, model=None, name=None):
        """Clear cache for a specific key."""
        key = self.generate_cache_key(instance_id, model, name)
        cache.delete(key)
        return key




def format_phone_number(phone_number, region_code=None):
    if not region_code:
        region_code = "NG"
    try:
        x = phonenumbers.parse(phone_number, region_code)
        phone_number = phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.E164)

        if phonenumbers.is_valid_number_for_region(x, region_code):
            return phone_number
    except:
        pass

    return None


def compare_password(input_password, hashed_password):
    return check_password(input_password, hashed_password)



def generate_otp():
    if settings.DEBUG:
        otp = "123456"
    else:
        otp = str(random.randint(1, 999999)).zfill(6)

    hashed_otp = make_password(otp)

    return otp, hashed_otp



def check_time_expired(time_to_check, duration=10) -> bool:
    """
    Returns True if the otp has expired and False if the otp is still valid.
    Returns True if the current time is greater than the time_to_check by the number of duration.
    """

    if not is_aware(time_to_check):
        time_to_check = make_aware(time_to_check)

    created_at = time_to_check
    current_time = timezone.now()

    time_difference = current_time - created_at
    time_difference_minutes = time_difference.total_seconds() / 60

    return time_difference_minutes > duration


def generate_random_username():
    # List of words to combine for the username
    adjectives = ["fast", "bright", "cool", "brave", "happy", "silent", "lucky"]
    nouns = ["lion", "tiger", "eagle", "panda", "shark", "falcon", "wolf"]

    # Choose a random adjective and noun
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)

    # Generate a random number
    number = random.randint(1, 999)

    # Combine the parts to form the username
    username = f"{adjective.capitalize()}{noun.capitalize()}{number}"

    return username
