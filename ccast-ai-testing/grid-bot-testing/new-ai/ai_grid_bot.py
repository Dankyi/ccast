import ccxt.async_support as ccxt
from platform import system as operating_system
import asyncio
from threading import Thread, Event

import middleware_fake_money as buy_sell_middleware


class AIGridBot(Thread):

    def __init__(self, exchange, coin_pair, lower_grid_percentage, profit_percentage, grid_amount):

        Thread.__init__(self)  # The class inherits the Thread class in Python
        self.daemon = True  # Lets Python forcefully destroy the thread on an unsafe shutdown, not preferred of course
        self.stop_signal = Event()

        self.exchange = exchange
        self.coin_pair = coin_pair
        self.lower_grid_percentage = lower_grid_percentage  # Price separation between lower grid prices
        self.profit_percentage = profit_percentage  # Price to sell at as a percentage increase of the current price
        self.grid_amount = grid_amount  # How many lower (buy) grids to create

    async def __start_ai(self):

        await self.exchange.load_markets(True)
        await self.__run_ai()

    async def __run_ai(self):

        order_middleware = buy_sell_middleware.Middleware(self.grid_amount)

        #  "Buy": List of prices to buy cryptocurrency (lower grids)
        #  "Sell": Single grid-point, this is the upper price in the grid where all the bought cryptocurrency is sold
        #
        grids = {"Buy": [], "Sell": 0.0}

        current_price = await self.exchange.fetch_ticker(self.coin_pair)
        current_price = current_price.__getitem__("last")

        grids["Buy"].append(current_price)
        grid_step_price = current_price * (self.lower_grid_percentage / 100.0)

        grids["Sell"] = current_price * (1.0 + (self.profit_percentage / 100.0))

        for _ in range(self.grid_amount - 1):

            current_price -= grid_step_price
            grids["Buy"].append(current_price)

        print("Lower (Buy): " + str(grids["Buy"]))
        print("Upper (Sell): " + str(grids["Sell"]))

        while not self.stop_signal.is_set():  # When the backend calls stop() and sets the Event, the loop will break
            pass

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

    ai_bot = AIGridBot(EXCHANGE, "ETH/BTC", 0.05, 0.05, 16)

    print("Press ENTER to STOP THE BOT!")
    print()

    ai_bot.start()

    _ = input()

    ai_bot.stop()

    ai_bot.join()
