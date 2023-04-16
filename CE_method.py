import random
import math
import numpy as np
from scipy import stats
from scipy.optimize import minimize
import Tetris
import matplotlib.pyplot as plt



def simulation_CE(alpha, N_mean, N_iteration,rho): #alpha : taux d'actualistion 
                               #N_mean: nombre de simulation par vecteur
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
        sample_mean = []

        for i in range(N):
            
            sample = distribution.rvs() #vecteur de paramètre W
            score_mean=[] #liste qui va contenir la moyenne des scores pour W sur N_mean parties

            for i in range(N_mean):
                score_mean.append(Tetris.simulation_without_graphic(sample))

            sample_list.append(sample)
            sample_mean.append(np.mean(score_mean))
            print(np.mean(score_mean))
            

        # Keeping the rho*N bests vectors
        k=math.floor(N*rho)

        indices=sorted(range(len(sample_mean)), key=lambda i: sample_mean[i], reverse=True)[:k]
        sample_high = [sample_list[i] for i in indices]
        print(sample_high)

        # New parameter estimation using MLE


        mean = np.mean(sample_high, axis = 0)
        cov =  np.cov(sample_high, rowvar = False,bias=True)

        res = (mean, cov)
        print(np.linalg.norm(cov))

        parameters.append((alpha * np.array(res[0]) + (1 - alpha) * np.array(parameters[-1][0]),
                        alpha ** 2 * np.array(res[1]) + (1 - alpha) ** 2 * np.array(parameters[-1][1])))    

        L_plot.append(max(sample_mean))
        plt.plot(L_plot)
        plt.show()
        t+=1
    
    return(L_plot,(mean, cov))

def get_mean_from_sample(sample,N_mean):
    L_mean=[]
    for k in range (N_mean):
        L_mean.append(Tetris.simulation_without_graphic(sample))

    return(np.mean(L_mean))

