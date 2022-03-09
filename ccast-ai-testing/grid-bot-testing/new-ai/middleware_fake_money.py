

class Middleware:

    def __init__(self):  # Simulating an ETH/BTC pair...

        self.base = 0.0  # Pretend this is ETH
        self.quote = 1.0  # Pretend this is BTC

    def get_balance(self):

        return self.quote  # The quote currency is your balance, it's what you purchase "base" with and sell "base" to.

    async def process_order(self, exchange, side, grid_amount, coin_pair_id):

        if side:  # Buy

            quote_div = self.quote / grid_amount

            self.quote -= quote_div
            self.base += quote_div / (await exchange.fetch_ticker(exchange.symbols[coin_pair_id]).__getitem__("last"))

        else:  # Sell
            pass

