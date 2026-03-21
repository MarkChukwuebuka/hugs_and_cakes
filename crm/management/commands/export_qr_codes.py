
import os
from django.core.management.base import BaseCommand
from crm.services.table_service import generate_qr_png
from crm.models import Table


class Command(BaseCommand):
    help = "Export QR code PNGs for all active tables"

    def add_arguments(self, parser):
        parser.add_argument("--output", default="qr_codes/", help="Output directory")

    def handle(self, *args, **options):
        output_dir = options["output"]
        os.makedirs(output_dir, exist_ok=True)

        tables = Table.active_available_objects.filter(is_active=True).order_by("number")
        for table in tables:
            png = generate_qr_png(table)
            path = os.path.join(output_dir, f"table_{table.number}.png")
            with open(path, "wb") as f:
                f.write(png)
            self.stdout.write(f"  ✓ Table {table.number} → {path}")

        self.stdout.write(self.style.SUCCESS(f"\nExported {tables.count()} QR codes."))