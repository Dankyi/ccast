

class Middleware:

    def __init__(self):  # Simulating an ETH/BTC pair...

        self.base = 0.0  # Pretend this is ETH
        self.quote = 1.0  # Pretend this is BTC

    def get_balance(self):

        return [self.base, self.quote]  # Return the coin pair e.g., ETH/BTC

    async def process_order(self, exchange, side, grid_amount, coin_pair_id):

        if side:  # Buy

            quote_div = self.quote / grid_amount

            self.quote -= quote_div

            base_quote_price = await exchange.fetch_ticker(exchange.symbols[coin_pair_id])
            base_quote_price = base_quote_price.__getitem__("last")

            self.base += quote_div / base_quote_price

        else:  # Sell
            pass

