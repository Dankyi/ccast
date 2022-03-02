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


async def find_coin(exchange):

    best_coin = ""
    tightest_percentage = 100

    PROGRESS = 0  # For debug purposes
    TOTAL_COIN_PAIRS = len(exchange.symbols)  # For debug purposes

    for coin_pair in exchange.symbols:

        coin_pair_index = exchange.symbols.index(coin_pair)

        candle_stick_data = await exchange.fetch_ohlcv(exchange.symbols[coin_pair_index], "1d")
        candle_stick = candle_stick_data[-1]  # Gets yesterday's final candle stick

        high_price = candle_stick[2]  # Yesterday's high and low
        low_price = candle_stick[3]

        difference = 1.0 - (low_price / high_price)

        if difference < tightest_percentage:
            best_coin = coin_pair
            tightest_percentage = difference

        PROGRESS += 1  # For debug purposes
        PERCENTAGE = (PROGRESS / TOTAL_COIN_PAIRS) * 100.0  # For debug purposes
        print(f"Completed: {PROGRESS}/{TOTAL_COIN_PAIRS} -> " + str("%.2f" % PERCENTAGE) + "%")  # For debug purposes


    return best_coin


async def main():

    exchange = await get_exchange()

    s_time = stopwatch()
    best_coin = await find_coin(exchange)
    e_time = stopwatch() - s_time
    e_time /= 1_000_000

    print("Best Coin: " + str(best_coin))
    print("Time Taken to Determine: " + str(e_time) + "ms")
    print()

    await exchange.close()


if __name__ == "__main__":

    """
    
    Note, since the main() method of this class would be called from another Python file in the normal operation, e.g.,
    the AI or the Middleware, the if __name__ == "__main__" section would not be present in that version.
    
    """

    asyncio.run(main())
