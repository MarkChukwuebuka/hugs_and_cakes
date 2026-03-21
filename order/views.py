from django.shortcuts import render
from django.views import View

from cart.services import CartService
from crm.models import Table, MenuItem
from order.constants import OrderType, OrderStatus
from order.models import Area, DeliveryAddress, Order, OrderItem
from order.services.order_service import OrderService
from utils.util import CustomRequestUtil, generate_order_ref


# Create your views here.

class CheckoutView(View, CustomRequestUtil):
    template_name = 'checkout.html'
    template_on_error = 'checkout.html'
    context_object_name = "categories"
    extra_context_data = {
        "title": "Checkout",
    }

    def get(self, request, *args, **kwargs):
        self.extra_context_data["order_type"] = request.session.get("order_type")
        self.extra_context_data["areas"] = Area.objects.all()
        return self.process_request(request)

    def post(self, request, *args, **kwargs):

        payload = dict(
            first_name = request.POST.get("first_name"),
            last_name = request.POST.get("last_name"),
            email = request.POST.get("email"),
            area_id = request.POST.get("area"),
            address = request.POST.get("address"),
            phone_number = request.POST.get("phone_number"),
            notes = request.POST.get("order_notes")
        )
        order_service = OrderService(request)
        return self.process_request(request, target_function=order_service.create_single, payload=payload)





