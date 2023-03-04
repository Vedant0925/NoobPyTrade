#url creation
import logging
from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)

api_key = <YOUR API KEY>
api_secret = <YOUR API SECRET>

kite = KiteConnect(api_key=api_key)

print(kite.login_url())

#request token
data = kite.generate_session(request_token, api_secret=api_secret)
kite.set_access_token(data["access_token"])

#API call
instruments = kite.instruments()

#instrument/company centred data
for x in instruments:
    if x['tradingsymbol'] == 'RELIANCE':
        print(x)
