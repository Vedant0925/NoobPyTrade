def get_profit_window(prices):
    buy = prices[0]
    profit = 0

    for i in range(1, len(prices)):
        if prices[i] < prices[i-1]:
            profit += prices[i-1]-buy
            buy = prices[i]

    profit += prices[-1]-buy
    
    return profit

def get_trend(prices):
    stack1, stack2 = [], []
    
    for i in range(len(prices)):
        while len(stack1) > 0 and prices[stack1[-1]] >= prices[i]:
            stack1.pop()
        
        stack1.append(i)
        
        while len(stack2) > 0 and prices[stack2[-1]] <= prices[i]:
            stack2.pop()
        
        stack2.append(i)
        
    if len(stack1) != 0 and len(stack2) != 0:
        return len(stack1)/len(stack2)
    elif len(stack1) != 0:
        return len(stack1)
    return 0

class TradingStrategy:
    def __init__(self, model, scl, lag, quantity):
        self.queue = collections.deque()
        self.model = model
        self.scl = scl
        self.profit = 0
        self.curr_state = None
        self.lag = lag
        self.buy_price = float("Inf")
        self.quantity = quantity
        
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

        if self.curr_state is None or self.curr_state == 'SELL':
            if (pred is not None and get_trend(pred) > 1):
                self.curr_state = 'BUY'
                self.buy_price = price
                print('BUY', self.buy_price)

        elif price-self.buy_price > 0 and self.curr_state == 'BUY':
            if (pred is not None and get_trend(pred) < 1 and get_profit_window(pred) > 0):
                self.curr_state = 'SELL'
                self.profit += self.quantity*(price-self.buy_price)
                print('SELL', price, self.profit)
    
    def get_profit(self):
        return self.profit
def get_trend(prices):
    stack1, stack2 = [], []
    
    for i in range(len(prices)):
        while len(stack1) > 0 and prices[stack1[-1]] >= prices[i]:
            stack1.pop()
        
        stack1.append(i)
        
        while len(stack2) > 0 and prices[stack2[-1]] <= prices[i]:
            stack2.pop()
        
        stack2.append(i)
        
    if len(stack1) != 0 and len(stack2) != 0:
        return len(stack1)/len(stack2)
    elif len(stack1) != 0:
        return len(stack1)
    return 0
def get_profit_window(prices):
    buy = prices[0]
    profit = 0

    for i in range(1, len(prices)):
        if prices[i] < prices[i-1]:
            profit += prices[i-1]-buy
            buy = prices[i]

    profit += prices[-1]-buy
    
    return profit
  
