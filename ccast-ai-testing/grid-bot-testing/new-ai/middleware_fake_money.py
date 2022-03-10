class Middleware:

    def __init__(self, grid_amount):  # Simulating an ETH/BTC pair...

        self.base = 0.0  # Pretend this is ETH
        self.quote = 1.0  # Pretend this is BTC
        self.quote_div_grids = self.quote / grid_amount
        # E.g., if you have 1 BTC with 4 grids, you want each purchase to be 0.25 BTC.

    def get_balance(self):

        return [self.base, self.quote]  # Return the coin pair e.g., ETH/BTC

    async def process_order(self, exchange, side, coin_pair):

        if side:  # Buy

            self.quote -= self.quote_div_grids

            base_quote_price = await exchange.fetch_ticker(coin_pair)
            base_quote_price = base_quote_price.__getitem__("last")

            amount = self.quote_div_grids / base_quote_price
            fee = float(exchange.calculate_fee(coin_pair, "market", "buy", amount, base_quote_price)["cost"])
            amount -= fee

            self.base += amount

        else:  # Sell

            coin_pair_split = coin_pair.split("/")

            base_dollar_pair = coin_pair_split[0] + "/" + "USDT"
            quote_dollar_pair = coin_pair_split[1] + "/" + "USDT"

            base_dollars = await exchange.fetch_ticker(base_dollar_pair)
            base_dollars = base_dollars.__getitem__("last")
            base_dollars *= self.base

            quote_dollars = await exchange.fetch_ticker(quote_dollar_pair)
            quote_dollars = quote_dollars.__getitem__("last")

            quote_amount = base_dollars / quote_dollars
            fee = float(exchange.calculate_fee(coin_pair, "market", "sell", self.base, quote_amount)["cost"])
            quote_amount -= fee

            self.quote += quote_amount
            self.base = 0.0
