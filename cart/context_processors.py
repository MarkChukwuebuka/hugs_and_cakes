from cart.services import CartService


def cart(request):
    return {'cart': CartService(request)}