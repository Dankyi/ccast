import ccxt.async_support as ccxt
from platform import system as operating_system
import asyncio

import middleware_fake_money as middleware


async def main(exchange):

    await exchange.load_markets(True)

    coin_pair = "ETH/BTC"
    coin_pair_id = -1

    if coin_pair in exchange.symbols:
        coin_pair_id = exchange.symbols.index(coin_pair)
    else:
        print("Coin Pair: " + coin_pair + " cannot be found in the exchange!")

    if coin_pair_id > -1:

        exchange_middleware = middleware.Middleware()
        coin_pair_split = coin_pair.split("/")

        balance = exchange_middleware.get_balance()
        print(coin_pair_split[0] + " -> " + str(balance[0]) + " | " + coin_pair_split[1] + " -> " + str(balance[1]))
        await exchange_middleware.process_order(exchange, True, 16, coin_pair_id)
        balance = exchange_middleware.get_balance()
        print(coin_pair_split[0] + " -> " + str(balance[0]) + " | " + coin_pair_split[1] + " -> " + str(balance[1]))

    await exchange.close()

if __name__ == "__main__":

    EXCHANGE = ccxt.kraken({"verbose": False, "enableRateLimit": True})

    if operating_system().upper() == "WINDOWS":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main(EXCHANGE))
