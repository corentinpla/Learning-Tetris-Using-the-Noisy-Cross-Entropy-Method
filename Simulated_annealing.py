import random
import math
import numpy as np
from scipy import stats
import Tetris



def simulation_SA(alpha, update_rate, N_mean, N_iteration, rho, output_file):


    # Initialisation
    mu0 = [0]*21
    sigma0 = np.diag([100]*21)
    V0 = (mu0, sigma0)
    parameters = [V0]
    t = 1
    T = 2*21
    L_plot = []
    L_norm = []



    for j in range(N_iteration):


        # Create the distribution
        distribution = stats.multivariate_normal(parameters[t-1][0], parameters[t-1][1], allow_singular=True)
        #Create a perturbation for simulated annealing
        perturbation = stats.multivariate_normal([0]*21, np.diag([10]*21))

        # Evaluate each parameter pool
        N = 100
        sample_list = []
        sample_perturbated_list = []
        sample_score = []
        sample_pertubated_score = []
        for i in range(N):
            sample = distribution.rvs() #Original sample
            sample_perturbated = sample + perturbation.rvs() #Perturbated sample
            sample_list.append(sample)
            sample_perturbated_list.append(sample_perturbated)
            sample_score.append(Tetris.simulation_without_graphic(sample))
            sample_pertubated_score.append(Tetris.simulation_without_graphic(sample_perturbated))

        # Keeping the 10% highest values
        k = math.floor(N*rho)

        indices=sorted(range(len(sample_score)), key=lambda i: sample_score[i], reverse=True)[:k]
        sample_high = [sample_list[i] for i in indices]

        indices=sorted(range(len(sample_pertubated_score)), key=lambda i: sample_pertubated_score[i], reverse=True)[:k]
        sample_perturbated_high = [sample_perturbated_list[i] for i in indices]

        #Comparison for simulated annealing
        theta = np.mean(sample_high) - np.mean(sample_perturbated_high)
        if theta < 0:
            sample = sample_perturbated_high
        else:
            p = math.exp(-theta/T)
            u = random.random()
            if u < p:
                sample = sample_perturbated_high
            else:
                sample = sample_high

        # New parameter estimation using MLE

        mean = np.mean(sample, axis = 0)
        cov =  np.cov(sample, rowvar = False, bias=True)
        res = (mean, cov)

        L_norm.append(np.linalg.norm(cov))

        # Smoothing parameter
        parameters.append((alpha * np.array(res[0]) + (1 - alpha) * np.array(parameters[-1][0]),
                       alpha ** 2 * np.array(res[1]) + (1 - alpha) ** 2 * np.array(parameters[-1][1])))

        #Test the new on 30 games
        new_score = []
        for i in range(N_mean):
            new_score.append(Tetris.simulation_without_graphic(parameters[-1][0]))
        print(np.mean(new_score))

        L_plot.append(np.mean(new_score))
        #Update
        T = T * update_rate
        t +=1

    return (L_plot, L_norm, mean)
