class Middleware:

    def __init__(self, grid_amount, dummy):

        self.real_money = dummy
        self.quote_div_grids = 1.0 / grid_amount

        if not self.real_money:

            self.base = 0.0
            self.quote = 1.0

    @staticmethod
    def get_fee(exchange, coin_pair, side):

        fee_dict = exchange.calculate_fee(coin_pair, "market", side, 0, 0)
        return float(fee_dict["rate"])

    async def get_balance(self, exchange=None):

        if self.real_money:

            pass  # TODO: Query exchange for user's balance

        else:

            return [self.base, self.quote]

    async def process_order(self, exchange, side, coin_pair):

        pass
