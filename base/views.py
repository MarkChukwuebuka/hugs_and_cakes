from django.shortcuts import render
from django.views import View

from utils.util import CustomRequestUtil


# Create your views here.
class BaseMVTView(View):
    util_class = CustomRequestUtil
    serializer_class = None
    template_name = None
    template_on_error = None
    extra_context_data = None

    def get_util(self, request):
        util = self.util_class(request)
        util.serializer_class = self.serializer_class
        util.template_name = self.template_name
        util.template_on_error = self.template_on_error
        util.extra_context_data = self.extra_context_data
        return util
