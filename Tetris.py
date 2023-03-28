import numpy as np
import pygame
import random


pygame.font.init()

# Variables Globales
Largeur_fenetre = 800
Hauteur_fenetre = 700
Largeur_jeu = 300  # 30 x 10 donne 300
Hauteur_jeu = 600  # 30 x 20 donne 600
Taille_bloc = 30

# On ne veut pas que le terrain de jeu recouvre la totalité de la fenêtre que l'on va créer donc on
# choisit des valeurs différentes pour ses dimensions. De plus, vu que le jeu se déroule dans un rectangle
# de 20 blocs par 10, il faut que l'on puisse placer 10 blocs en largeur et 20 en hauteur.

# Définition de l'origine de notre grille de jeu: en pygame le point (0,0) de notre fenêtre ne se trouve
# ni au centre ni au milieu de celle-ci mais en haut à gauche. On conserve cette notion lorsque l'on crée
# l'origine de notre grille de jeu.

x0 = (Largeur_fenetre - Largeur_jeu) // 2
y0 = Hauteur_fenetre - Hauteur_jeu

# Ces deux valeurs nous serviront à localiser chaque tétrimino qui sera en train de tomber.
# Définissons maintenant ces tétriminos.


# Formes et formes des rotations possibles des tétriminos

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# On utilise des listes de listes pour définir nos tétriminos, les zéros représentent les endroits où il
# y a des blocs. Chaque tétrimino a plusieurs formes possibles et elles sont représentées par les
# différentes dispositions des zéros.

Tetriminos = [S, Z, I, O, J, L, T]
Tetriminos_couleur = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# On indexe nos tétriminos de 0 à 6 et on utilise un codage rvb pour déterminer les couleurs de ceux-ci


class Piece(object):
    def __init__(self, x, y, tetrimino):
        self.x = x
        self.y = y
        self.tetrimino = tetrimino
        self.couleur = Tetriminos_couleur[Tetriminos.index(tetrimino)]
        self.rotation = 0

#Cette classe nous permet de définir toutes les caractéristiques de nos téttriminos: couleur, position, état de rotation...
            
def creation_grille(positions_statiques):
    grille = [[(0, 0, 0) for k in range(10)] for k in range(20)]

    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if (j, i) in positions_statiques:
                c = positions_statiques[(j, i)]
                grille[i][j] = c
    return grille

#Cette fonction sert à créer notre grille qui n'est qu'une matrice de blocs noirs pour l'instant.


def conversion_format(tetrimino): #Cette fonction sert à transformer nos listes de zéros en véritables formes.
    positions = []
    format = tetrimino.tetrimino[tetrimino.rotation % len(tetrimino.tetrimino)] #On associe à chaque tétrimino sa forme en fonction de son état de rotation, pour
                                                                                #pour le I il n'y en a que deux, mais pour le T quatre. A chaque fois que l'on
                                                                                #a tourné deux ou quatre fois on revient à la forme de base.

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((tetrimino.x + j, tetrimino.y + i)) #Dès qu'un zéro apparaît cela signifie qu'il y a un bloc à afficher et donc on ajoute à la liste
                                                                     #de positionnements de notre tétrimino.

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4) #On soustrait 2 et 4 pour déplacer vers le haut et vers la gauche notre tétrimino qui était décalé en raison de la
                                                #définition en listes de celui-ci.

    return positions


def espace_disponible(tetrimino, grille): #Cette fonction nous permet de déterminer quelles sont les positions disponibles dans notre grille pour le tétrimino
    position_valide = [[(j, i) for j in range(10) if grille[i][j] == (0, 0, 0)] for i in range(20)] #Si le carreau (i,j) de notre grille est noir alors il n'y a 
                                                                                                    #aucun tetrimino à cet endroit
    position_valide = [j for sub in position_valide for j in sub] #On fait ça pour ne garder qu'une liste d'objets et pas une liste de listes.

    formate = conversion_format(tetrimino)

    for pos in formate:
        if pos not in position_valide: #cette condition est pour vérifier que chacune de nos rotations de notre tétrimino est possible
            if pos[1] > -1: #cette condition est pour empêcher de vérifier que la position est valide avant que le tétrimino n'apparaisse sur l'écran pour qu'il 
                            #puisse tomber quoiqu'il arrive alors qu'il est au-dessus de la grille et donc apparaître dans la grille.
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1: #Si le tétrimino est bloqué au-dessus de la grille, le joueur a perdu la partie
            return True
    return False


def obtenir_forme():
    return Piece(5, 0, random.choice(Tetriminos)) 


def dessine_texte_milieu(text, size, color, surface):
    police = pygame.font.SysFont("comicsans", size, bold=True)
    label = police.render(text, True, color)
    surface.blit(label, (x0 + Largeur_jeu / 2 - (label.get_width() / 2), y0 + Hauteur_jeu / 2 - label.get_width() / 2))#on centre le texte 


def dessine_grille(surface, grille): #cette fonction sert à quadriller la grille de jeu obtenue via la fonction creation_grille
    for i in range(len(grille)):
        pygame.draw.line(surface, (128, 128, 128), (x0, y0 + i * Taille_bloc), (x0 + Largeur_jeu, y0 + i * Taille_bloc))
        for j in range(len(grille[i])):
            pygame.draw.line(surface, (128, 128, 128), (x0 + j * Taille_bloc, y0),
                             (x0 + j * Taille_bloc, y0 + Hauteur_jeu))


def clear_rows(grille, positions_statiques):#cette fonction sert à éliminer les lignes qui sont complétées au fur et à mesure du jeu.
    inc = 0
    for i in range(len(grille) - 1, -1, -1):
        row = grille[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del positions_statiques[(j, i)] #on essaye de supprimer l'information que le bloc (i,j) est occupé si elle existe
                except:
                    continue

    if inc > 0:
        for key in sorted(list(positions_statiques), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                positions_statiques[newKey] = positions_statiques.pop(key) #on supprime les anciennes positions statiques en les réhaussant du nombre de lignes 
                                                                           #éliminées pour bien conserver l'information qu'il y a des blocs déjà présents sur 
                                                                           #les lignes autres que celles qui sont éliminées et les garder en positions impossibles 
                                                                           #à prendre
    return (inc)#on renvoie le nombre de lignes éliminées

def test_clear_rows():
    pygame.init()
    surface = pygame.display.set_mode((Largeur_fenetre, Hauteur_fenetre))
    positions_statiques = {}
    #On génère une grille aléatoirement pour tester notre fonction dessus
    for pos in [[np.random.randint(0, 10), np.random.randint(15, 20)] for _ in range(40)]:
        p = (pos[0], pos[1])
        positions_statiques[p] = Tetriminos_couleur[0]

    grille = creation_grille(positions_statiques)
    dessine_fenetre(surface, grille)
    pygame.display.update()
    nb_ligne_pleine = 0
    for j in range(len(grille)):
        row = grille[j]
        if (0,0,0) not in row:
            nb_ligne_pleine += 1
    if clear_rows(grille,{}) == nb_ligne_pleine:
        print(nb_ligne_pleine)
        return True
    else:
        return False

def dessine_prochaine_forme(tetrimino, surface): #cette fonction sert à la fois à dessiner le texte "Prochaine Forme" et à afficher le tétrimino qui suivra.
    police = pygame.font.SysFont('comicsans', 30)
    label = police.render('Prochaine Forme', True, (255, 255, 255))

    sx = x0 + Largeur_jeu + 50
    sy = y0 + Hauteur_jeu / 2 + 100  # -100
    format = tetrimino.tetrimino[tetrimino.rotation % len(tetrimino.tetrimino)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, tetrimino.couleur,
                                 (sx + j * Taille_bloc, sy + i * Taille_bloc, Taille_bloc, Taille_bloc), 0)

    surface.blit(label, (sx + 10, sy - 30))

def plus_haut_bloc(grille): #cette fonction sert à renvoyer la hauteur du plus haut bloc
    ind = len(grille)
    for j in range(len(grille)):
        row = grille[j]
        for espace in row:
            if espace != (0,0,0):
                return ind
        ind -= 1
    return ind

def espace_perdu(grille): #cette fonction sert à renvoyer le nombre de blocs où il n'y a pas de tétrimino présent mais qui ne sont plus accessibles car recouverts
    count = 0
    for j in range (19,plus_haut_bloc(grille)-1, -1):
        row_inf = grille[j]
        for espace in row_inf:
            c = 0
            for i in range(1, j):
                if grille[j-i][row_inf.index(espace)] != (0,0,0):
                    c += 1
            if espace == (0,0,0) and c >= 1:
                count += 1
    return count


def dessine_fenetre(surface, grille, score=0): #cette fonction sert à créer la fenêtre de jeu où seront affichées la grille de jeu et la prochaine forme.
    surface.fill((0, 0, 0))

    pygame.font.init()
    police = pygame.font.SysFont('comicsans', 60)
    label = police.render('Tetrisae', True, (255, 255, 255))

    surface.blit(label, (x0 + Largeur_jeu / 2 - (label.get_width() / 2), 30))

    police = pygame.font.SysFont('comicsans', 30)
    label = police.render('Score:' + str(score), True, (255, 255, 255))

    sx = x0 + Largeur_jeu + 50
    sy = y0 + Hauteur_jeu / 2 + 100  # -100
    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grille)):
        for j in range(len(grille[i])):
            pygame.draw.rect(surface, grille[i][j],
                             (x0 + j * Taille_bloc, y0 + i * Taille_bloc, Taille_bloc, Taille_bloc), 0)

    pygame.draw.rect(surface, (255, 0, 0), (x0, y0, Largeur_jeu, Hauteur_jeu), 4)

    dessine_grille(surface, grille)
    # pygame.display.update()


def main(win): #cette fonction est la boucle de jeu
    B = 20
    ep2 = 0
    positions_statiques = {}
    grille = creation_grille(positions_statiques)

    changement_tetrimino = False
    run = True
    tetrimino_actuel = obtenir_forme()
    prochain_tetrimino = obtenir_forme()
    temps = pygame.time.Clock()
    temps_de_chute = 0
    temps_de_jeu = 0
    vitesse_chute = 0.33
    score = 0

    while run:
        grille = creation_grille(positions_statiques)
        temps_de_chute += temps.get_rawtime()
        temps_de_jeu += temps.get_rawtime()
        temps.tick()


        if temps_de_chute / 1000 > vitesse_chute: #cette condition est utilisée afin de faire tomber automatiquement les tétriminos
            temps_de_chute = 0
            tetrimino_actuel.y += 1
            if not (espace_disponible(tetrimino_actuel, grille)) and tetrimino_actuel.y > 0: #cette condition est utilisée afin de vérifier si la chute du tétrimino 
                                                                                             #est possible et s'il est bien dans la grille de jeu et pas au-dessus, 
                                                                                             #s'il ne peut plus tomber alors on change de tétrimino.
                tetrimino_actuel.y -= 1
                changement_tetrimino = True

        if temps_de_jeu / 1000 > 5: #plus le jeu avance et plus il est difficile de placer des blocs donc on diminue au cours du jeu la vitesse de chute.
            temps_de_jeu = 0
            if vitesse_chute > 0.12:
                vitesse_chute -= 0.005

        for event in pygame.event.get(): #en fonction de la touche pressée on effectue l'action qui y correspond, les flèches latérales servent à bouger sur les 
                                         #côtés, celle du bas à descendre et celle du haut à effectuer une rotation.
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetrimino_actuel.x -= 1
                    if not (espace_disponible(tetrimino_actuel, grille)):
                        tetrimino_actuel.x += 1
                if event.key == pygame.K_RIGHT:
                    tetrimino_actuel.x += 1
                    if not (espace_disponible(tetrimino_actuel, grille)):
                        tetrimino_actuel.x -= 1
                if event.key == pygame.K_DOWN:
                    tetrimino_actuel.y += 1
                    if not (espace_disponible(tetrimino_actuel, grille)):
                        tetrimino_actuel.y -= 1
                if event.key == pygame.K_UP:
                    tetrimino_actuel.rotation += 1
                    if not (espace_disponible(tetrimino_actuel, grille)):
                        tetrimino_actuel.rotation -= 1

        tetrimino_pos = conversion_format(tetrimino_actuel)

        for i in range(len(tetrimino_pos)):
            x, y = tetrimino_pos[i]
            if y > -1:
                grille[y][x] = tetrimino_actuel.couleur #on colore les endroits de la grille où il y a des tétriminos

        if changement_tetrimino:#on effectue toutes les actions nécessaires lorsque l'on change de tétrimino
            A,B = B,plus_haut_bloc(grille)
            ep,ep2 = ep2, espace_perdu(grille)
            for pos in tetrimino_pos:
                p = (pos[0], pos[1])
                positions_statiques[p] = tetrimino_actuel.couleur
            tetrimino_actuel = prochain_tetrimino
            prochain_tetrimino = obtenir_forme()
            changement_tetrimino = False
            score += clear_rows(grille, positions_statiques) * 10
            if B > A:
                dessine_texte_milieu("PERDU", 80, (255, 255, 255), win)
                pygame.display.update()
                pygame.time.delay(1500)
                run = False


        dessine_fenetre(win, grille, score)
        dessine_prochaine_forme(prochain_tetrimino, win)
        pygame.display.update()

        if check_lost(positions_statiques):
            dessine_texte_milieu("Perdu", 80, (255, 255, 255), win)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False


def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        dessine_texte_milieu("Appuyez pour commencer", 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.display.quit()

#Lors de l'exécution des différentes IA, il faut ignorer les lignes suivantes sinon Tetrisae se lance et il faut fermer la fenêtre pour pouvoir lancer la simulation
win = pygame.display.set_mode((Largeur_fenetre, Hauteur_fenetre))
pygame.display.set_caption('Tetrisae')
main_menu(win)
