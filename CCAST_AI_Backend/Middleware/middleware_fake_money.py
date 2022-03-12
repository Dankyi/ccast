class Middleware:

    def __init__(self, grid_amount):  # Simulating an ETH/BTC pair...

        self.base = 0.0  # Pretend this is ETH
        self.quote = 1.0  # Pretend this is BTC
        self.quote_div_grids = self.quote / grid_amount
        # E.g., if you have 1 BTC with 4 grids, you want each purchase to be 0.25 BTC.

    def get_balance(self):

        return [self.base, self.quote]  # Return the coin pair e.g., ETH/BTC

    @staticmethod
    def get_fee(exchange, coin_pair, side):

        fee_dict = exchange.calculate_fee(coin_pair, "market", side, 0, 0)
        fee = float(fee_dict["rate"])

        coin_pair_split = coin_pair.split("/")

        if side.upper() == "BUY" and coin_pair_split[0] != fee_dict["currency"]:
            pass  # TODO: Convert fee amount to base currency
        elif side.upper() == "SELL" and coin_pair_split[1] != fee_dict["currency"]:
            pass  # TODO: Convert fee amount to quote currency

        return fee

    async def process_order(self, exchange, side, coin_pair):

        if side:  # Buy

            self.quote -= self.quote_div_grids

            base_quote_price = await exchange.fetch_ticker(coin_pair)
            base_quote_price = base_quote_price.__getitem__("last")

            amount = self.quote_div_grids / base_quote_price

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

            self.quote += quote_amount
            self.base = 0.0
