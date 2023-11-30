#----------------------------------------------------------------------------------------------------------------------#
# BIBLIOTECAS;

import pygame             # Importa a Biblioteca pygame.
import sys                # Importa a Biblioteca sys. 
from settings import *    # Importa tudo em setting.py
from tiles import Tile    # Importa a Classe 'Tile' de tilet.py
from level import Level   # Importa a Classe 'Level' de level.py.
from player import Player # Importa a Classe 'Player' de player.py.
from necroboss import Necroboss
import random

#----------------------------------------------------------------------------------------------------------------------#
# FERRAMENTAS;

pygame.init()                                                          # Inicializa o Pygame. 
pygame.font.init()
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((screen_width, screen_height))        # Cria a janela do jogo. 
clock = pygame.time.Clock()                                            # Cria o objeto Clock que é usado para controlar o FPS. 
pygame.display.set_caption("Revenge of Jack the Lumber")               # Dá um nome a tela principal do jogo.
screenintro = pygame.display.set_mode((screen_width, screen_height))   # Cria a janela de intro do jogo.
current_level = 0                                                      # Recebe o número atual da fase.

splashspeed = 10
random_width = random.randint(1, 604)
random_width2 = random.randint(1, 604)
attack_rect = pygame.Rect(600, random_width, 50, 50)
attack_rect2 = pygame.Rect(600, random_width2, 50, 50)
attack_rect3 = pygame.Rect(600, random_width, 50, 50)

#----------------------------------------------------------------------------------------------------------------------#
# INSTÂNCIAS;

level =  Level(level_map, screen, current_level)  # Classe Level. 
level2 = Level(level_map2, screen, current_level) # Classe Level.
level3 = Level(level_map3, screen, current_level) # Classe Level.
level4 = Level(level_map4, screen, current_level) # Classe Level.
level5 = Level(level_map5, screen, current_level) # Classe Level.

# O Construtor da Classe recebe dois argumentos... 
# level_map representa o layout da Fase em Settings.  
# screen é a superfície onde será exibida, sendo a minha tela. 

#-----------------------------------------------------------------------------------------------------------------------#
# EVENTOS;

while True:                           # O Loop principal verifica os eventos do jogo enquanto em execucão...
    for event in pygame.event.get():  # Para cada evento que rodar dentro do método de eventos do pygame...
        if event.type == pygame.QUIT: # Se o evento for Quit...
            pygame.quit()             # O programa é encerrado.
            sys.exit()
   
    screen.fill((0, 0, 0))            # Preenche a tela com a cor preta.
    keys = pygame.key.get_pressed()   # Uma instância de um método pygame para pressionamento de teclas. 
    level.intro()                     # Método para desenhar a imagem da tela de introducão.

    if keys[pygame.K_c]:              # Se a tecla Enter foi pressionada...eeeeeeeeee
        current_level = 1             # Altera o valor do contador.

    if current_level == 1:            # Sendo o contador diferente do valor original de zero...
        level5.run(5)                 # Vai para a tela principal do jogo.
        text = font.render("Jack", True, (0, 0, 255))  # Text, anti-aliasing, color
        text_rect = text.get_rect(center=(38, 25))  # Center the text on the screen
        screen.blit(text, text_rect)

        text2 = font.render("Necromancer", True, (0, 0, 255))  # Text, anti-aliasing, color
        text2_rect = text2.get_rect(center=(1100, 25))  # Center the text on the screen
        screen.blit(text2, text2_rect) 

        level.blastattack(screen)

        if len(level.enemies) == 0 or all(enemy.rect.y > screen_height for enemy in level.enemies.sprites()): # Verifica se não há mais inimigos no nível ou se todos os inimigos estão fora da tela
            current_level = 2

    if len(level.enemies) == 1:   # Se o número de sprites no meu grupo for 1...
        current_level = 2         # Altera o valor da fase atual.

    if current_level == 2:        # Se o valor da fase atual for 2...
        level2.run(2)
        text = font.render("Jack", True, (0, 0, 255))  # Text, anti-aliasing, color
        text_rect = text.get_rect(center=(38, 25))  # Center the text on the screen
        screen.blit(text, text_rect)
        if len(level2.enemies) == 0 or all(enemy.rect.y > screen_height for enemy in level2.enemies.sprites()): # Verifica se não há mais inimigos no nível ou se todos os inimigos estão fora da tela
            current_level = 3    

    if current_level == 3:
        level3.run(3)
        text = font.render("Jack", True, (0, 0, 255))  # Text, anti-aliasing, color
        text_rect = text.get_rect(center=(38, 25))  # Center the text on the screen
        screen.blit(text, text_rect)
        if len(level3.enemies) == 0 or all(enemy.rect.y > screen_height for enemy in level3.enemies.sprites()): # Verifica se não há mais inimigos no nível ou se todos os inimigos estão fora da tela
            current_level = 4

    if current_level == 4:
        level4.run(4)
        text = font.render("Jack", True, (0, 0, 255))  # Text, anti-aliasing, color
        text_rect = text.get_rect(center=(38, 25))  # Center the text on the screen
        screen.blit(text, text_rect)
        if len(level4.enemies) == 0 or all(enemy.rect.y > screen_height for enemy in level4.enemies.sprites()): # Verifica se não há mais inimigos no nível ou se todos os inimigos estão fora da tela
            current_level = 5

    if current_level == 5: 
        level5.run(5)
        text = font.render("Jack", True, (0, 0, 255))  # Text, anti-aliasing, color
        text_rect = text.get_rect(center=(38, 25))  # Center the text on the screen
        screen.blit(text, text_rect) 
        text2 = font.render("Necromancer", True, (0, 0, 255))  # Text, anti-aliasing, color
        text2_rect = text2.get_rect(center=(1100, 25))  # Center the text on the screen
        screen.blit(text2, text2_rect) 

    pygame.display.update() # Atualiza a tela.
    clock.tick(60)          # O loop é executado em 60 FPS. 

#------------------------------------------------------------------------------------------------------------------------#