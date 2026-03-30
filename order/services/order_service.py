from cart.services import CartService
from crm.models import Table, MenuItem
from order.constants import OrderType, OrderStatus
from order.models import Order, DeliveryAddress, Area, OrderItem
from utils.constants.messages import ResponseMessages, ErrorMessages
from utils.models import ModelService
from utils.util import CustomRequestUtil, generate_order_ref, AppLogger
from django.db import transaction

class OrderService(CustomRequestUtil):

    def __init__(self, request):
        super().__init__(request)
        self.request = request
        self.model_service = ModelService(request)
        self.model = Order
        self.cart = CartService(request)

    def create_single(self, payload):
        order_type = self.request.session.get("order_type") or OrderType.delivery
        notes = payload.pop("notes", None)
        try:
            with transaction.atomic():
                if order_type == OrderType.delivery:
                    delivery_address = DeliveryAddress.objects.create(
                        **payload
                    )

                    delivery_fee = 0
                    area = Area.objects.filter(id=self.request.POST.get("area")).first()
                    if area:
                        delivery_fee = area.delivery_fee

                    table = None

                    total_amount = self.cart.get_total_cost() + delivery_fee
                else:
                    delivery_address = None
                    table_id = self.request.session.get("table_id")
                    table = Table.active_available_objects.filter(id=table_id).first()
                    total_amount = self.cart.get_total_cost()

                order = Order.objects.create(
                    order_id=generate_order_ref(),
                    order_type=order_type,
                    table=table,
                    delivery_address=delivery_address,
                    status=OrderStatus.pending,
                    total_amount=total_amount,
                    notes=notes
                )

                for item in self.cart:
                    menu_item_in_cart = item.get("menu_item")
                    quantity_in_cart = item.get("quantity")
                    menu_item = MenuItem.active_available_objects.filter(id=menu_item_in_cart.id).first()
                    if not menu_item:
                        continue

                    if menu_item.percentage_discount:
                        item_cost = menu_item.discounted_price * quantity_in_cart
                        original_price = menu_item.discounted_price
                    else:
                        item_cost = menu_item.price * quantity_in_cart
                        original_price = menu_item.price

                    OrderItem.active_available_objects.create(
                        order=order,
                        menu_item=menu_item,
                        quantity=quantity_in_cart,
                        original_price=original_price,
                        total_cost=item_cost
                    )

        except Exception as e:
            AppLogger.report(e, error_position="create_order")
            return None, ErrorMessages.something_went_wrong

        self.cart.clear()

        self.request.session.pop("order_type", None)
        self.request.session.pop("table_id", None)
        return ResponseMessages.order_placed_successfully, None


