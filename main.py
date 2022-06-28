import configparser
import math

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

if __name__ == '__main__':

    # instantiate parser for reading config file
    config = configparser.ConfigParser()

    # parse config.ini file
    config.read('config.ini')

    # read values
    p = config.getfloat('RunParams', 'p')
    n = config.getint('RunParams', 'n')

    sum_of = 0
    array_lower_bound = []
    array_upper_bound = []
    while n > 0:
        # new iteration of the algorithm
        sum_of = 0
        x = np.arange(0, n + 1)

        binomial_pmf = binom.pmf(x, n, p)

        # finding the maximum number of successes
        for i in range(0, n + 1):
       

            # summing to check if binominal distributions from x = 0 to x = i sum to the probability that is greater
            # than 95%
            sum_of += binomial_pmf[i]
            if sum_of >= 0.95:
                xi = np.arange(0, i + 1)

                 # plotting binomial distribution for x = 0 to x = i
                plt.plot(x, binomial_pmf, color='blue')
                plt.title(f"Binomial Distribution (n={n}, p={p})")
                plt.fill_between(xi, binomial_pmf[0: i + 1], color='pink', alpha=0.4)
                plt.show()
                # i instead of n-i
                # set the new widow size n to n - maximum_successes
                n = n - i
                if n != 0:
                    # append maximum number of successes for each iteration/window size n for later calculation of
                    # minimum number of errors
                    array_lower_bound.append(i)
                break  # n == 0 , the calculation of the lower bound is finished
            #print(sum_of)

    # read values since I have to reset initial value of n to failure_locktime
    p = config.getfloat('RunParams', 'p')
    n = config.getint('RunParams', 'n')

    # keeping track of the number of errors determined in the iterations where I was certain less than 95%
    less_certain_numberOfFailures = {}
    while n > 0:
        sum_of = 0

        prev_n = n
        x = np.arange(0, n + 1)
        # probability of failure is 1-p
        binomial_pmf = binom.pmf(x, n, 1 - p)

        # find maximum errors
        for i in range(0, n + 1):

            sum_of += binomial_pmf[i]

            if sum_of >= 0.95:

                # i instead of n-i
                # set the new widow size n to maximum failures
                n = i
                if n == prev_n:
                    # entering this "if" means that in this iteration my window "n" didn't change from the last
                    # iteration, therefore, I have to start decreasing certainty
                    sum_of -= binomial_pmf[i]


                    # decrease n for 1 and put it in dictionary as new_certainty: n
                    n = n - 1
                    less_certain_numberOfFailures[sum_of] = n

                    # plot to see maximum errors with less certainty
                    xi = np.arange(0, n + 1)
                    plt.plot(x, binomial_pmf, color='blue')
                    plt.title(f"Binomial Distribution (n={n + 1}, p={p})")
                    plt.fill_between(xi, binomial_pmf[0: n + 1], color='pink', alpha=0.4)
                    plt.show()
                    break
                else:
                    # plot only the graph with the maximum number of failures
                    xi = np.arange(0, i + 1)
                    plt.plot(x, binomial_pmf, color='blue')
                    plt.title(f"Binomial Distribution (n={n}, p={p})")
                    plt.fill_between(xi, binomial_pmf[0: i + 1], color='pink', alpha=0.4)
                    plt.show()
                array_upper_bound.append(i)  # for the calculation append the number of successes (because they will
                # cause in the nex iteration the number of collateral errors)
                break  # stop searching for maximum errors number because you found it


    


    #number of collateral errors for the lower bound
    min_number_of_collaterals = 0
    n = config.getint('RunParams', 'n')


    for i in range(0, len(array_lower_bound) - 1):
        for j in range(0, i + 1):
            if i + 1 == len(array_lower_bound):
                break #do this since I am not counting first iteraation as iteration that could possibly have collateral errors, here I am only determining the number of successes and failures in the window
            min_number_of_collaterals += array_lower_bound[j]

    # number of collateral errors for the upper bound is initially 0
    max_number_of_collaterals = 0
    n = config.getint('RunParams', 'n')

    for i in range(0, len(array_upper_bound)):
        max_number_of_collaterals += n - array_upper_bound[i]  # I'm subtracting from initial failure_locktime the maximum number of failures, because every success means collateral error in the next iteration

    #number of collateral errors for the upper bound but with less certainty
    max_number_of_collaterals_less_certain = 0


    n = config.getint('RunParams', 'n') #set n to inital failure_locktime
    for failures in less_certain_numberOfFailures.values():
        if failures != 0: #here I am excluding the last iteration when the number of failures is 0 which means by the definition of collateral errors that from this point onwards only inflight errors will be happening (exactly success locktime inflight errors)
            max_number_of_collaterals_less_certain += n - failures #number of collaterals will be the same as the number of successes from the previous iteration

    max_number_of_collaterals_less_certain += max_number_of_collaterals

    print("Lower bound " + str(min_number_of_collaterals))
    print("Upper bound " + str(max_number_of_collaterals_less_certain))

