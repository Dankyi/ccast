"""

Author: Zac King (U1758957)

This Python file is designed to test a more real-time implementation of a neural network, it gathers real-time price
data for a coin (bound to the rate limit of the exchange) and predicts after a certain amount of time has passed, and
then repeats.

"""

import ccxt.async_support as ccxt
import asyncio


async def get_exchange():

    exchange = ccxt.hitbtc({"verbose": False, "enableRateLimit": True})
    await exchange.load_markets(True)

    return exchange


async def main():

    exchange = await get_exchange()



    await exchange.close()


if __name__ == "__main__":
    asyncio.run(main())
