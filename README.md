# Learning Tetris using the noisy Cross Entropy method
Project conducted as part of the second year Monte Carlo course at ENSAE.
## Main idea 
The cross-entropy method is an efficient and general optimization algorithm. However, its applicability in reinforcement learning seems to be limited although it is fast, because it often converges to suboptimal policies. A standard technique for preventing early convergence is to introduce noise. We apply the noisy cross-entropy method to the game of Tetris to demonstrate its efficiency.
# Tetris controller
Following the approach of Thiery and Scherrer [2], we shall learn state-value functions that are linear combination of 21 basis functions.

| Feature  | Id | Description  | Comments |
| ------------- | ------------- | ------------- | ------------- |
| Column height   | $h_p$ | Height of the $p$ th column of the board  | There are $P$ such features where $P$ is the board width  |
| Column difference  | $\Delta h_p$  | Absolute difference $\mid h_p − h_{p+1} \mid$ between adjacent columns  | There are $P − 1$ such features where $P$ is the board width  |
| Maximum height  | $L$  | Maximum pile height  | Prevents from having a big pile  |
| Holes  | $H$  | Number of empty cells covered by at least one full cell  | Prevents from making holes  |

The value function : 

$V_w(s):=\sum_{i=1}^{10} w_i \h_i(s) + \sum_{i=1}^{9} w_{10+i} \Delta h_i(s)+ w_20L+w_21H$



# Optimizer
## Cross entropy 
## Cross entropy with constant noise 
## Simulated annealing
# Bibliography 
* [1] [Learning Tetris Using the Noisy Cross-Entropy Method](https://www.researchgate.net/publication/6743957_Learning_Tetris_Using_the_Noisy_Cross-Entropy_Method), I. Szita , A. Lorincz 
* [2] [Improvements on Learning Tetris with Cross Entropy](https://inria.hal.science/inria-00418930/document), Christophe Thiery, Bruno Scherrer, INRIA
* [3] [A Tutorial on the Cross-Entropy Method](https://link.springer.com/article/10.1007/s10479-005-5724-z), Pieter-Tjerk de Boer, Dirk P. Kroese, Shie Mannor, Reuven Y. Rubinstein
# Contacts

* Grégoire Brugère - gregoire.brugere@ensae.fr  
* Léo Stepiens - leo.stepiens@ensae.fr
* Corentin Pla - corentin.pla@ensae.fr  



