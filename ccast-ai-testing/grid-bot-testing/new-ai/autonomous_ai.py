import ccxt.async_support as ccxt
from platform import system as operating_system
import asyncio
from time import sleep

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

        exchange_middleware = middleware.Middleware(16)
        coin_pair_split = coin_pair.split("/")

        async def simulate_buy_and_sell(buy_loops):

            balance = exchange_middleware.get_balance()
            print("Starting Balance: "
                  + coin_pair_split[0] + " -> " + str(balance[0])
                  + " | "
                  + coin_pair_split[1] + " -> " + str(balance[1]))

            for _ in range(buy_loops):

                await exchange_middleware.process_order(exchange, True, coin_pair, coin_pair_id)  # Do a buy!

                balance = exchange_middleware.get_balance()
                print("Buy: "
                      + coin_pair_split[0] + " -> " + str(balance[0])
                      + " | "
                      + coin_pair_split[1] + " -> " + str(balance[1]))

            sleep(5.0)  # Sleep for N seconds in lieu of actually waiting for the price to cross the threshold

            await exchange_middleware.process_order(exchange, False, coin_pair, coin_pair_id)  # Do a sell!

            balance = exchange_middleware.get_balance()
            print("Sell: "
                  + coin_pair_split[0] + " -> " + str(balance[0])
                  + " | "
                  + coin_pair_split[1] + " -> " + str(balance[1]))

        # await simulate_buy_and_sell(3)

    await exchange.close()

if __name__ == "__main__":

    EXCHANGE = ccxt.kraken({"verbose": False, "enableRateLimit": True})

    if operating_system().upper() == "WINDOWS":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main(EXCHANGE))
