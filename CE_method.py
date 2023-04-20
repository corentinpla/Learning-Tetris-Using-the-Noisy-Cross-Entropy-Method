import random
import math
import numpy as np
from scipy import stats
from scipy.optimize import minimize
import Tetris
import matplotlib.pyplot as plt



def simulation_CE(alpha, N_iteration,rho): #alpha : taux d'actualistion 
                              
                               #N_iteration : nombre d'iterations
                               #rho : the fraction of verctors that are selected
                               #retourne L_plot : le score maximal par itération
    
    # Initialisation
    mu0 = [5]*21
    sigma0 = np.diag([100]*21)
    V0 = (mu0, sigma0)
    parameters = [V0]
    t=1
    L_plot=[]

    for j in range (N_iteration):


        # Create the distribution
        distribution = stats.multivariate_normal(parameters[t-1][0], parameters[t-1][1],allow_singular=True)
        

        # Evaluate each parameter pool
        N = 100
        sample_list = []
        sample_score = []

        for i in range(N):
            
            sample = distribution.rvs() #vecteur de paramètre W
            

            sample_score.append(Tetris.simulation_without_graphic(sample))
            sample_list.append(sample)
            

        # Keeping the rho*N bests vectors
        k=math.floor(N*rho)

        indices=sorted(range(len(sample_score)), key=lambda i: sample_score[i], reverse=True)[:k]
        sample_high = [sample_list[i] for i in indices]
        best_sample=sample_list[indices[0]]

        # New parameter estimation using MLE

        mean = np.mean(sample_high, axis = 0)
        cov =  np.cov(sample_high, rowvar = False,bias=True)

        res = (mean, cov)
        print(np.linalg.norm(cov))

        parameters.append((alpha * np.array(res[0]) + (1 - alpha) * np.array(parameters[-1][0]),
                        alpha ** 2 * np.array(res[1]) + (1 - alpha) ** 2 * np.array(parameters[-1][1])))    

        for k in range (30):
            L_mean.append(Tetris.simulation_without_graphic(best_sample))


        L_plot.append(np.mean(L_mean))
        t+=1
    
    return(L_plot,(mean, cov))

