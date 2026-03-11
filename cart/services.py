from django.conf import settings

from crm.services.menu_item_service import MenuItemService
from utils.util import CustomRequestUtil


class CartService(CustomRequestUtil):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        self.request = request
        self.menu_item_service = MenuItemService(request)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart
        # It first checks if there's an existing cart in the session.
        #  If not, it creates an empty cart in the session.
        # The cart is stored in the self.cart attribute for further use.

    def __iter__(self):
        menu_item_ids = self.cart.keys()
        menu_items = self.menu_item_service.__get_base_query().filter(id__in=menu_item_ids)

        for menu_item in menu_items:
            item = self.cart[str(menu_item.id)].copy()
            item['menu_item'] = menu_item

            if menu_item.percentage_discount:
                item['total_price'] = int(menu_item.discounted_price * item['quantity'])
            else:
                item['total_price'] = int(menu_item.price * item['quantity'])

            yield item


    def __len__(self):
        return len(self.cart)
        # This method returns the total number of items in the cart.

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        #  This method saves the cart back to the user's session after making changes.

    def add(self, menu_item_id, quantity, update_quantity=False):
        # This method is used to add menu_items to the cart.
        menu_item_id = str(menu_item_id)
        message = ""

        if menu_item_id not in self.cart:
            self.cart[menu_item_id] = {'quantity': quantity, 'id': menu_item_id}
            message = "Item has been added to cart"

        if update_quantity:
            self.cart[menu_item_id]['quantity'] = int(quantity)
            message = "Cart has been updated"

            if self.cart[menu_item_id]['quantity'] == 0:
                self.remove(menu_item_id)
                message = "Item has been removed from cart"

        self.save()

        return message, None

    def remove(self, menu_item_id):
        menu_item_id = str(menu_item_id)  # Ensure data type compatibility
        if menu_item_id in self.cart:
            del self.cart[menu_item_id]
            self.save()  # Ensure cart data is saved to the session
        message = "Item was removed from cart"
        return message, None

        #  This method removes a menu_item from the cart based on its menu_item_id.

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
        # This method clears the entire cart by deleting it from the session.

    def get_total_cost(self):
        total = 0
        menu_item_ids = self.cart.keys()
        menu_items = self.menu_item_service.__get_base_query().filter(id__in=menu_item_ids)

        for value in self.cart.values():
            key = int(value['id'])
            qty = value['quantity']
            for menu_item in menu_items:
                if key == menu_item.id:
                    if menu_item.percentage_discount:
                        total = total + (menu_item.discounted_price * qty)
                    else:
                        total = total + (menu_item.price * qty)

        return total

    def get_item(self, menu_item_id):
        if str(menu_item_id) in self.cart:
            return self.cart[str(menu_item_id)]
        else:
            return None
    # This method retrieves an item from the cart based on its menu_item_id and returns it