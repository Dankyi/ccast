class Middleware:

    def __init__(self, grid_amount, dummy):

        self.real_money = not dummy

        if self.real_money:

            self.quote_div_grids = None  # Will be initialised later!

        else:

            self.base = 0.0
            self.quote = 1.0
            self.quote_div_grids = self.quote / grid_amount

    def get_type(self):
        return self.real_money

    @staticmethod
    def get_fee(exchange, coin_pair, side):

        fee_dict = exchange.calculate_fee(coin_pair, "market", side, 0, 0)
        return float(fee_dict["rate"])

    async def get_balance(self, exchange, coin_pair):

        if self.real_money:

            coin_pair_split = coin_pair.split("/")

            account_balance = await exchange.fetch_balance()
            account_balance = account_balance["total"]

            base_quote_balance = [0.0, 0.0]

            if coin_pair_split[0] in account_balance:  # Base
                base_quote_balance[0] = float(account_balance[coin_pair_split[0]])

            if coin_pair_split[1] in account_balance:  # Quote
                base_quote_balance[1] = float(account_balance[coin_pair_split[1]])

            return base_quote_balance

        else:

            return [self.base, self.quote]

    async def process_order(self, exchange, side, coin_pair):

        if self.real_money:

            pair_balance = await self.get_balance(exchange, coin_pair)
            # [BASE, QUOTE]

            if side:  # Buy

                pass

            else:  # Sell

                pass

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
