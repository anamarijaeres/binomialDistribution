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
        sum_of = 0
        x = np.arange(0, n + 1)
        binomial_pmf = binom.pmf(x, n, p)


        for i in range(0, n + 1):
            xi = np.arange(0, i+1)

            plt.plot(x, binomial_pmf, color='blue')
            plt.title(f"Binomial Distribution (n={n}, p={p})")
            plt.fill_between(xi, binomial_pmf[0 : i+1], color='pink', alpha=0.4)
            plt.show()
            sum_of += binomial_pmf[i]
            if sum_of >= 0.95:
                #i instead of n-i
                n = n - i
                if n!=0:
                    array_lower_bound.append(i)
                break
            print(sum_of)

    # read values
    p = config.getfloat('RunParams', 'p')
    n = config.getint('RunParams', 'n')
    smallest_possible_window = False
    dict={}
    while n > 0:
        sum_of = 0
        prev_n = n
        x = np.arange(0, n + 1)
        binomial_pmf = binom.pmf(x, n, 1-p)
        for i in range(0, n + 1):
            sum_of += binomial_pmf[i]

            if sum_of >= 0.95:
                xi = np.arange(0, i + 1)
                plt.plot(x, binomial_pmf, color='blue')
                plt.title(f"Binomial Distribution (n={n}, p={p})")
                plt.fill_between(xi, binomial_pmf[0: i + 1], color='pink', alpha=0.4)
                plt.show()
                #i instead of n-i
                n = i
                if n == prev_n:
                    sum_of-=binomial_pmf[i]
                    smallest_possible_window = True
                    n = n - 1
                    dict[sum_of] = n

                    xi = np.arange(0, n+1)
                    plt.plot(x, binomial_pmf, color='blue')
                    plt.title(f"Binomial Distribution (n={n+1}, p={p})")
                    plt.fill_between(xi, binomial_pmf[0: n+ 1], color='pink', alpha=0.4)
                    plt.show()
                    break
                array_upper_bound.append(i)
                break





    while n > 0:
        sum_of = 0
        prev_n = n
        x = np.arange(0, n + 1)
        binomial_pmf = binom.pmf(x, n, p)
        for i in range(0, n + 1):
            sum_of += binomial_pmf[i]
            print(sum_of)
            if sum_of > 0.05:
                n = n - i
                if n == prev_n:
                    smallest_possible_window = True
                    n=n-1
                    dict[1-sum_of]=n
                    break
                array_upper_bound.append(i)
                break

    n = config.getint('RunParams', 'n')
    no_of_cols_max = 0
    for i in range(0, len(array_upper_bound)):
        no_of_cols_max += n- array_upper_bound[i]

    no_of_cols_min = 0
    n = config.getint('RunParams', 'n')

    sum_fornow=0
    done=False
    for i in range(0, len(array_lower_bound)-1):
        for j in range(0, i + 1):
            if i+1==len(array_lower_bound):
                break
            no_of_cols_min += array_lower_bound[j]
        if done:
            break

    no_of_cols_max_less_certain=0
    sum_upper_array=sum(array_upper_bound)

    n = config.getint('RunParams', 'n')
    for i in dict.values():
        if i!=0:
            no_of_cols_max_less_certain+=n-i

    no_of_cols_max_less_certain+=no_of_cols_max


