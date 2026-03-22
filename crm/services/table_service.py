from django.core.cache import cache
from django.db.models import Q

from crm.models import Table
from utils.constants.messages import ResponseMessages, ErrorMessages
from utils.models import ModelService
from utils.util import CustomRequestUtil, make_slug
from django.conf import settings
import qrcode
from io import BytesIO

class TableService(CustomRequestUtil):

    def __init__(self, request):
        super().__init__(request)
        self.model_service = ModelService(request)
        self.model = Table

    def create_single(self, payload):

        pass


    def fetch_list(self, filter_params=None):
        q = Q()

        return self.__get_base_query().filter(q)

    def __get_base_query(self):
        qs = Table.available_objects.all()
        return qs


    def fetch_single_by_id(self, table_id):
        def __handle_fetch():
            table = self.__get_base_query().filter(id=table_id).first()
            if not table:
                return None, self.make_error(ErrorMessages.table_not_found)

            return table, None
        cache_key = self.generate_cache_key(instance_id=table_id, model=self.model)
        return cache.get_or_set(cache_key, __handle_fetch)


    def update_single(self, payload, category_code):
        pass


def generate_qr_png(table) -> bytes:
    """Returns PNG bytes for a table's QR code."""
    url = f"{settings.FRONTEND_BASE_URL}/menu/?token={table.qr_token}"

    img = qrcode.make(url, box_size=10, border=4)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()




