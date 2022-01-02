"""

Author: Zac King (U1758957)

This Python file is designed to load the price history text file, predict the next price using AI
and/or machine learning, and graph the output for nicer visualisation.

Implement as many different AIs and/or machine learning algorithms as you want and test them all here.

"""
import numpy
from sklearn.svm import SVR, NuSVR
import matplotlib.pyplot as plt
import numpy as np
from random import randint


def predict_price_svr(price_history):

    """

    Performs a Support Vector Regression on price_history to predict the next price

    :param price_history: the price history list
    :return: a predicted price based on the price history
    """

    data_points = [[i] for i in range(len(price_history))]  # 2D list of data points for SVR (i.e., [[0], [1], [2], ..]

    support_vector_regression = SVR(kernel="rbf")  # Possible kernels are rbf, poly, and linear

    support_vector_regression.fit(data_points, price_history)  # This is the training of the AI

    # This is the prediction of the next data point. For example, if data_point was kept at 32, the AI just trained ..
    # .. on 32 prices, and you are now asking the AI to predict the 33rd data point (aka the next price).
    predicted_price = support_vector_regression.predict([[len(data_points) + 1]])

    #  the predict() function returns a Numpy array of length 1, so returning the 0th index is needed here
    return predicted_price[0]


def predict_price_nusvr():
    pass


# # # AI/Machine Learning implementations go above here... # # #


def plot_graph(plot_data):

    plt.style.use("seaborn-whitegrid")

    print("Price History: " + str(plot_data[0]))  # Index 0 is the original price history used for training
    print("Next (Real) Price: " + str(plot_data[1]))  # Index 1 is the next real price after price history
    print("Next (Predicted) Price: " + str(plot_data[2]))  # Index 2 is the next predicted price after price history

    x_axis = [x for x in range(len(plot_data[0]) + 1)]  # The y-axis is all the price stuff

    plt.plot(x_axis[:-1], np.array(plot_data[0]), color="red")  # Price History is a red line chart on the graph
    plt.scatter(x_axis[-1], np.array(plot_data[1]), color="green")  # Real next price is a green point on the plot
    plt.scatter(x_axis[-1], np.array(plot_data[2]), color="blue")  # Predicted next price is a blue point on the plot

    plt.annotate("Real", (x_axis[-1], np.array(plot_data[1])))
    plt.annotate("Predicted", (x_axis[-1], np.array(plot_data[2])))

    plt.show()


def load_price_file():

    """

    Opens the price.txt file and builds the price history list

    :return: a list of prices
    """

    price_history = []

    with open("price.txt", "r") as txt_file:
        lines = txt_file.readlines()
        for line in lines:
            price_history.append(float(line))

    return price_history


def main():

    price_history = load_price_file()
    plot_data = []

    data_points = 32  # Of the price history, how many points of data to use (e.g., 32 out of the 720).
                      # This is used for the AI to train/predict

    # Random starting point in the price history list
    rnd_start_index = randint(0, len(price_history) - data_points)

    # Choosing a random range of price_history that is data_points + 1 long
    # The +1 is so the real next price can be compared to the predicted next price later on
    price_history = price_history[rnd_start_index:rnd_start_index + data_points + 1]

    plot_data.append(price_history[:-1])  # Leave out the very last index for plotting ..
    plot_data.append([price_history[-1]])  # .. As it is plotted independently here

    price_history = price_history[:-1]  # Price history can now be just data_points long

    # # # Calls to AI/ML functions go below here # # #
    # # Uncomment the one AI being tested and comment out all the rest # #

    predicted_price = predict_price_svr(price_history)
    # predicted_price = predict_price_nusvr()

    # # # Calls to AI/ML functions go above here # # #

    plot_data.append([predicted_price])
    plot_graph(plot_data)


if __name__ == "__main__":
    main()
