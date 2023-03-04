def place_order(kite, exchange, tradingsymbol, quantity, order_type):
    order_id = kite.place_order(variety=kite.VARIETY_REGULAR, 
                                exchange=exchange,
                                tradingsymbol=tradingsymbol,
                                transaction_type=order_type,
                                quantity=quantity,
                                product=kite.PRODUCT_CNC,
                                order_type=kite.ORDER_TYPE_MARKET)
    
    return order_id

class TradingStrategy:
    def __init__(self, kite, model, scl, lag, exchange, symbol, quantity, delta, backtesting=True, dqueue=None):
        self.queue = collections.deque()
        self.price_dqueue = dqueue
        self.model = model
        self.scl = scl
        self.profit = 0
        self.curr_state = None
        self.lag = lag
        self.buy_price = float("Inf")
        self.backtesting = backtesting
        self.kite = kite
        self.exchange = exchange
        self.symbol = symbol
        self.quantity = quantity
        self.delta = delta
        
    def trade(self, price):
        self.queue.append(price)

        while len(self.queue) > self.lag:
            self.queue.popleft()
        
        pred = None
        
        if len(self.queue) == self.lag:
            window = np.array([self.scl.transform(np.array(self.queue).reshape(-1,1))])

            pred = self.model.predict(window)
            pred = self.scl.inverse_transform(pred[0])
            pred = [x[0] for x in pred]

        buy_price = price+min(20.0, price*0.03/100)
        sell_price = price-min(20.0, price*0.03/100)

        if self.curr_state is None or self.curr_state == 'SELL':
            if (pred is not None and get_trend(pred) > 1):
                status = False

                if self.backtesting is False:
                    if self.price_dqueue is None or len(self.price_dqueue) == 0 or self.price_dqueue[-1] <= price:
                        order_id = place_order(self.kite, self.exchange, self.symbol, self.quantity, 'BUY')
                        hist = self.kite.order_history(order_id)

                        if len(hist) > 0 and hist[-1]['status'] == 'COMPLETE':
                            status = True
                            buy_price = hist[-1]['average_price']

                if self.backtesting or status:
                    self.curr_state = 'BUY'
                    self.buy_price = buy_price
                    print('BUY', self.buy_price)


        elif sell_price-self.buy_price > self.delta and self.curr_state == 'BUY':
            if (pred is not None and get_trend(pred) < 1 and get_profit_window(pred) > 0):
                status = False

                if self.backtesting is False:
                    if self.price_dqueue is None or len(self.price_dqueue) == 0 or self.price_dqueue[-1] >= price:
                        order_id = place_order(self.kite, self.exchange, self.symbol, self.quantity, 'SELL')
                        hist = self.kite.order_history(order_id)

                        if len(hist) > 0 and hist[-1]['status'] == 'COMPLETE':
                            status = True
                            sell_price = hist[-1]['average_price']

                if self.backtesting or status:
                    self.curr_state = 'SELL'
                    self.profit += self.quantity*(sell_price-self.buy_price)
                    print('SELL', sell_price, self.profit)
    
    def get_profit(self):
        return self.profit
