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
    tightest_difference = 100
    difference_variation = 0.01  # 0.5% (0.005) by default

    trading_volume = {}  # Trading Volume : [Low, High, Coin Pair]
    raw_volumes = []
    top_n = 100  # E.g., top 100 coins (by trading volume)

    PROGRESS = 0  # For debug purposes
    TOTAL_COIN_PAIRS = len(exchange.symbols)  # For debug purposes

    print("Gathering coin pair data...")
    print()

    for coin_pair in exchange.symbols:

        coin_pair_index = exchange.symbols.index(coin_pair)

        candle_stick_data = await exchange.fetch_ohlcv(exchange.symbols[coin_pair_index], "1d")

        if len(candle_stick_data) < 1:
            continue  # For some strange reason I found a coin pair that didn't return the standard 720 length list,
            #  it was 0...

        candle_stick = candle_stick_data[-1]  # Gets yesterday's final candle stick

        high_price = candle_stick[2]  # Yesterday's high, low and volume
        low_price = candle_stick[3]
        volume = candle_stick[-1]

        if volume < 1:
            continue  # There are some coins with 0 trading volume, we aren't interested in those

        trading_volume[volume] = [low_price, high_price, coin_pair]
        raw_volumes.append(volume)

        PROGRESS += 1  # For debug purposes
        PERCENTAGE = (PROGRESS / TOTAL_COIN_PAIRS) * 100.0  # For debug purposes
        print(f"Gathered: {PROGRESS}/{TOTAL_COIN_PAIRS} -> " + str("%.2f" % PERCENTAGE) + "%")  # For debug purposes

    print()
    print("Determining best coin pair from top " + str(top_n) + " coin pairs...")
    print()

    raw_volumes.sort(reverse=True)

    for volume in raw_volumes[:top_n]:  # Top N coins by 24h trading volume

        low_price = trading_volume[volume][0]
        high_price = trading_volume[volume][1]

        difference = 1.0 - (low_price / high_price)

        if difference < difference_variation:
            continue  # We want a bit of variance in the 24h difference, to indicate highs and lows - a completely
            # flat price means you can never buy or sell!

        if difference < tightest_difference:
            best_coin = trading_volume[volume][2]
            tightest_difference = difference

        print("Current: " + best_coin + " -> " + str(tightest_difference))  # For debug purposes

    print()  # For debug purposes
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
