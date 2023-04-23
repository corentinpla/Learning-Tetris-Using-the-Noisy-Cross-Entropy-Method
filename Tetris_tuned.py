import Tetris as T
import numpy
import random
import copy 

def depht_holes(field): #somme du nombre de cellules pleines au-dessus de chaque trou
    L=0
    h=column_height(field)

    for j in range(10):
        for i in range(20-h[j],20):
            if field[i][j]==0:
                L+=i-(20-h[j]) #profondeur du trou
    
    return(L)

def line_with_holes(field): #retourne le nombre de lignes avec des trous
    L=[]
    h=column_height(field)

    for j in range(10):
        for i in range(20-h[j],20):
            if field[i][j]==0 and i not in L:
                L.append(i)
    
    return(len(L))

def evaluate_tuned(W, field): 
    #W=[w1, ..., w23] vector of parameters to tune 

    h=T.column_height(field)
    dh=T.column_difference(field)
    L=T.holes(field)
    H=T.maximum_height(field)
    D=depht_holes(field)
    LWH=line_with_holes(field)
    
    S1,S2,S3,S4=0,0,0,0

    for k in range (len(h)):
        S1+=h[k]*W[k]
    
    for k in range (len(dh)):
        S2+=dh[k]*W[10+k]

    S3=W[19]*L

    S4=W[20]*H

    S5=W[21]*D

    S6=W[22]*LWH

    return(S1+S2+S3+S4+S5+S6)