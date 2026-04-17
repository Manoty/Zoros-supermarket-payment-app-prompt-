from payments.models import PaymentTransaction


def create_transaction(phone_number, amount):
    return PaymentTransaction.objects.create(
        phone_number=phone_number,
        amount=amount
    )


def update_transaction_with_mpesa(transaction, response):
    transaction.mpesa_request_id = response.get("MerchantRequestID")
    transaction.mpesa_checkout_id = response.get("CheckoutRequestID")
    transaction.save()