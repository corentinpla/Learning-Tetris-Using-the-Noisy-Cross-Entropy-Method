# Learning Tetris using the noisy Cross Entropy method
Project conducted as part of the second year Monte Carlo course at ENSAE. Most of the explanations belows are extracts from preexisting articles (see bibliography), however, the code and the results are ours.
## Main idea 
The cross-entropy method is an efficient and general optimization algorithm. However, its applicability in reinforcement learning seems to be limited although it is fast, because it often converges to suboptimal policies. A standard technique for preventing early convergence is to introduce noise. We apply the noisy cross-entropy method to the game of Tetris to demonstrate its efficiency.
## Code
* `Tetris.py` implements the Tetris game and the state-value functions.
* `Tetris_tuned.py` proposes two more features to integrate in the state-value function (depht of the holes & numbers of lines with holes) as it is proposed by [2]. 
* `CE_method.py` implements the classical cross-entropy method optimizer.
* `CE_method_with_noise.py` implements the Noisy cross-entropy method (constant & decreasing noise).
* `Simulated_annealing.py` implements the simulated annealing optimizer. 
# Tetris controller
Following the approach of Thiery and Scherrer [2], we shall learn state-value functions that are linear combination of 21 basis functions.

| Feature  | Id | Description  | Comments |
| ------------- | ------------- | ------------- | ------------- |
| Column height   | $h_p$ | Height of the $p$ th column of the board  | There are $P$ such features where $P$ is the board width  |
| Column difference  | $\Delta h_p$  | Absolute difference $\mid h_p − h_{p+1} \mid$ between adjacent columns  | There are $P − 1$ such features where $P$ is the board width  |
| Maximum height  | $L$  | Maximum pile height  | Prevents from having a big pile  |
| Holes  | $H$  | Number of empty cells covered by at least one full cell  | Prevents from making holes  |

The value function to optimise: 

$$
V_w(s):=\sum_{i=1}^{10} w_i h_i(s) + \sum_{i=1}^{9} w_{10+i}\Delta h_i(s) + w_{20}L + w_{21}H
$$

where $s$ denotes a Tetris state and $w=(w_1,w_2,...,w_{21})$ the weight under which optimize.


**One of our Tetris simulation for an optimised weight vector (for gif generator see `Tetris.py`) :**

![](https://github.com/corentinpla/Learning-Tetris-Using-the-Noisy-Cross-Entropy-Method/blob/main/figures/Tetris.gif)


# Optimizer
## Cross entropy 
### Presentation
An interesting illustration to understand this principle for $w=(w_1,w_2)$ is proposed in this [repo](https://github.com/amundim/cross_entropy_optimization) :
* The red crosses : the 10 best vectors we select and use to estimate next round $\mathcal{N}\left(\mu, \sigma^2\right)$
* The black dots : the next round 100 vectors we generate and test 
![](https://github.com/corentinpla/Learning-Tetris-Using-the-Noisy-Cross-Entropy-Method/blob/main/figures/cross_entropy_optimization.gif)

### Results 
![](https://github.com/corentinpla/Learning-Tetris-Using-the-Noisy-Cross-Entropy-Method/blob/main/figures/simulation%20CE(1%2C%20100%2C0.1%2C5%2C100).png)


## Cross entropy with constant noise 
### Presentation

### Results 
![](https://github.com/corentinpla/Learning-Tetris-Using-the-Noisy-Cross-Entropy-Method/blob/main/figures/simulation%20CE%20const%20noise(1%2C%20100.0.1.5.100)-2.png)


## Cross entropy with decreasing noise 
### Presentation

### Results 
![](https://github.com/corentinpla/Learning-Tetris-Using-the-Noisy-Cross-Entropy-Method/blob/main/figures/simulation_CE_deacr_noise(1%2C100%2C0.1%2C5%2C100).png)
<p align="center">
  <img src="https://github.com/corentinpla/Learning-Tetris-Using-the-Noisy-Cross-Entropy-Method/blob/main/figures/comparaison_of_the_3_opti.png"/>
</p>


# Further improvements
* Try a two pieces Tetris controller 
* Use new features in the controller 
* Optimize the hyperparameters
* Simulated annealing optimizer

# Bibliography 
* [1] [Learning Tetris Using the Noisy Cross-Entropy Method](https://www.researchgate.net/publication/6743957_Learning_Tetris_Using_the_Noisy_Cross-Entropy_Method), I. Szita , A. Lorincz 
* [2] [Improvements on Learning Tetris with Cross Entropy](https://inria.hal.science/inria-00418930/document), Christophe Thiery, Bruno Scherrer, INRIA
* [3] [A Tutorial on the Cross-Entropy Method](https://link.springer.com/article/10.1007/s10479-005-5724-z), Pieter-Tjerk de Boer, Dirk P. Kroese, Shie Mannor, Reuven Y. Rubinstein



# Contacts

* Grégoire Brugère - gregoire.brugere@ensae.fr  
* Léo Stepiens - leo.stepiens@ensae.fr
* Corentin Pla - corentin.pla@ensae.fr  



