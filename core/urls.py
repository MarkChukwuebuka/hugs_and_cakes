import os

from django.contrib import admin
from django.urls import path, include

app_name = os.getenv('APP_NAME')

admin.site.site_header = f"{app_name} Administration"
admin.site.site_title = f"{app_name} Admin Portal"
admin.site.index_title = f"Welcome to {app_name} Admin Dashboard"




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crm.urls')),
    path('', include('account.urls')),
    path('', include('order.urls')),
    path('', include('cart.urls')),
]


handler404 = "crm.views.page_not_found"
handler500 = "crm.views.server_error"