from django.core.cache import cache
from django.db.models import Q

from crm.models import Category
from utils.constants.messages import ResponseMessages, ErrorMessages
from utils.models import ModelService
from utils.util import CustomRequestUtil, make_slug


class CategoryService(CustomRequestUtil):

    def __init__(self, request):
        super().__init__(request)
        self.model_service = ModelService(request)
        self.model = Category

    def create_single(self, payload):

        name = payload.get("name")
        cover_image = payload.get("cover_image")
        code = make_slug(name)

        category, is_created = Category.objects.get_or_create(
            name__iexact=name,
            defaults=dict(
                code=code,
                cover_image=cover_image,
            )
        )

        if not is_created:
            return None, self.make_error(ErrorMessages.category_already_exists)

        return ResponseMessages.category_created_successfully, None

    def fetch_list(self, filter_params=None):
        q = Q()

        return self.__get_base_query().filter(q)

    def __get_base_query(self):
        qs = Category.available_objects.all()
        return qs


    def fetch_single_by_code(self, category_code):
        def __handle_fetch():
            category = self.__get_base_query().filter(code=category_code).first()
            if not category:
                return None, self.make_error(ErrorMessages.category_not_found)

            return category, None
        cache_key = self.generate_cache_key(instance_id=category_code, model=self.model)
        return cache.get_or_set(cache_key, __handle_fetch)


    def update_single(self, payload, category_code):
        category, error = self.fetch_single_by_code(category_code)
        if not category:
            return category, error

        name = payload.get("name")
        if name:
            existing_category = self.__get_base_query().filter(
                name__iexact=name
            ).exclude(id=category.id).exists()

            if existing_category:
                return None, self.make_error(ErrorMessages.category_already_exists)

        category.name = payload.get("name", category.name)
        category.code = make_slug(name)
        category.cover_image = payload.get("cover_image", category.cover_image)
        category.save(update_fields=["code", "cover_image", "name"])

        self.clear_temp_cache(instance_id=category_code, model=self.model)
        return ResponseMessages.category_updated_successfully, None




