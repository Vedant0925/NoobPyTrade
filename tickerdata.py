from kiteconnect import KiteTicker
from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)

def on_ticks(ws, ticks):
    print(ticks[0]['last_price'])

def on_connect(ws, response):
    ws.subscribe([738561])
    ws.set_mode(ws.MODE_LTP, [738561])

def on_close(ws, code, reason):
    ws.stop()
    
kws = KiteTicker(api_key, access_token)

kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()
