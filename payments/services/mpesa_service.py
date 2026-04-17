import requests
import base64
from datetime import datetime
from django.conf import settings
from requests.auth import HTTPBasicAuth


# payments/services/mpesa_service.py

import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings


def get_access_token():
    url = f"{settings.MPESA_CONFIG['BASE_URL']}/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(
        url,
        auth=HTTPBasicAuth(
            settings.MPESA_CONFIG['CONSUMER_KEY'],
            settings.MPESA_CONFIG['CONSUMER_SECRET']
        ),
        timeout=10
    )

    # DEBUG (keep this for now)
    print("MPESA TOKEN RESPONSE:", response.text)

    data = response.json()
    return data["access_token"]

def generate_password():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    data_to_encode = (
        settings.MPESA_CONFIG["SHORTCODE"] +
        settings.MPESA_CONFIG["PASSKEY"] +
        timestamp
    )

    password = base64.b64encode(data_to_encode.encode()).decode()

    return password, timestamp


def initiate_stk_push(phone_number, amount, account_reference, transaction_desc):
    access_token = get_access_token()
    password, timestamp = generate_password()

    url = f"{settings.MPESA_CONFIG['BASE_URL']}/mpesa/stkpush/v1/processrequest"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "BusinessShortCode": settings.MPESA_CONFIG["SHORTCODE"],
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": settings.MPESA_CONFIG["SHORTCODE"],
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CONFIG["CALLBACK_URL"],
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc,
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()