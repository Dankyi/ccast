import ccxt.async_support as ccxt
from platform import system as operating_system
import asyncio

import middleware_fake_money as middleware


async def main(exchange):
    pass


if __name__ == "__main__":

    EXCHANGE = ccxt.kraken({"verbose": False, "enableRateLimit": True})

    if operating_system().upper() == "WINDOWS":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main(EXCHANGE))
