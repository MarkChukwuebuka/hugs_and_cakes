
import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
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

        get_cart = request.session.get("cart")
        cart_count = len(get_cart) if get_cart else 0

        return JsonResponse({
            "success": True,
            "message": res,
            "cart_count": cart_count
        })

    return None



def cart(request):

    if not request.session.get("cart"):
        messages.error(request, "There are no items in your cart")
        return redirect("home")
    # print(request.session["order_type"])
    context = {
        "title": "Cart",
        "order_type": request.session.get("order_type")
    }
    return render(request, 'cart.html', context)
