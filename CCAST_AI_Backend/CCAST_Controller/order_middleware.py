import exchange_middleware as ex_middleware


class Middleware:

    def __init__(self, grid_amount, dummy):

        self.real_money = not dummy
        self.initial_balance = True

        self.starting_quote = 0.0
        self.profit_percentage = 0.0

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

    def get_percentage_profit(self):

        return self.profit_percentage

    async def get_balance(self, exchange, side, coin_pair):

        current_balance = [0.0, 0.0]

        if self.real_money:

            coin_pair_split = coin_pair.split("/")

            account_balance = await ex_middleware.fetch_balance(exchange)

            if coin_pair_split[0] in account_balance:  # Base
                current_balance[0] = float(account_balance[coin_pair_split[0]])

            if coin_pair_split[1] in account_balance:  # Quote
                current_balance[1] = float(account_balance[coin_pair_split[1]])

        else:

            current_balance[0] = self.base
            current_balance[1] = self.quote

        if self.initial_balance:

            self.starting_quote = current_balance[1]
            self.initial_balance = False

        else:

            if side is not None:

                if not side:

                    self.profit_percentage = (1.0 - (self.starting_quote / current_balance[1])) * 100.0

                    with open("PROFIT_LOG.txt", "a+") as profit_log_writer:
                        #  Write a log of the profit after each sell, each line is a new sell event.
                        profit_log_writer.write(str(self.profit_percentage))
                        profit_log_writer.write("\n")

        return current_balance

    async def process_order(self, exchange, side, coin_pair):

        if self.real_money:

            pair_balance = await self.get_balance(exchange, side, coin_pair)  # [BASE/QUOTE] e.g., [0.001, 0.000349]

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
