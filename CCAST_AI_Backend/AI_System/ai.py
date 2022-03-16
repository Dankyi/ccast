from platform import system as operating_system
import asyncio
from threading import Thread, Event
from time import sleep

from CCAST_AI_Backend.Middleware import middleware_orders as middleware


class AIGridBot(Thread):

    def __init__(self, exchange, dummy, coin_pair, lower_grid_percentage, profit_percentage, grid_amount):

        """

        The constructor for the AI class.

        :param exchange: The exchange object
        :param dummy: Whether the AI will be using real money or fake money, dummy = True is fake money.
        :param coin_pair: The coin-pair to trade, e.g., ETH/BTC
        :param lower_grid_percentage: The price separation between each buy grid, expressed as a percentage
        :param profit_percentage: The price that the bot will sell at, as a percentage above the current price
        :param grid_amount: The amount of lower (buy) grids to create
        """

        Thread.__init__(self)  # The class inherits the Thread class in Python
        self.daemon = True  # Lets Python forcefully destroy the thread on an unsafe shutdown, not preferred of course
        self.stop_signal = Event()

        self.order_middleware = middleware.Middleware(grid_amount, dummy)
        self.exchange = exchange
        self.coin_pair = coin_pair
        self.lower_grid_percentage = lower_grid_percentage  # Price separation between lower grid prices
        self.profit_percentage = profit_percentage  # Price to sell at as a percentage increase of the current price
        self.grid_amount = grid_amount  # How many lower (buy) grids to create

        self.balance = [0.0, 0.0]

    async def __get_balance(self):

        """

        A method to obtain the current balance of the user and update a variable with it. The AI runs this every loop
        to keep it up to date.

        """

        current_balance = await self.order_middleware.get_balance()
        self.balance = [current_balance[0], current_balance[1]]

    def get_balance(self):

        """

        An external class can get the balance from here, it always in the form BASE/QUOTE e.g., ETH/BTC

        :return: The current balance of the coin pair
        """

        return self.balance

    async def __start_ai(self):

        """

        The run() method for the Thread starts this private method. It loads the markets from the exchange and then
        starts up the AI processing.

        """

        print("Fees will be taken into account automatically during grid creation!")
        print()

        await self.exchange.load_markets(True)

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

        current_price = await self.exchange.fetch_ticker(self.coin_pair)
        current_price = current_price.__getitem__("last")

        buy_fee = self.order_middleware.get_fee(self.exchange, self.coin_pair, "buy")
        sell_fee = self.order_middleware.get_fee(self.exchange, self.coin_pair, "sell")

        grid_step_price = current_price * (self.lower_grid_percentage / 100.0)

        grids["Sell"] = current_price * (1.0 + (self.profit_percentage / 100.0))
        grids["Sell"] += (grids["Sell"] * sell_fee)

        for _ in range(self.grid_amount):

            current_price -= (current_price * buy_fee)
            grids["Buy"].append([current_price, False])
            current_price -= grid_step_price

        print("Lower (Buy): " + str(grids["Buy"]))
        print("Upper (Sell): " + str(grids["Sell"]))
        print()

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

            await self.__get_balance()

            current_price = await self.exchange.fetch_ticker(self.coin_pair)
            current_price = current_price.__getitem__("last")
            print(self.coin_pair + " Current Price: " + str(current_price))

            if current_price >= grids["Sell"]:

                if not bought:

                    if self.stop_signal.is_set():
                        break
                    else:
                        continue  # TODO: Maybe re-evaluate grids if this happens n times?

                bought = False

                await self.order_middleware.process_order(self.exchange, False, self.coin_pair)

                print("Sold!")

                if self.stop_signal.is_set():
                    break

                sleep(60.0)  # Pause between cycles in-case the market is suddenly dropping or spiking?

                grids = await self.create_grids()
                continue

            if self.stop_signal.is_set():

                if not bought:
                    break
                else:
                    print("Selling remaining order/s before stopping...")
                    continue

            for grid_price in grids["Buy"]:

                if not grid_price[1]:

                    if current_price <= grid_price[0]:

                        await self.order_middleware.process_order(self.exchange, True, self.coin_pair)
                        grid_price[1] = True

                        bought = True

                        print("Bought!")

        await self.__close_api()

    async def __close_api(self):

        """

        If the AI is stopped, the final thing it does is go in here and close the exchange, as per the requirement of
        the CCXT library.

        """

        await self.__get_balance()  # Update the balance one last time to be up to date
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
