from time import perf_counter_ns as stopwatch
import ccxt.async_support as ccxt
import asyncio


async def get_exchange():

    exchange = ccxt.binance({"verbose": False, "enableRateLimit": True})
    await exchange.load_markets(True)

    print("Exchange: " + exchange.name)
    print("Rate Limit: " + str(exchange.rateLimit) + "ms")

    return exchange


async def main():

    exchange = await get_exchange()

    await exchange.close()


if __name__ == "__main__":

    """
    
    Note, since the main() method of this class would be called from another Python file in the normal operation, e.g.,
    the AI or the Middleware, the if __name__ == "__main__" section would not be present in that version.
    
    """

    asyncio.run(main())
