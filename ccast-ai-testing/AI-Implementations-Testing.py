"""

Author: Zac King (U1758957)

This Python file is designed to load the price history text file, predict the next price using AI
and/or machine learning, and graph the output for nicer visualisation.

Implement as many different AIs and/or machine learning algorithms as you want and test them all here.

"""

from sklearn.svm import SVR, NuSVR
import matplotlib.pyplot as plt
import numpy as np
from random import randint


def predict_price_svr():
    pass


def predict_price_nusvr():
    pass


# # # AI/Machine Learning implementations go above here... # # #


def plot_graph():
    pass


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


if __name__ == "__main__":
    main()
