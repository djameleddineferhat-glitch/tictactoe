import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
LARGEUR = 600
HAUTEUR = 600
TILE_SIZE = 200

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)

# Charger l'image pour le joueur "X" (claymore.png)
image_x = pygame.image.load("claymore.png")
image_x = pygame.transform.scale(image_x, (TILE_SIZE, TILE_SIZE))  # Redimensionner l'image pour qu'elle corresponde à la taille de la case

# Charger l'image pour le joueur "O" (lance.png) - IA
image_o = pygame.image.load("lance.png")
image_o = pygame.transform.scale(image_o, (TILE_SIZE, TILE_SIZE))  # Redimensionner l'image pour l'IA

# Charger l'image de fond
background = pygame.image.load("dynasty.png")
background = pygame.transform.scale(background, (LARGEUR, HAUTEUR))  # Redimensionner l'image pour qu'elle corresponde à la taille de la fenêtre

# Charger l'image de défaite
img_defaite = pygame.image.load("deadmo.png")
img_defaite = pygame.transform.scale(img_defaite, (LARGEUR, HAUTEUR))  # Redimensionner l'image pour qu'elle s'adapte à la taille de la fenêtre

# Fonction pour afficher le plateau de jeu
def afficher_plateau(plateau, screen):
    screen.blit(background, (0, 0))  # Afficher l'image de fond
    for i in range(1, 3):
        pygame.draw.line(screen, NOIR, (i * TILE_SIZE, 0), (i * TILE_SIZE, HAUTEUR), 5)
        pygame.draw.line(screen, NOIR, (0, i * TILE_SIZE), (LARGEUR, i * TILE_SIZE), 5)

    for i in range(3):
        for j in range(3):
            if plateau[i][j] == "X":
                screen.blit(image_x, (j * TILE_SIZE, i * TILE_SIZE))  # Afficher l'image de "X" (claymore)
            elif plateau[i][j] == "O":
                screen.blit(image_o, (j * TILE_SIZE , i * TILE_SIZE))  # Afficher l'image de "O" (lance pour IA)
    pygame.display.flip()  # Met à jour l'affichage

# Fonction pour vérifier si un joueur a gagné
def verifier_gagnant(plateau, joueur):
    for i in range(3):
        if plateau[i][0] == plateau[i][1] == plateau[i][2] == joueur:
            return True
        if plateau[0][i] == plateau[1][i] == plateau[2][i] == joueur:
            return True
    if plateau[0][0] == plateau[1][1] == plateau[2][2] == joueur:
        return True
    if plateau[0][2] == plateau[1][1] == plateau[2][0] == joueur:
        return True
    return False

# Fonction pour vérifier si une case est libre
def case_libre(plateau, ligne, col):
    return plateau[ligne][col] == " "

# Fonction de l'ordinateur (bot) pour jouer
def ordinateur(board, coup_ia):
    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if case_libre(board, i, j):
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    
    # Jouer un son différent selon le coup de l'IA
    if coup_ia == 1:
        sound = pygame.mixer.Sound("tres.mp3")  # Son pour le premier coup de l'IA
    elif coup_ia == 2:
        sound = pygame.mixer.Sound("duo.mp3")  # Son pour le deuxième coup de l'IA
    else:
        sound = pygame.mixer.Sound("unus.mp3")  # Son pour le troisième coup de l'IA
    
    sound.play()  # Jouer le son
    return best_move

# Fonction de l'algorithme Minimax
def minimax(plateau, depth, maximiser):
    score = evaluation(plateau)
    if score == 1 or score == -1:
        return score
    if all(plateau[i][j] != " " for i in range(3) for j in range(3)):
        return 0

    if maximiser:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if case_libre(plateau, i, j):
                    plateau[i][j] = "O"
                    score = minimax(plateau, depth + 1, False)
                    plateau[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if case_libre(plateau, i, j):
                    plateau[i][j] = "X"
                    score = minimax(plateau, depth + 1, True)
                    plateau[i][j] = " "
                    best_score = min(score, best_score)
        return best_score

# Fonction d'évaluation de la partie
def evaluation(plateau):
    if verifier_gagnant(plateau, "X"):
        return -1
    elif verifier_gagnant(plateau, "O"):
        return 1
    return 0

# Fonction principale pour gérer le jeu
def jeu_tic_tac_toe():
    plateau = [[" " for _ in range(3)] for _ in range(3)]  # Créer un plateau vide
    joueurs = ["X", "O"]  # X pour le joueur, O pour le bot
    tour = 0
    coup_ia = 1  # Compteur pour savoir quel son jouer (1er coup, 2ème coup, etc.)
    game_over = False
    screen = pygame.display.set_mode((LARGEUR, HAUTEUR))  # Création de la fenêtre
    pygame.display.set_caption("Tic-Tac-Toe")  # Titre de la fenêtre

    # Charger et jouer la bande son
    pygame.mixer.music.load("ost_mogh.mp3")  # Charger le fichier de musique
    pygame.mixer.music.play(-1)  # Jouer la musique en boucle (-1 pour indiquer la répétition infinie)

    # Charger le son de défaite
    son_defaite = pygame.mixer.Sound("nihil.mp3")

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN and tour % 2 == 0:  # Si c'est le tour du joueur
                x, y = event.pos
                ligne, col = y // TILE_SIZE, x // TILE_SIZE  # Calcul des indices
                if case_libre(plateau, ligne, col):
                    plateau[ligne][col] = "X"  # Le joueur joue avec "X" (claymore)
                    if verifier_gagnant(plateau, "X"):
                        afficher_plateau(plateau, screen)
                        pygame.display.update()
                        print("Félicitations, vous avez gagné !")
                        game_over = True
                    elif all(plateau[i][j] != " " for i in range(3) for j in range(3)):  # Match nul
                        afficher_plateau(plateau, screen)
                        pygame.display.update()
                        print("Match nul ! Le jeu est terminé.")
                        game_over = True
                    tour += 1

        if tour % 2 != 0:  # Tour du bot
            ligne, col = ordinateur(plateau, coup_ia)  # Le coup de l'IA
            plateau[ligne][col] = "O"  # L'IA joue avec "O" (lance)
            if verifier_gagnant(plateau, "O"):
                afficher_plateau(plateau, screen)
                pygame.display.update()
                print("Le bot a gagné !")
                # Afficher l'image de défaite
                screen.blit(img_defaite, (0, 0))
                pygame.display.update()
                # Jouer le son de défaite
                son_defaite.play()
                # Ajouter une boucle pour empêcher la fermeture immédiate
                attente_quitter = True
                while attente_quitter:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            attente_quitter = False
                            game_over = True
                break
            elif all(plateau[i][j] != " " for i in range(3) for j in range(3)):  # Match nul
                afficher_plateau(plateau, screen)
                pygame.display.update()
                print("Match nul ! Le jeu est terminé.")
                game_over = True
            coup_ia += 1
            tour += 1
        
        afficher_plateau(plateau, screen)  # Rafraîchir l'affichage du plateau

    pygame.quit()  # Fermer Pygame proprement

# Lancer le jeu
jeu_tic_tac_toe()
