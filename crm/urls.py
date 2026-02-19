from django.urls import path

from crm.views import ContactUsView, AboutView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactUsView.as_view(), name='contact'),
    path('about-us/', AboutView.as_view(), name='about'),
]