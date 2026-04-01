from django.shortcuts import render
from django.views import View

from crm.models import Table
from crm.services.category_service import CategoryService
from crm.services.menu_item_service import MenuItemService
from crm.services.table_service import TableService
from order.constants import OrderType
from utils.constants.messages import ErrorMessages
from utils.util import CustomRequestUtil



class HomeView(View, CustomRequestUtil):
    template_name = 'index.html'
    extra_context_data = {
        "title": "Welcome",
    }

    def get(self, request, *args, **kwargs):
        category_service = CategoryService(request)
        self.extra_context_data["categories"] = category_service.fetch_list()
        return self.process_request(request)


class AboutView(View, CustomRequestUtil):
    template_name = 'about-us.html'
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
    context_object_name = 'page_obj'
    extra_context_data = {
        "title": "Menu",
    }

    def get(self, request, *args, **kwargs):
        menu_item_service = MenuItemService(request)
        category_service = CategoryService(request)
        table_service = TableService(request)

        category_slug = request.GET.get("category")
        table_token = request.GET.get("token")

        error = None
        if table_token:
            table = Table.active_available_objects.filter(qr_token=table_token, is_active=True).first()
            if table:
                request.session["table_id"] = table.id
                request.session["order_type"] = OrderType.dine_in
            else:
                error = ErrorMessages.invalid_qr_code

        self.extra_context_data["categories"] = category_service.fetch_list()
        self.extra_context_data["selected_category"] = category_service.fetch_single_by_code(category_slug)

        return self.process_request(
            request, target_function=menu_item_service.fetch_list, errors=error, category_slug=category_slug, paginate=True
        )




def page_not_found(request, exception):
    return render(request, 'error-404.html', {'title':'Page Not Found'}, status=404)

def server_error(request):
    return render(request, 'error-500.html', {'title':'Server Error'}, status=404)


