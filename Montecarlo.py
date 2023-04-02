import numpy as np
from scipy import stats
import sys
sys.path.append("/home/leo/Programmation/Python/MonteCarlo")
from scipy.optimize import minimize
import Tetris_final as Tetris
# Initialisation
mu0 = [5]*21
sigma0 = np.diag([100]*21)
V0 = (mu0, sigma0)
parameters = [V0]
thresholds = [-1]
d = 100
t = 1

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

    # Evaluate each parameter pool
    N = 100
    sample_list = []
    S_list = []
    for i in range(N):
        sample = distribution.rvs()
        sample_list.append(sample)
        S_list.append(Tetris.simulation_without_graphic(sample))

    # Keeping the 10% highest values
    p = 0.9

    S_list = np.array(sorted(S_list))
    quantile = np.quantile(S_list, 1 - p)
    indices = np.where(S_list >= quantile)[0]
    S_high = S_list[indices]
    sample_high = [sample_list[i] for i in indices]
    thresholds.append(int(S_high[0]))


    # New parameter estimation using MLE

    mean = np.mean(sample_high, axis = 0)
    cov =  np.cov(sample_high, rowvar = False)
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

    # Smoothing parameter
    alpha = 0.4
    parameters.append((alpha * np.array(res[0]) + (1 - alpha) * np.array(parameters[-1][0]),
                       alpha ** 2 * np.array(res[1]) + (1 - alpha) ** 2 * np.array(parameters[-1][1])))

    print(parameters[-1], thresholds[-1])
    t +=1

# Result

mean_result = parameters[-1][0]
sample_result = stats.multivariate_normal(parameters[-1][0],parameters[-1][1]).rvs()