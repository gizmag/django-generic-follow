from django.dispatch import Signal


bulk_create = Signal(providing_args=["users", "target"])
bulk_delete = Signal(providing_args=["users", "target"])
