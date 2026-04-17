from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from payments.services.mpesa_service import initiate_stk_push
from payments.repositories.payment_repository import (
    create_transaction,
    update_transaction_with_mpesa
)


class InitiatePaymentView(APIView):

    def post(self, request):
        phone_number = request.data.get("phone_number")
        amount = request.data.get("amount")

        if not phone_number or not amount:
            return Response(
                {"error": "phone_number and amount are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1. Create transaction FIRST
        transaction = create_transaction(phone_number, amount)

        # 2. Call M-Pesa
        response = initiate_stk_push(
            phone_number=phone_number,
            amount=amount,
            account_reference=str(transaction.id),
            transaction_desc="Supermarket Payment"
        )

        # 3. Update transaction with M-Pesa IDs
        update_transaction_with_mpesa(transaction, response)

        return Response({
            "message": "STK Push initiated",
            "transaction_id": transaction.id,
            "mpesa_response": response
        })