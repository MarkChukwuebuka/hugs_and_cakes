from django.views import View

from crm.services.category_service import CategoryService
from crm.services.menu_item_service import MenuItemService
from utils.util import CustomRequestUtil



class HomeView(View, CustomRequestUtil):
    template_name = 'index.html'
    extra_context_data = {
        "title": "Welcome",
    }

    def get(self, request, *args, **kwargs):
        return self.process_request(request)


class AboutView(View, CustomRequestUtil):
    template_name = 'about.html'
    extra_context_data = {
        "title": "About Us",
    }

    def get(self, request, *args, **kwargs):
        return self.process_request(request)


class ContactUsView(View, CustomRequestUtil):
    template_name = 'contact-us.html'
    extra_context_data = {
        "title": "Contact Us",
    }

    def get(self, request, *args, **kwargs):
        return self.process_request(request)




class CategoryView(View, CustomRequestUtil):
    template_name = 'category.html'
    template_on_error = 'category.html'
    context_object_name = "categories"
    extra_context_data = {
        "title": "Categories",
    }

    def get(self, request, *args, **kwargs):
        category_service = CategoryService(request)
        return self.process_request(request, target_function=category_service.fetch_list)


class MenuView(View, CustomRequestUtil):
    template_name = 'menu.html'
    template_on_error = 'menu.html'
    context_object_name = 'menu_items'
    extra_context_data = {
        "title": "Menu",
    }

    def get(self, request, *args, **kwargs):
        menu_item_service = MenuItemService(request)
        return self.process_request(request, target_function=menu_item_service.fetch_list)
