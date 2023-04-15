import random
import math
import numpy as np
from scipy import stats
from scipy.optimize import minimize
import Tetris


# Initialisation
mu0 = [0]*21
sigma0 = np.diag([100]*21)
V0 = (mu0, sigma0)
parameters = [V0]
thresholds = [-1]

t = 1
T = 2*21
update_rate = 0.8



for j in range (10):


    # Create the distribution
    distribution = stats.multivariate_normal(parameters[t-1][0], parameters[t-1][1])
    

    # Evaluate each parameter pool
    N = 100
    sample_list = []

    sample_mean = []

    for i in range(N):
        
        sample = distribution.rvs()
        score_mean=[]
        for i in range(30):
            score_mean.append(Tetris.simulation_without_graphic(sample))
        print(np.mean(score_mean))

        sample_list.append(sample)
        sample_mean.append(np.mean(score_mean))
        

    # Keeping the 10% highest values
    p = 0.9

    sample_mean = np.array(sorted(sample_mean))
    quantile = np.quantile(sample_mean, 1 - p)
    indices = np.where(sample_mean >= quantile)[0]
    S_high = sample_mean[indices]
    sample_high = [sample_list[i] for i in indices]

   
    print(S_high)

    print(S_high[0])
    print(S_high[-1])

    # New parameter estimation using MLE


    mean = np.mean(sample_high, axis = 0)
    cov =  np.cov(sample_high, rowvar = False)
    res = (mean, cov)

  
    alpha = 0.4
    parameters.append((alpha * np.array(res[0]) + (1 - alpha) * np.array(parameters[-1][0]),
                       alpha ** 2 * np.array(res[1]) + (1 - alpha) ** 2 * np.array(parameters[-1][1])))

    #Update
    T = T * update_rate
    t +=1

# Result

mean_result = parameters[-1][0]
sample_result = stats.multivariate_normal(parameters[-1][0],parameters[-1][1]).rvs()