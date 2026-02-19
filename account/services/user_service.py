from account.models import User
from utils.constants.messages import ResponseMessages, ErrorMessages
from utils.models import ModelService
from utils.util import CustomRequestUtil
from django.core.cache import cache
from django.db.models import Q

class UserService(CustomRequestUtil):
    def __init__(self, request):
        super().__init__(request)
        self.model_service = ModelService(self.request)

    def check_email_exists(self, email):
        user = User.available_objects.filter(Q(email__iexact=email))

        return user.exists(), user.first()

    def update(self, payload):
        model_service = ModelService(self.request)

        user = model_service.update_model_instance(model_instance=self.auth_user, **payload)

        return user


    def fetch_user_by_user_id(self, user_id):
        def __do_fetch_single():
            try:
                user = User.objects.get(user_id=user_id)
                return user, None

            except User.DoesNotExist:
                return None, ResponseMessages.user_not_found

            except Exception as e:
                # TODO: logger
                return None, ErrorMessages.something_went_wrong

        cache_key = self.generate_cache_key(instance_id=user_id, model=User)
        return cache.get_or_set(cache_key, __do_fetch_single)


    def fetch_user_by_user_email(self, email):
        def __do_fetch_single():
            try:
                user = User.objects.get(email=email)
                return user

            except User.DoesNotExist:
                raise NotFoundError(ResponseMessages.user_not_found)

            except Exception as e:
                raise ServerError(error=e, error_position="UserService.fetch_user_by_email")

        cache_key = self.generate_cache_key(instance_id=email, model=User)
        return cache.get_or_set(cache_key, __do_fetch_single)
