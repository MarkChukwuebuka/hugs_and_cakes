from django.urls import path

from crm.views import ContactUsView, AboutView, HomeView, CategoryView, MenuView

urlpatterns = [
    path('add-to-cart/<int:item_id>/', HomeView.as_view(), name='add-to-cart'),
]