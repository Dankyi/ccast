from time import perf_counter_ns as stopwatch
import ccxt.async_support as ccxt
import asyncio


async def get_exchange():

    exchange = ccxt.binance({"verbose": False, "enableRateLimit": True})
    await exchange.load_markets(True)

    print("Exchange: " + exchange.name)
    print("Rate Limit: " + str(exchange.rateLimit) + "ms")
    print()

    return exchange


def find_coin(exchange):

    return ""


async def main():

    exchange = await get_exchange()

    s_time = stopwatch()
    best_coin = find_coin(exchange)
    e_time = stopwatch() - s_time
    e_time /= 1_000_000

    print("Best Coin: " + str(best_coin))
    print("Time Taken to Determine: " + str(e_time))
    print()

    await exchange.close()


if __name__ == "__main__":

    """
    
    Note, since the main() method of this class would be called from another Python file in the normal operation, e.g.,
    the AI or the Middleware, the if __name__ == "__main__" section would not be present in that version.
    
    """

    asyncio.run(main())
