"""

Author: Zac King (U1758957)

This Python file is designed to test a more real-time implementation of a neural network, it gathers real-time price
data for a coin (bound to the rate limit of the exchange) and predicts after a certain amount of time has passed, and
then repeats.

The result is shown as a graph at the end.

"""

from sklearn.svm import NuSVR
import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter_ns as stopwatch
import ccxt.async_support as ccxt
import asyncio


async def get_exchange():

    #  Default: ccxt.hitbtc, but Binance has a rate limit of just 50ms for some reason, much faster
    exchange = ccxt.binance({"verbose": False, "enableRateLimit": True})
    await exchange.load_markets(True)

    return exchange


async def get_last_price(exchange, coin_index):

    tick = await exchange.fetch_ticker(exchange.symbols[coin_index])
    last_price = tick.__getitem__("last")

    return last_price


def predict_next_price(price_list):

    data_points = [[i] for i in range(len(price_list))]

    predictive_model = NuSVR(kernel="rbf")
    predictive_model.fit(data_points, price_list)
    predicted_price = predictive_model.predict([[len(data_points) + 1]])

    return predicted_price


def calculate_accuracy(accuracy_dict, previous_real_price, next_real_price, next_predicted_price, is_finished):

    # https://doi.org/10.3390/e21060589
    # Page 7 of 12 gives us a way to evaluate the accuracy of our models

    if is_finished:

        t_p = accuracy_dict["TP"]  # True Positives
        t_n = accuracy_dict["TN"]  # True Negatives
        f_p = accuracy_dict["FP"]  # False Positives
        f_n = accuracy_dict["FN"]  # False Negatives

        accuracy = (t_p + t_n) / (t_p + t_n + f_p + f_n)
        precision = t_p / (t_p + f_p)

        print("Accuracy: " + str(accuracy))
        print("Precision: " + str(precision))
        print()

    else:

        if next_real_price >= previous_real_price and next_predicted_price >= previous_real_price:
            accuracy_dict["TP"] += 1
        elif next_real_price < previous_real_price and next_predicted_price < previous_real_price:
            accuracy_dict["TN"] += 1
        elif next_real_price < previous_real_price <= next_predicted_price:
            accuracy_dict["FP"] += 1
        elif next_real_price >= previous_real_price > next_predicted_price:
            accuracy_dict["FN"] += 1

        print()
        print("Accuracy Tally: " + str(accuracy_dict))


def plot_graph(plot_data, data_points):

    """

    -> RED graph is real-time coin data, default is BTC/USDT.
    -> GREEN graph is predicted coin data at each interval.

    It's a bit spooky how well the prediction works already, it tends to fit the real graph really well!!

    """

    plt.style.use("seaborn-whitegrid")

    x_axis = [x for x in range(len(plot_data[0]))]
    x_axis_predicted_points = []

    i = data_points

    for _ in range(len(plot_data[1])):
        x_axis_predicted_points.append(i)
        i += data_points

    plt.plot(x_axis, np.array(plot_data[0]), color="red")
    plt.plot(x_axis_predicted_points, np.array(plot_data[1]), marker='o', color="green")

    plt.show()


async def main():

    exchange = await get_exchange()

    coin_index = -1
    coin = "ETH/USDT"  # Default: BTC/USDT

    if coin in exchange.symbols:
        coin_index = exchange.symbols.index(coin)
    else:
        print(coin + " not found in exchange!")

    if coin_index > -1:

        accuracy_dict = {"TP": 0,  # True Positive (Model predicts higher, reality is higher)
                         "TN": 0,  # True Negative (Model predicts lower, reality is lower)
                         "FP": 0,  # False Positive (Model predicts higher, reality is lower)
                         "FN": 0}  # False Negative (Model predicts lower, reality is higher)

        data_points = 4  # How many points to gather before training + prediction
                          # Note that the rate limit of HitBTC is 1.5 seconds, so 10 will take 15 seconds!!
                          # Add 1.5 seconds to the end also, for the next real price for comparison.

        prediction_amount = 64  # How many predictions to be made
                                # This is temporary for testing, in the real product this would loop until interrupted
                                # E.g., from the user telling the program to stop

        plot_data = [[], []]

        for n in range(prediction_amount):

            print("Predicting Price " + str(n + 1) + " / " + str(prediction_amount))

            print()  # Empty print to look nice

            price_list = []

            #  It will say, e.g., 11/10, because the last point isn't used in training ..
            #  .. It's used to compare the next real price with the next predicted price.
            for i in range(data_points + 1):
                price_list.append(await get_last_price(exchange, coin_index))
                print("Gathered " + str(i + 1) + " / " + str(data_points) + " ...")

            s_time = stopwatch()

            predicted_price = predict_next_price(price_list[:-1])
            calculate_accuracy(accuracy_dict, price_list[-2], price_list[-1], predicted_price[0], False)

            plot_data[0] += price_list
            plot_data[1].append(predicted_price)

            e_time = stopwatch() - s_time
            e_time /= 1_000_000.0  # Nanoseconds to Milliseconds

            print()  # Empty print to make it look nicer

            print("Current Price List: " + str(price_list))
            print("Next Real Price: " + str(price_list[-1]))
            print("Predicted Real Price: " + str(predicted_price[0]))

            print()  # Empty print to make it look nicer

            print("AI Training & Prediction Time Taken: " + str(e_time) + "ms")

            print()  # Empty print to make it look nicer

        calculate_accuracy(accuracy_dict, 0, 0, 0, True)

        plot_graph(plot_data, data_points + 1)

    await exchange.close()


if __name__ == "__main__":
    asyncio.run(main())
