
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from cart.services import CartService
from utils.util import CustomRequestUtil


@csrf_exempt
def add_to_cart(request):
    cart_service = CartService(request)

    if request.method == "POST":
        data = json.loads(request.body)
        menu_item_id = int(data.get("menu_item_id"))
        menu_item_qty = int(data.get("menu_item_qty", 1))

        res, _ = cart_service.add(menu_item_id, menu_item_qty)

        cart = request.session.get("cart")
        cart_count = len(cart) if cart else 0

        return JsonResponse({
            "success": True,
            "message": res,
            "cart_count": cart_count
        })

    return None


@csrf_exempt
def update_cart(request):
    cart_service = CartService(request)

    if request.method == 'POST':
        data = json.loads(request.body)
        menu_item_id = data.get("menu_item_id")
        quantity = data.get("menu_item_qty")

        res, _ = cart_service.add(menu_item_id, quantity, True)


        return JsonResponse({
            "success": True,
            "message": res
        })

    return None


@csrf_exempt
def remove_from_cart(request):
    cart_service = CartService(request)

    if request.method == "POST":
        data = json.loads(request.body)
        menu_item_id = data.get("menu_item_id")

        res, _ = cart_service.remove(menu_item_id)

        cart = request.session.get("cart")
        cart_count = len(cart) if cart else 0

        return JsonResponse({
            "success": True,
            "message": res,
            "cart_count": cart_count
        })

    return None



class CartView(View, CustomRequestUtil):
    template_name = 'cart.html'
    template_on_error = 'cart.html'

    def get(self, request, *args, **kwargs):
        self.context_object_name = "cart"
        cart_service = CartService(request)
        return self.process_request(request, target_function=cart_service.fetch_cart)


    def post(self, request, *args, **kwargs):
        cart_service = CartService(request)
        return self.process_request(
            request, target_function=cart_service.add_to_cart, item_id=item_id
        )

# def cart_view(request):
#     cart = request.session.get("cart", {})
#     items = []
#     total = 0
#
#     for item_id, data in cart.items():
#         item = MenuItem.objects.get(id=item_id)
#         quantity = data["quantity"]
#         subtotal = item.base_price * quantity
#
#         items.append({
#             "item": item,
#             "quantity": quantity,
#             "subtotal": subtotal,
#         })
#
#         total += subtotal
#
#     return render(request, "cart.html", {
#         "cart_items": items,
#         "total": total,
#     })