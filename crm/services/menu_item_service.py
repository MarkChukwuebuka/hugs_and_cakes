from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q

from crm.models import Category, MenuItem
from utils.constants.messages import ResponseMessages, ErrorMessages
from utils.models import ModelService
from utils.util import CustomRequestUtil


class MenuItemService(CustomRequestUtil):

    def __init__(self, request):
        super().__init__(request)
        self.model = MenuItem

    def create_single(self, payload):

        name = payload.get("name")

        menu_item, is_created = self.__get_base_query().objects.get_or_create(
            name__iexact=name,
            defaults=dict(
                description=payload.get("description"),
                base_price=payload.get("base_price"),
                image=payload.get("image"),
                is_available=payload.get("is_available"),
                is_dine_in_available=payload.get("is_dine_in_available"),
                is_delivery_available=payload.get("is_delivery_available"),
                preparation_time=payload.get("preparation_time"),
            )
        )

        if not is_created:
            return None, self.make_error(ErrorMessages.menu_item_already_exists)

        return ResponseMessages.menu_item_created_successfully, None

    def fetch_list(self, category_slug=None, paginate=False):
        q = Q()
        if category_slug:
            q &= Q(category__code__iexact=category_slug)

        items = self.__get_base_query().filter(q)

        if paginate:
            paginator = Paginator(items, 8)

            # get the current page number from request
            page_number = self.request.GET.get("page", 1)
            page_obj = paginator.get_page(page_number)

            return page_obj


        return items

    def __get_base_query(self):
        qs = MenuItem.available_objects.select_related("category")
        return qs


    def fetch_single_by_slug(self, menu_item_slug):
        def __handle_fetch():
            menu_item = self.__get_base_query().filter(slug=menu_item_slug).first()
            if not menu_item:
                return None, self.make_error(ErrorMessages.menu_item_not_found)

            return menu_item, None
        cache_key = self.generate_cache_key(instance_id=menu_item_slug, model=self.model)
        return cache.get_or_set(cache_key, __handle_fetch)


    def fetch_single_by_id(self, menu_item_id):
        def __handle_fetch():
            menu_item = self.__get_base_query().filter(id=menu_item_id).first()
            if not menu_item:
                return None, self.make_error(ErrorMessages.menu_item_not_found)

            return menu_item, None
        cache_key = self.generate_cache_key(instance_id=menu_item_id, model=self.model)
        return cache.get_or_set(cache_key, __handle_fetch)


    def update_single(self, payload, menu_item_slug):
        menu_item, error = self.fetch_single_by_id(menu_item_slug)
        if not menu_item:
            return menu_item, error

        name = payload.get("name")
        if name:
            existing_menu_item = self.__get_base_query().filter(
                name__iexact=name
            ).exclude(id=menu_item.id).exists()

            if existing_menu_item:
                return None, self.make_error(ErrorMessages.menu_item_with_that_name_already_exists)

        menu_item.name = payload.get("name", menu_item.name)
        menu_item.description = payload.get("description", menu_item.description)
        menu_item.base_price = payload.get("base_price", menu_item.base_price)
        menu_item.is_available = payload.get("is_available", menu_item.is_available)
        menu_item.preparation_time = payload.get("preparation_time", menu_item.preparation_time)
        menu_item.is_dine_in_available = payload.get("is_dine_in_available", menu_item.is_dine_in_available)
        menu_item.is_delivery_available = payload.get("is_delivery_available", menu_item.is_delivery_available)
        menu_item.code = self.make_menu_item_slug(name)
        menu_item.image = payload.get("image", menu_item.image)
        menu_item.save()

        self.clear_temp_cache(instance_id=menu_item_slug, model=self.model)
        return ResponseMessages.menu_item_updated_successfully, None








