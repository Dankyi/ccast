import asyncio
from platform import system as operating_system
from threading import Thread, Event
from time import sleep

import order_middleware as or_middleware
import exchange_middleware as ex_middleware


class AIGridBot(Thread):

    def __init__(self, exchange, dummy, coin_pair, lower_grid_percentage, profit_percentage):

        """

        The constructor for the AI class.

        :param exchange: The exchange object
        :param dummy: Whether the AI will be using real money or fake money, dummy = True is fake money.
        :param coin_pair: The coin-pair to trade, e.g., ETH/BTC
        :param lower_grid_percentage: The price separation between each buy grid, expressed as a percentage
        :param profit_percentage: The price that the bot will sell at, as a percentage above the current price
        """

        Thread.__init__(self)  # The class inherits the Thread class in Python
        self.daemon = True  # Lets Python forcefully destroy the thread on an unsafe shutdown, not preferred of course
        self.stop_signal = Event()

        self.MIN_PERCENTAGE = 0.25  # Don't allow lower grids to go below this percentage, the default (0.25) would
        #  represent 25% of the entire coins price, it is basically a limit on the number of grids that can be created.
        #  If you could keep going infinitely, then you could have grids set to negative prices.

        self.exchange = exchange
        self.dummy = dummy
        self.coin_pair = coin_pair
        self.lower_grid_percentage = lower_grid_percentage  # Price separation between lower grid prices
        self.profit_percentage = profit_percentage  # Price to sell at as a percentage increase of the current price

        self.coin_pair_price = 0.0

        #  These three are calculated later, so are set to some default values on construction.
        self.balance = [0.0, 0.0]
        self.grid_amount = 0
        self.order_middleware = or_middleware.Middleware(1, dummy)

    async def __get_balance(self, side):

        """

        A method to obtain the current balance of the user and update a variable with it. The AI runs this every loop
        to keep it up to date.

        """

        current_balance = await self.order_middleware.get_balance(self.exchange, side, self.coin_pair)
        self.balance = [current_balance[0], current_balance[1]]

    def get_information(self):

        """

        A getter method that contains information that the frontend may want to pull from the AI, can be expanded as
        necessary.

        BALANCE: The users current balance in the form [BASE, QUOTE]
        GRID AMOUNT: The amount of grids the AI has created
        CURRENT PRICE: The current price of the coin pair, e.g., ETH/BTC may be 0.0718825
        ALIVE: Is the AI thread running?
        PROFIT: The percentage profit of the QUOTE currency since the AI instance was started

        :return: a dictionary containing the above described information
        """

        return {"BALANCE": self.balance,
                "GRID AMOUNT": self.grid_amount,
                "CURRENT PRICE": self.coin_pair_price,
                "ALIVE": self.is_alive(),
                "PROFIT": self.order_middleware.get_percentage_profit()}

    async def __init_grid_amount_and_middleware(self):

        """

        Calculate the amount of grids to create. Attempts to get as close to the minimum purchasable amount that it
        can, and also factors in a hard limit on how low the grids can go (self.MIN_PERCENTAGE).

        The hard limit is mostly to save on CPU and RAM usage. For example, if you were trading ETH/BTC, and had 1 BTC,
        and the current price of ETH/BTC was 0.0703975, if the minimum purchasable amount of ETH was 0.001 (this is the
        value for FTX) you would create 14205 grids. Not only would this produce grid prices less than zero (the other
        reason for the hard limit), it is simply extremely unlikely that a coin pair would get anywhere close to being
        worth 0, so holding such a big list in memory is a waste of RAM, and looping through the whole 14205 indexes is
        also a waste of CPU, so it's sensible to have a minimum price level, which is 75% of the current value of the
        coin by default.

        """

        min_base_order_amount = float(self.exchange.markets[self.coin_pair]["limits"]["amount"]["min"])

        buy_fee = self.order_middleware.get_fee(self.exchange, self.coin_pair, "buy")

        base_quote_price = await ex_middleware.fetch_current_price(self.exchange, self.coin_pair)

        quote_to_base = self.balance[1] / base_quote_price
        self.grid_amount = int(quote_to_base // min_base_order_amount)

        minimum_grid_level = base_quote_price * (1.0 - self.MIN_PERCENTAGE)
        grid_step_price = base_quote_price * (self.lower_grid_percentage / 100.0)

        for i in range(self.grid_amount):

            base_quote_price -= grid_step_price
            base_quote_price -= (base_quote_price * buy_fee)

            if base_quote_price < minimum_grid_level and i < self.grid_amount:
                self.grid_amount = i
                break

        self.order_middleware = or_middleware.Middleware(self.grid_amount, self.dummy)

    async def __start_ai(self):

        """

        The run() method for the Thread starts this private method. It loads the markets from the exchange and then
        starts up the AI processing.

        """

        await ex_middleware.load_markets(self.exchange)

        await self.__get_balance(None)  # Update the balance before beginning

        await self.__init_grid_amount_and_middleware()

        await self.__run_ai()

    async def create_grids(self):

        """

        For this particular AI implementation, this method creates the grids that are used to buy cryptocurrency at
        various prices. It's ran every time a sell occurs.

        Fee's are taken into account here. The grid percentage will have the fee taken off it to negate it, and the
        sell grid will have the fee added onto it for the same effect.

        :return: A dictionary with two keys. The "Buy" key holds an array of arrays, where each index is a two indexed
        array of a buy price and whether or not it was triggered yet. The "Sell" key holds a single value, which is the
        sell "grid" price.

        """

        #  "Buy": List of prices to buy cryptocurrency (lower grids) - and if they have already been crossed!
        #  "Sell": Single grid-point, this is the upper price in the grid where all the bought cryptocurrency is sold
        #
        grids = {"Buy": [], "Sell": 0.0}

        current_price = await ex_middleware.fetch_current_price(self.exchange, self.coin_pair)

        buy_fee = self.order_middleware.get_fee(self.exchange, self.coin_pair, "buy")
        sell_fee = self.order_middleware.get_fee(self.exchange, self.coin_pair, "sell")

        grid_step_price = current_price * (self.lower_grid_percentage / 100.0)

        grids["Sell"] = current_price * (1.0 + (self.profit_percentage / 100.0))
        grids["Sell"] += (grids["Sell"] * sell_fee)

        for _ in range(self.grid_amount):

            current_price -= (current_price * buy_fee)
            grids["Buy"].append([current_price, False])
            current_price -= grid_step_price

        return grids

    async def __run_ai(self):

        """

        The "main method" of the AI so-to-speak. Runs in a permanent while-loop and checks an Event object every loop.

        The Event object is a method of thread synchronisation in Python: if the object is NOT set, the AI will continue
        looping (i.e., doing its buying and selling et al.) but if the object IS set then the AI will sell off its
        remaining stock (if applicable) and then stop. An external class triggers this.

        """

        grids = await self.create_grids()
        bought = False

        while True:

            current_price = await ex_middleware.fetch_current_price(self.exchange, self.coin_pair)
            self.coin_pair_price = current_price

            if current_price >= grids["Sell"]:

                if not bought:

                    if self.stop_signal.is_set():
                        break
                    else:
                        continue  # TODO: Maybe re-evaluate grids if this happens n times?

                bought = False

                await self.order_middleware.process_order(self.exchange, False, self.coin_pair)

                await self.__get_balance(False)  # Update the balance after selling

                if self.stop_signal.is_set():
                    break

                sleep(60.0)  # Pause between cycles in-case the market is suddenly dropping or spiking?

                grids = await self.create_grids()
                continue

            if self.stop_signal.is_set():

                if not bought:
                    break
                else:
                    continue

            for grid_price in grids["Buy"]:

                if not grid_price[1]:

                    if current_price <= grid_price[0]:

                        await self.order_middleware.process_order(self.exchange, True, self.coin_pair)
                        grid_price[1] = True

                        bought = True

                        await self.__get_balance(True)  # Update the balance after buying

        await self.__close_api()

    async def __close_api(self):

        """

        If the AI is stopped, the final thing it does is go in here and close the exchange, as per the requirement of
        the CCXT library.

        """

        await self.__get_balance(None)  # Update the balance one last time to be up to date
        await self.exchange.close()  # This can take a second, so the backend needs to utilise .join() to wait for this

    def stop(self):  # Backend calls this method when the user presses the stop button in the frontend

        """

        Some other class (e.g., the Flask backend) calls this method of the AI object, triggering it to stop.

        """

        self.stop_signal.set()

    def run(self):

        """

        The main method of the Thread class in Python, over-ridden to execute the AI processing.

        It also has a little if statement because Windows is special and will throw exceptions if it uses the default
        event loop policy.

        """

        if operating_system().upper() == "WINDOWS":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        asyncio.run(self.__start_ai())  # The threads run method runs the private __start_ai() method in this class
