import random
import math
import numpy as np
from scipy import stats
from scipy.optimize import minimize
import Tetris


def simulation_CE_const_noise(alpha, N_mean, N_iteration,rho,noise): #alpha : taux d'actualistion 
                               #N_mean: nombre de simulation par vecteur
                               #N_iteration : nombre d'iterations
                               #rho : the fraction of verctors that are selected
                               #retourne L_plot : le score maximal par itération
                               #noise : value of the constant noise to add 
                               
    # Initialisation
    mu0 = [0]*21
    sigma0 = np.diag([100]*21)
    V0 = (mu0, sigma0)
    parameters = [V0]
    L_plot=[]


    for j in range (N_iteration):


        # Create the distribution
        distribution = stats.multivariate_normal(parameters[t-1][0], parameters[t-1][1])
        

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
            

        # Keeping the rho*N bests vectors
        k=floor(N*rho)

        indices=sorted(range(len(sample_mean)), key=lambda i: sample_mean[i], reverse=True)[:k]
        sample_high = [sample_list[i] for i in indices]
    

        # New parameter estimation using MLE


        mean = np.mean(sample_high, axis = 0)
        cov =  np.cov(sample_high, rowvar = False)
        res = (mean, cov)
        print(res)

        #add noise 

        matrix_noise = np.diag([noise]*21)

        parameters.append((alpha * np.array(res[0]) + (1 - alpha) * np.array(parameters[-1][0]),
                        alpha ** 2 * np.array(res[1]) + (1 - alpha) ** 2 * np.array(parameters[-1][1])+matrix_noise))    

        L_plot.append(max(sample_mean))
    
    return(L_plot,(mean, cov))


def simulation_CE_deacr_noise(alpha, N_mean, N_iteration,rho,a,b): #alpha : taux d'actualistion 
                                   #N_mean: nombre de simulation par vecteur
                                   #N_iteration : nombre d'iterations
                                   #rho : the fraction of verctors that are selected
                                   #retourne L_plot : le score maximal par itération
                                   #noise : value of the constant noise to add
                                   #a,b : params of the decreasing noise, a=5 , b=100 in the paper

    # Initialisation
    mu0 = [0]*21
    sigma0 = np.diag([100]*21)
    V0 = (mu0, sigma0)
    parameters = [V0]
    L_plot=[]


    for j in range (N_iteration):


        # Create the distribution
        distribution = stats.multivariate_normal(parameters[t-1][0], parameters[t-1][1])
        

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
            

        # Keeping the rho*N bests vectors
        k=floor(N*rho)

        indices=sorted(range(len(sample_mean)), key=lambda i: sample_mean[i], reverse=True)[:k]
        sample_high = [sample_list[i] for i in indices]
    

        # New parameter estimation using MLE


        mean = np.mean(sample_high, axis = 0)
        cov =  np.cov(sample_high, rowvar = False)
        res = (mean, cov)
        print(res)

        #add noise 
        noise = max(0, a-n/b)

        matrix_noise = np.diag([noise]*21)

        parameters.append((alpha * np.array(res[0]) + (1 - alpha) * np.array(parameters[-1][0]),
                        alpha ** 2 * np.array(res[1]) + (1 - alpha) ** 2 * np.array(parameters[-1][1])+matrix_noise))    

        L_plot.append(max(sample_mean))
    
    return(L_plot,(mean, cov))