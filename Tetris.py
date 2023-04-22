import numpy
import random
import copy 
import matplotlib.pyplot as plt


class Figure:
    x = 0
    y = 0
#liste des 6 différentes figures et leur rotation
    figures = [ 
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y, type): 
        self.x = x #position de la pièce sur la largeur du jeu 
        self.y = y #position de la pièce sur la longueur du jeu
        self.type = type #type de la pièce entre 1 et 6
        self.rotation = 0 #rotatio de la pièce

    #séléction de la pièce (type et rotation) dans la liste figures
    def image(self):
        return self.figures[self.type][self.rotation]
    
    #méthode pour faire pivoter la pièce
    def rotate(self,k):
        self.rotation = (self.rotation + k) % len(self.figures[self.type])

class Tetris:
    def __init__(self, height, width): #initialisation du jeu 
        self.score = 0 #score du jeu 
        self.state = "start" #état du jeu (gameover si le jeu est fini)
        self.field = [] # grille de jeu
        self.height = 0 #hauteur du jeu
        self.width = 0 #largeur du jeu 
        self.x = 100
        self.y = 60
        self.figure = None
    
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"

        for i in range(height): # creation de la grille de taille height x width 
            new_line = []

            for j in range(width):
                new_line.append(0)
                
            self.field.append(new_line)

    def new_figure(self,type,x,y):
        self.figure = Figure(x, y,type) #introduction d'une nouvelle figure type en (x,y) 

    def intersects(self): #check if the currently flying figure intersecting with something fixed on the field. 
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection



    def break_lines(self): #checking and detroying full lines
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self,color): #descend la pièce jusqu'en bas 
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze(color)

    def freeze(self,color): #If it moves down and intersects, then this means we have reached the bottom, so we need to “freeze” the figure on our field:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = color
        self.break_lines()

    def go_side(self, dx): #decale la pièce de dx (gauche si dx<0 droite sinon)
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self,k):
        old_rotation = self.figure.rotation
        self.figure.rotate(k)
        if self.intersects():
            self.figure.rotation = old_rotation


#Features du jeu 
#retourne la taille des 10 colonnes du jeu 
def column_height(field): #from top to bottom
    h=[]
    for j in range(10):
        column=[field[i][j] for i in range(20)] 
        height=0

        while height<20 and column[height]==0 :
            height+=1

        h.append(20-height)

    return(h)

#retourne la taille maximale des colonnes du jeu 
def maximum_height(field):
    return(max(column_height(field)))

#retourne la différence en valeur absolue de la taille d'une colonne avec celle de sa voisine 
def column_difference(field):# absolute difference between adjacent columns
    df=[]
    h=column_height(field)

    for j in range(9):
        df.append(abs(h[j+1]-h[j]))
    
    return(df)
#compte le nombre de troux inaccessibles du jeu 
def holes(field):
    L=0
    h=column_height(field)

    for j in range(10):
        for i in range(20-h[j],20):
            if field[i][j]==0:
                L+=1
    
    return(L)


#Evalue la configuration de la grille en pondérant les features par le vecteur W de taille 21
def evaluate(W, field): 
    #W=[w1, ..., w21] vector of parameters to tune 

    h=column_height(field)
    dh=column_difference(field)
    L=holes(field)
    H=maximum_height(field)
    
    S1,S2,S3,S4=0,0,0,0

    for k in range (len(h)):
        S1+=h[k]*W[k]
    
    for k in range (len(dh)):
        S2+=dh[k]*W[10+k]

    S3=W[19]*L

    S4=W[20]*H

    return(S1+S2+S3+S4)

#pour une configuration et une nouvelle piece donné, retourne le meilleur coup au sens de evaluate()
def evaluate_best_move(W,field,type,color):
    L=[]
    score=[]
    for k in range (4):
        for col in range (-5,10):
        
            game_copy=Tetris(20,10)
            
            game_copy.field=copy.deepcopy(field)

            game_copy.new_figure(type,3,0)
            game_copy.rotate(k)
            game_copy.go_side(col) 
            game_copy.go_space(color)
            score.append(evaluate(W,game_copy.field))
            L.append([col,k])
    
    best_move=score.index(min(score))
    return(L[best_move])

#simule une partie 
def simulation_without_graphic(W):


    game = Tetris(20, 10)
    while game.state!="gameover":

        fig=random.randint(0,6)
        color=1
        game.new_figure(fig,3,0)
        if game.intersects():
            game.state="gameover"

        col, rot = evaluate_best_move(W,game.field,fig,color)
        game.rotate(rot)
        game.go_side(col)
        game.go_space(color)
        print(game.score)


    return(game.score)

def simulation_gif(W):
    L=[]

    game = T.Tetris(20, 10)
    while game.state!="gameover":


        fig=random.randint(0,6)
        color=random.randint(1,4)
        game.new_figure(fig,3,0)
        if game.intersects():
            game.state="gameover"

        col, rot = evaluate_best_move(W,game.field,fig,color)
        game.rotate(rot)
        game.go_side(col)
        game.go_space(color)
        
        fig, ax = plt.subplots()
        ax.set_title(str(game.score))
        ax.matshow(game.field, cmap='Blues')
        L.append(fig)

    return(L)  


def get_gif (L): #L: list of figures
    with imageio.get_writer('my_gif.gif', mode='I') as writer:

        for fig in L:
            fig.canvas.draw()
            image = imageio.core.asarray(fig.canvas.renderer.buffer_rgba())
            writer.append_data(image)