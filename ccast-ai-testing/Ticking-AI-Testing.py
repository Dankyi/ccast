"""

Author: Zac King (U1758957)

This Python file is designed to test a more real-time implementation of a neural network, it gathers real-time price
data for a coin (bound to the rate limit of the exchange) and predicts after a certain amount of time has passed, and
then repeats.

"""

from sklearn.neural_network import MLPRegressor
import numpy as np
import matplotlib.pyplot as plt
import ccxt.async_support as ccxt
import asyncio


async def get_exchange():

    exchange = ccxt.hitbtc({"verbose": False, "enableRateLimit": True})
    await exchange.load_markets(True)

    return exchange


async def get_last_price(exchange, coin_index):

    tick = await exchange.fetch_ticker(exchange.symbols[coin_index])
    last_price = tick.__getitem__("last")

    return last_price


def predict_next_price(price_list):

    data_points = [[i] for i in range(len(price_list))]

    ml_perceptron = MLPRegressor(solver="lbfgs", hidden_layer_sizes=(8, 2), activation="relu")
    ml_perceptron.fit(data_points, price_list)
    predicted_price = ml_perceptron.predict([[len(data_points) + 1]])

    return predicted_price


async def main():

    exchange = await get_exchange()

    coin_index = -1
    coin = "BTC/USDT"

    if coin in exchange.symbols:
        coin_index = exchange.symbols.index(coin)
    else:
        print(coin + " not found in exchange!")

    if coin_index > -1:

        data_points = 10  # How many points to gather before training + prediction
                          # Note that the rate limit of HitBTC is 1.5 seconds, so 10 will take 15 seconds!!
                          # Add 1.5 seconds to the end also, for the next real price for comparison.

        prediction_amount = 10  # How many predictions to be made
                                # This is temporary for testing, in the real product this would loop until interrupted
                                # E.g., from the user telling the program to stop

        for _ in range(prediction_amount):

            price_list = []

            for i in range(data_points + 1):
                price_list.append(await get_last_price(exchange, coin_index))
                print("Gathered " + str(i + 1) + " / " + str(data_points + 1) + " ...")

            predicted_price = predict_next_price(price_list[:-1])

            print()  # Empty print to make it look nicer

            print("Current Price List: " + str(price_list))
            print("Next Real Price: " + str(price_list[-1]))
            print("Predicted Real Price: " + str(predicted_price))

            print()  # Empty print to make it look nicer

    await exchange.close()


if __name__ == "__main__":
    asyncio.run(main())
