import ccxt.async_support as ccxt
from platform import system as operating_system
import asyncio
from threading import Thread, Event

import middleware_fake_money as middleware


class AIGridBot(Thread):

    def __init__(self, exchange, coin_pair, stop):

        Thread.__init__(self)
        self.stop_signal = stop
        self.exchange = exchange
        self.coin_pair = coin_pair

    async def __start_ai(self):

        await self.exchange.load_markets(True)
        await self.__run_ai()

    async def __run_ai(self):

        while not self.stop_signal.is_set():
            pass

        await self.__stop_ai()

    async def __stop_ai(self):

        await self.exchange.close()

    def run(self):

        if operating_system().upper() == "WINDOWS":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        asyncio.run(self.__start_ai())


if __name__ == "__main__":

    EXCHANGE = ccxt.binance({"verbose": False, "enableRateLimit": True})

    stop_signal = Event()

    ai_bot = AIGridBot(EXCHANGE, "ETH/BTC", stop_signal)
    ai_bot.daemon = True

    print("Press ENTER to STOP THE BOT!")
    print()

    ai_bot.start()

    _ = input()

    stop_signal.set()

    ai_bot.join()
