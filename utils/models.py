from utils.constants.messages import ErrorMessages
from utils.util import CustomRequestUtil, AppLogger


class ModelService(CustomRequestUtil):
    def __init__(self, request):
        super().__init__(request)

    def create_model_instance(self, model=None, payload=None):
        """Creates a model instance of the model passed using the payload data"""
        if payload is None:
            payload = {}

        try:
            if model is None:
                error = "Invalid model instance"
                AppLogger.report(error=error, error_position=f"ModelService.create_model_instance - {model}")
                return None, ErrorMessages.something_went_wrong
            has_created_by_attr = hasattr(model, "created_by")

            if isinstance(payload, list):
                
                payload_list = []
                for data in payload:
                    if has_created_by_attr:
                        data["created_by"] = self.auth_user
                    payload_list.append(model(**data))
                
                main_object = model.objects.bulk_create(payload_list, ignore_conflicts=True)
                
                return main_object, None
            else:
                if has_created_by_attr:
                    payload["created_by"] = self.auth_user
                main_object = model.objects.create(**payload)

            main_object.save()

            return main_object, None

        except Exception as e:
            AppLogger.report(error=e, error_position=f"ModelService.create_model_instance - {model}")
            return None, ErrorMessages.something_went_wrong


    def update_model_instance(self, model_instance=None, **kwargs):
        try:
            if model_instance is None:
                AppLogger.report(error="Invalid model instance", error_position=f"ModelService.update_model_instance - {model_instance}")
                return None, ErrorMessages.something_went_wrong

            base_model_attributes = ["updated_by", "updated_at"]
            update_fields = []

            for attr in base_model_attributes:
                if hasattr(model_instance, attr):
                    if attr == "updated_at":
                        update_fields.append(attr)
                    elif attr == "updated_by":
                        kwargs[attr] = self.auth_user

            for field, value in kwargs.items():
                setattr(model_instance, field, value)
                update_fields.append(field)

            model_instance.save(update_fields=update_fields)

            self.clear_temp_cache(instance_id=model_instance.id, model=model_instance.model_name())

            return model_instance

        except Exception as e:
            AppLogger.report(error=e, error_position=f"ModelService.update_model_instance- {model_instance}")
            return None, ErrorMessages.something_went_wrong
