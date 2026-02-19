from django.views import View

from utils.util import CustomRequestUtil



class HomeView(View, CustomRequestUtil):
    template_name = 'index.html'
    extra_context_data = {
        "title": "Welcome",
    }

    def get(self, request, *args, **kwargs):
        return self.process_request(request)


class AboutView(View, CustomRequestUtil):
    template_name = 'about.html'
    extra_context_data = {
        "title": "About Us",
    }

    def get(self, request, *args, **kwargs):
        return self.process_request(request)


class ContactUsView(View, CustomRequestUtil):
    template_name = 'contact-us.html'
    extra_context_data = {
        "title": "Contact Us",
    }

    def get(self, request, *args, **kwargs):
        return self.process_request(request)
