from django.urls import path

from order.views import CheckoutView, OrderSuccessView

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/success/<str:order_id>/', OrderSuccessView.as_view(), name='order_success'),
]