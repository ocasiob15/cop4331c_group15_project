from app import app

import squareconnect

from squareconnect.rest import ApiException
from squareconnect.apis.transactions_api import TransactionsApi
from squareconnect.apis.locations_api import LocationsApi

from uuid import uuid1

square_token    = app.config['SQUARE_TOKEN']
square_app_id   = app.config['SQUARE_APP_ID']
square_location = app.config['SQUARE_LOCATION_ID'] if 'SQUARE_LOCATION_ID' in app.config else None

squareconnect.configuration.access_token = square_token

loc_api   = LocationsApi()
trans_api = TransactionsApi()


# so, the square API uses the swagger spec, which specifies that
# currency ammounts must be of type int, as they indicate the ammount
# in the smallest unit of that currency (cent for USD, satoshi for BTC)
def fulfill_usd_payment(amount):
    # convert float to cents
    amount *= 100
    amount = int(amount)
    return fulfill_payment("USD", amount)

def fulfill_btc_payment(amount):
    # convert float to satoshi
    amount *= 100000000
    amount = int(amount)

    return fulfill_payment("BTC", amount)

def fulfill_payment(currency, amount):

    idemp_key = str(uuid1())

    body = {}

    body['idempotency_key'] = idemp_key
    body['card_nonce']      = "fake-card-nonce-ok"
    body['amount_money']    = {"currency": "USD", "amount" : amount}

    try:
        response = trans_api.charge(square_location, body)

    except ApiException as e:
        response = {"success": False, "errors": [ "{}".format(e) ]}

    print(response)

    return {"success": True}

