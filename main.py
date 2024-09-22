import random
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.integrate import quad

def basicMonteCarlo(currentPrice, strike, numIter, volatility, numSims):
    sum = 0
    finalPrices = []

    for i in range(numSims):
        price = currentPrice
        for i in range(numIter):
            if random.random() < 0.5:
                price += volatility
            else:
                price -= volatility

        sum += max(0, price-strike)
        finalPrices.append(price)

    sum /= numSims
    print("Standard Dev: " + str(findStd(finalPrices, findAvg(finalPrices))))
    plt.hist(finalPrices, bins=range(min(finalPrices), max(finalPrices) + 2), edgecolor='black', align='left')

    # Add titles and labels
    plt.title('Histogram of Number Frequencies')
    plt.xlabel('Number')
    plt.ylabel('Frequency')

    # Display the plot
    return sum

def func(x, mean, std_dev):
    """Probability Density Function of the Gaussian distribution."""
    return 1 / (math.sqrt(2 * math.pi * std_dev**2)) * np.exp(-((x - mean)**2) / (2 * std_dev**2))

def findAvg(list):
    sum = 0
    for num in list:
        sum += num
    return sum / len(list)

def findStd(list, avg):
    sum = 0
    for num in list:
        sum += abs(num-avg)
    return sum / len(list)

def binomialEst(currentPrice, strike, numIter, volatility):
    standardDeviation = math.sqrt(numIter*.25) * volatility * 2
    # standardDeviation = 127.25803540000038
    # setting the x - coordinates
    x = np.arange(currentPrice - 3 * standardDeviation, currentPrice + 3 * standardDeviation, 0.1)
    # setting the corresponding y - coordinates
    y = func(x, currentPrice, standardDeviation) * 900000

    # plotting the points
    plt.fill_between(x, y, where=(x >= strike), color='green', alpha=0.5, label='Above strike')

    # Adding labels and legend
    plt.xlabel('Price')
    plt.ylabel('Probability Density')
    plt.title('Chances of Final Price')
    plt.legend()
    plt.plot(x, y)

    # function to show the plot
    result, error = quad(lambda x: func(x, currentPrice, standardDeviation) * (x-strike), strike, currentPrice + 20 * standardDeviation)

    return result


print(binomialEst(1000, 1100, 1000, 5))
print(basicMonteCarlo(1000, 1100, 1000, 5, 90000))
plt.show()