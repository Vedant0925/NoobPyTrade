logging.basicConfig(level=logging.DEBUG)

def trim_queue(dqueue, lock):
    while True:
        with lock:
            if len(dqueue) > 1:
                dqueue = [dqueue[-1]]
        
def place_trade(dqueue, lock, api_key, access_token):
    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    
    model = keras.models.load_model('trading_model/1')

    with open('metadata.pkl', 'rb') as f:
        scl, historical_ma_data, delta = pickle.load(f)
        
    strat = TradingStrategy(kite, model, scl, 20, 'NSE', 'RELIANCE', 1, delta, backtesting=False, dqueue=dqueue)
    
    while True:
        with lock:
            if len(dqueue) > 0:
                price = dqueue.pop()
                strat.trade(price)
            
def on_ticks(ws, ticks):
    print(ticks[0]['last_price'])
    dqueue.append(ticks[0]['last_price'])

def on_connect(ws, response):
    ws.subscribe([738561])
    ws.set_mode(ws.MODE_LTP, [738561])

def on_close(ws, code, reason):
    ws.stop()


if __name__=="__main__":
    api_key = str(sys.argv[1])
    access_token = str(sys.argv[2])
    
    kws = KiteTicker(api_key, access_token)

    manager = Manager()
    dqueue = manager.list()
    lock = manager.Lock()
    
    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_close = on_close
    
    p1 = Process(target=place_trade, args=(dqueue, lock, api_key, access_token))
    p2 = Process(target=trim_queue, args=(dqueue, lock))
    
    p1.start()
    p2.start()

    # Infinite loop on the main thread. Nothing after this will run.
    # You have to use the pre-defined callbacks to manage subscriptions.
    kws.connect()
