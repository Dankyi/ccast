import ccxt.async_support as ccxt
from platform import system as operating_system
import asyncio
from threading import Thread, Event
from time import sleep

import CCAST_AI_Backend.Middleware.middleware_fake_money as transaction_middleware


class AIGridBot(Thread):

    def __init__(self, exchange, coin_pair, lower_grid_percentage, profit_percentage, grid_amount):

        Thread.__init__(self)  # The class inherits the Thread class in Python
        self.daemon = True  # Lets Python forcefully destroy the thread on an unsafe shutdown, not preferred of course
        self.stop_signal = Event()

        self.order_middleware = None
        self.exchange = exchange
        self.coin_pair = coin_pair
        self.lower_grid_percentage = lower_grid_percentage  # Price separation between lower grid prices
        self.profit_percentage = profit_percentage  # Price to sell at as a percentage increase of the current price
        self.grid_amount = grid_amount  # How many lower (buy) grids to create

    def debug_get_balance(self):

        #  A debug function to print the balance to the console, in the full program another backend script is...
        #  ... responsible for this and piping it to the frontend.

        coin_pair_split = self.coin_pair.split("/")
        current_balance = self.order_middleware.get_balance()

        print("Balance: "
              + str(current_balance[0]) + " " + coin_pair_split[0]
              + " | "
              + str(current_balance[1]) + " " + coin_pair_split[1])

        print()

    async def __start_ai(self):

        print("Fees will be taken into account automatically during grid creation!")
        print()

        await self.exchange.load_markets(True)

        self.order_middleware = transaction_middleware.Middleware(self.grid_amount)  # Will eventually be awaited

        await self.__run_ai()

    async def create_grids(self):

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

        grids = await self.create_grids()
        bought = False

        while True:

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

                self.debug_get_balance()

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

        await self.exchange.close()  # This can take a second, so the backend needs to utilise .join() to wait for this

    def stop(self):  # Backend calls this method when the user presses the stop button in the frontend

        self.stop_signal.set()

    def run(self):

        if operating_system().upper() == "WINDOWS":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        asyncio.run(self.__start_ai())  # The threads run method runs the private __start_ai() method in this class


if __name__ == "__main__":

    EXCHANGE = ccxt.binance({"verbose": False, "enableRateLimit": True})

    ai_bot = AIGridBot(EXCHANGE, "ETH/BTC", 0.005, 0.005, 16)

    print("Type B and then ENTER to see the current balance!")
    print("Press ENTER with no input to STOP THE BOT!")
    print()

    ai_bot.start()

    while True:

        command = input()
        if command.upper().startswith("B"):
            ai_bot.debug_get_balance()
        else:
            break

    ai_bot.stop()
    ai_bot.join()
    ai_bot.debug_get_balance()
