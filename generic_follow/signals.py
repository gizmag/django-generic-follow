from django.dispatch import Signal


follow_bulk_create = Signal(providing_args=["users", "target"])
follow_bulk_delete = Signal(providing_args=["users", "target"])
