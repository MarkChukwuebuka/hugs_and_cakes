
from django.views import View

from order.models import Area
from order.services.order_service import OrderService
from utils.util import CustomRequestUtil


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
        print(request.session["order_type"])
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
        return self.process_request(request, target_view="home", target_function=order_service.create_single, payload=payload)





