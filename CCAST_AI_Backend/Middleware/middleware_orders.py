class Middleware:

    def __init__(self, grid_amount, dummy):

        self.real_money = not dummy

        if self.real_money:

            self.quote_div_grids = None  # Will be initialised later!

        else:

            self.base = 0.0
            self.quote = 1.0
            self.quote_div_grids = self.quote / grid_amount

    @staticmethod
    def get_fee(exchange, coin_pair, side):

        fee_dict = exchange.calculate_fee(coin_pair, "market", side, 0, 0)
        return float(fee_dict["rate"])

    async def get_balance(self, exchange):

        if self.real_money:

            pass  # TODO: Query exchange for user's balance

        else:

            return [self.base, self.quote]

    async def process_order(self, exchange, side, coin_pair):

        if self.real_money:

            pass  # TODO: Query exchange for trading user's real money

        else:

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
