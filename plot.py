# For plotting sensitivity analysis, not part of the app.
import numpy as np
import matplotlib.pyplot as plt

from constants import *

def get_x_wait(rho=72000, p_storm=2 / 3, p_mold=0.4, p_lo_acidity=0.2):
    def get_u(x):
        return -np.exp(-x / rho)

    def get_x(u):
        return -rho * np.log(-u)

    u_wait_storm_mold = get_u(x_wait_storm_mold)
    u_wait_storm_no_mold = get_u(x_wait_storm_no_mold)
    u_wait_no_storm_lo_acidity = get_u(x_wait_no_storm_lo_acidity)
    u_wait_no_storm_hi_sugar = get_u(x_wait_no_storm_hi_sugar)
    u_wait_no_storm_lo_sugar = get_u(x_wait_no_storm_lo_sugar)
    u_wait_no_storm_nor_acidity = 0.5 * u_wait_no_storm_hi_sugar + 0.5 * u_wait_no_storm_lo_sugar
    u_wait_storm = p_mold * u_wait_storm_mold + (1 - p_mold) * u_wait_storm_no_mold
    u_wait_no_storm = p_lo_acidity * u_wait_no_storm_lo_acidity + (1 - p_lo_acidity) * u_wait_no_storm_nor_acidity
    u_wait = p_storm * u_wait_storm + (1 - p_storm) * u_wait_no_storm
    return get_x(u_wait)

def plot():
    plt.figure(1, figsize=[10, 6])
    p_storm = np.linspace(0, 1, 100)
    plt.plot(p_storm, get_x_wait(p_storm=p_storm), label='wait')
    plt.hlines(x_harvest, 0, 1, label='harvest')
    plt.xticks(np.linspace(0, 1, 21))
    plt.legend(loc=5)
    plt.xlabel('Probability of storm')
    plt.ylabel('Certain Equivalent ($)')
    plt.show()

    plt.figure(2, figsize=[10, 6])
    p_mold = np.linspace(0, 1, 100)
    plt.plot(p_mold, get_x_wait(p_mold=p_mold), label='wait')
    plt.hlines(x_harvest, 0, 1, label='harvest')
    plt.xticks(np.linspace(0, 1, 21))
    plt.legend(loc=9)
    plt.xlabel('Probability of mold forming if there is a storm')
    plt.ylabel('Certain Equivalent ($)')
    plt.show()

    plt.figure(3, figsize=[10, 6])
    p_lo_acidity = np.linspace(0, 1, 100)
    plt.plot(p_storm, get_x_wait(p_lo_acidity=p_lo_acidity), label='wait')
    plt.hlines(x_harvest, 0, 1, label='harvest')
    plt.legend(loc=5)
    plt.xlabel('Probability of acidity dropping below 20%')
    plt.ylabel('Certain Equivalent ($)')
    plt.show()

    plt.figure(4, figsize=[10, 6])
    gamma = np.linspace(-0.0001, 0.0001, 100)
    rho = 1 / gamma
    plt.plot(gamma, get_x_wait(rho=rho), label='wait')
    plt.hlines(x_harvest, -0.0001, 0.0001, label='harvest')
    plt.legend(loc=5)
    plt.xlabel('Risk aversion coefficient')
    plt.ylabel('Certain Equivalent ($)')
    plt.show()

if __name__ == '__main__':
    plot()