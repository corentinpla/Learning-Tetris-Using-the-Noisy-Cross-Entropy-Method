import random
import math
import numpy as np
from scipy import stats
import sys
sys.path.append("/home/leo/Programmation/Python/MonteCarlo")
from scipy.optimize import minimize
import Tetris

# Initialisation
mu0 = [5]*21
sigma0 = np.diag([100]*21)
V0 = (mu0, sigma0)
parameters = [V0]
thresholds = [-1]
d = 6
t = 1
T = 2*21
update_rate = 0.8

# Test
#def evaluate(S):
#    return sum([abs(x) for x in S])

def last_d_values_equal(lst, d):
    if len(lst) < d:
        return False
    return len(set(lst[-d:])) == 1


while not last_d_values_equal(thresholds,d):


    # Create the distribution
    distribution = stats.multivariate_normal(parameters[t-1][0], parameters[t-1][1])
    #Create a perturbation for simulated annealing
    width = np.max(parameters[t-1][1]) / 10
    perturbation = stats.multivariate_normal([0]*21, np.diag([width]*21))

    # Evaluate each parameter pool
    N = 100
    sample_list = []
    sample_perturbated_list = []
    S_list = []
    S_perturbated_list = []
    for i in range(N):
        sample = distribution.rvs()
        sample_perturbated = sample + perturbation.rvs()
        sample_list.append(sample)
        sample_perturbated_list.append(sample_perturbated)
        S_list.append(Tetris.simulation_without_graphic(sample))
        S_perturbated_list.append(Tetris.simulation_without_graphic(sample_perturbated))

    # Keeping the 10% highest values
    p = 0.9

    S_list = np.array(sorted(S_list))
    quantile = np.quantile(S_list, 1 - p)
    indices = np.where(S_list >= quantile)[0]
    S_high = S_list[indices]
    sample_high = [sample_list[i] for i in indices]

    S_perturbated_list = np.array(sorted(S_perturbated_list))
    quantile = np.quantile(S_perturbated_list, 1 - p)
    indices = np.where(S_perturbated_list >= quantile)[0]
    S_perturbated_high = S_perturbated_list[indices]
    sample_perturbated_high = [sample_perturbated_list[i] for i in indices]

    #Comparison for simulated annealing
    theta = np.mean(S_high) - np.mean(S_perturbated_high)
    if theta < 0:
        S = S_perturbated_high
        sample = sample_perturbated_high
    else:
        p = math.exp(-theta/T)
        u = random.random()
        if u < p:
            S = S_perturbated_high
            sample = sample_perturbated_high
        else:
            S = S_high
            sample = sample_high

    print(S[0])
    print(S[-1])

    # New parameter estimation using MLE

    thresholds.append(int(S[0]))
    mean = np.mean(sample, axis = 0)
    cov =  np.cov(sample, rowvar = False)
    res = (mean, cov)

    #def fct_to_opt (parameter):
    #    mean_vector = parameter[:21]
    #    cov_matrix = parameter[21:].reshape((21, 21))
    #    dis = stats.multivariate_normal(mean_vector, cov_matrix)
    #    expression = 0
    #    for j in range(len(S_high)):
    #        expression += np.log(dis.pdf(sample_high[j]))
    #    expression = expression * (1/N)
    #    return -expression

    #x0 = np.concatenate((parameters[t-1][0], parameters[t-1][1].flatten()))
    #opt_res = minimize(fct_to_opt, x0)

    # Smoothing parameter and decay
    decay = np.diag([max(5 - t/10, 0)]*21)
    alpha = 0.4
    parameters.append((alpha * np.array(res[0]) + (1 - alpha) * np.array(parameters[-1][0]),
                       alpha ** 2 * np.array(res[1]) + (1 - alpha) ** 2 * np.array(parameters[-1][1]) + decay))

    #Update
    T = T * update_rate
    t +=1

# Result

mean_result = parameters[-1][0]
sample_result = stats.multivariate_normal(parameters[-1][0],parameters[-1][1]).rvs()