# Learning Tetris using the noisy Cross Entropy method
Project conducted as part of the second year Monte Carlo course at ENSAE.
## Main idea 
The cross-entropy method is an efficient and general optimization algorithm. However, its applicability in reinforcement learning seems to be limited although it is fast, because it often converges to suboptimal policies. A standard technique for preventing early convergence is to introduce noise. We apply the noisy cross-entropy method to the game of Tetris to demonstrate its efficiency.
# Tetris controller
Following the approach of Thiery and Scherrer [2], we shall learn state-value functions that are linear combination of 21 basis functions.

$$
\begin{array}{|l|l|l|l|}
\hline \text { Feature } & \text { Id } & \text { Description } & \text { Comments } \\
\hline \text { Column height } & h_p & \text { Height of the } p \text { th column of the board } & \begin{array}{l}
\text { There are } P \text { such features } \\
\text { where } P \text { is the board width }
\end{array} \\
\hline \text { Column difference } & \Delta h_p & \begin{array}{l}
\text { Absolute difference }\left|h_p-h_{p+1}\right| \text { be- } \\
\text { tween adjacent columns }
\end{array} & \begin{array}{l}
\text { There are } P-1 \text { such features } \\
\text { where } P \text { is the board width }
\end{array} \\
\hline \text { Maximum height } & H & \text { Maximum pile height: } \max _p h_p & \text { Prevents from having a big pile } \\
\hline \text { Holes } & L & \begin{array}{l}
\text { Number of empty cells covered by at } \\
\text { least one full cell }
\end{array} & \text { Prevents from making holes } \\
\hline
\end{array}
$$

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



