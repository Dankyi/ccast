import ccxt.async_support as ccxt
from platform import system as operating_system
import asyncio
from threading import Thread, Event

import middleware_fake_money as middleware


class AIGridBot(Thread):

    def __init__(self, exchange, coin_pair):

        Thread.__init__(self)  # The class inherits the Thread class in Python
        self.daemon = True  # Lets Python forcefully destroy the thread on an unsafe shutdown, not preferred of course
        self.stop_signal = Event()
        self.exchange = exchange
        self.coin_pair = coin_pair

    async def __start_ai(self):

        await self.exchange.load_markets(True)
        await self.__run_ai()

    async def __run_ai(self):

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

    ai_bot = AIGridBot(EXCHANGE, "ETH/BTC")

    print("Press ENTER to STOP THE BOT!")
    print()

    ai_bot.start()

    _ = input()

    ai_bot.stop()

    ai_bot.join()
