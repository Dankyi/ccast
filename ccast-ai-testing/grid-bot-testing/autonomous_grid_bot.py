from time import perf_counter_ns as stopwatch
import ccxt.async_support as ccxt
import asyncio


async def get_exchange():

    exchange = ccxt.binance({"verbose": False, "enableRateLimit": True})
    await exchange.load_markets(True)

    print("Exchange: " + exchange.name)
    print("Rate Limit: " + str(exchange.rateLimit) + "ms")

    return exchange


async def get_current_price(exchange, coin_pair_id):

    current_price = await exchange.fetch_ticker(exchange.symbols[coin_pair_id])
    current_price = current_price.__getitem__("last")

    return current_price


async def main():

    exchange = await get_exchange()

    coin_pair_id = -1
    coin_pair = "ETH/BTC"

    if coin_pair in exchange.symbols:
        coin_pair_id = exchange.symbols.index(coin_pair)
    else:
        print(coin_pair + " not found in exchange!")

    if coin_pair_id > -1:

        current_price = await get_current_price(exchange, coin_pair_id)
        print(current_price)

    await exchange.close()


if __name__ == "__main__":
    asyncio.run(main())
