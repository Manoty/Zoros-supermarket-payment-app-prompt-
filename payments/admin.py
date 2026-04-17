from django.contrib import admin
from .models import PaymentTransaction


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "phone_number", "amount", "status", "created_at")
    search_fields = ("phone_number", "mpesa_checkout_id", "receipt_number")