import CCAST_AI_Backend.CCAST_Controller.AI_System.exchange_middleware as ex_middleware


class Middleware:

    def __init__(self, grid_amount, dummy):

        self.real_money = not dummy

        if self.real_money:

            self.first_order = True
            self.grid_amount = grid_amount
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

            account_balance = await ex_middleware.fetch_balance(exchange)

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

            pair_balance = await self.get_balance(exchange, coin_pair)  # [BASE/QUOTE] e.g., [0.001, 0.000349]

            if self.first_order:

                self.quote_div_grids = pair_balance[1] / self.grid_amount
                self.first_order = False

            if side:  # Buy

                base_quote_price = await ex_middleware.fetch_current_price(exchange, coin_pair)

                amount = self.quote_div_grids / base_quote_price
                await ex_middleware.create_order(exchange, coin_pair, "buy", amount)

                #  Amount of BASE currency to buy. E.g., if you are trading ETH/BTC, and want to buy 0.1 BTC of ETH,
                #  you need to do 0.1 / Price, so if ETH/BTC is currently trading at 0.07, then 0.1 BTC is worth
                #  1.42 ETH, so you feed that into the create_order(..) function.

            else:  # Sell

                await ex_middleware.create_order(exchange, coin_pair, "sell", pair_balance[0])

                #  Amount of BASE currency to sell. Since we want to sell all of the BASE currency at once, we only
                #  need to feed it the latest current balance. E.g., if you have ETH/BTC as [5.63, 0.031] then you want
                #  to just sell all 5.63 ETH, so just pass index 0 in as the amount without any other processing.

        else:

            if side:  # Buy

                self.quote -= self.quote_div_grids

                base_quote_price = await ex_middleware.fetch_current_price(exchange, coin_pair)

                amount = self.quote_div_grids / base_quote_price

                self.base += amount

            else:  # Sell

                coin_pair_split = coin_pair.split("/")

                base_dollar_pair = coin_pair_split[0] + "/" + "USDT"
                quote_dollar_pair = coin_pair_split[1] + "/" + "USDT"

                base_dollars = await ex_middleware.fetch_current_price(exchange, base_dollar_pair)
                base_dollars *= self.base

                quote_dollars = await ex_middleware.fetch_current_price(exchange, quote_dollar_pair)

                quote_amount = base_dollars / quote_dollars

                self.quote += quote_amount
                self.base = 0.0
