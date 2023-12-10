#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# BIBLIOTECAS;

import pygame            # Importa a Biblioteca pygame.
import sys               # Importa a Biblioteca sys. 
from settings import *   # Importa tudo em setting.py
from level import Level  # Importa a Classe 'Level' de level.py.

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# FERRAMENTAS;  

pygame.init()        # Inicializa o Pygame.
pygame.font.init()   # Inicializa a Fonte.
pygame.mixer.init()  # Inicializa o Áudio.

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# UTILITÁRIOS

screen = pygame.display.set_mode((screen_width, screen_height))       # Cria a janela do jogo. 
pygame.display.set_caption("Revenge of Jack the Lumber")              # Dá um nome a tela principal do jogo.
clock = pygame.time.Clock()                                           # Cria o objeto Clock que é usado para controlar o FPS. 
screenintro = pygame.display.set_mode((screen_width, screen_height))  # Cria a janela de intro do jogo.
font = pygame.font.Font(None, 36)                                     # Cria um bloco para escrever.
theme = pygame.mixer.Sound('./graphics/sounds/scenario/theme.mp3')    # Tema principal do jogo.
start = pygame.mixer.Sound('./graphics/sounds/scenario/start.mp3')    # Coinflip.
taunt1 = pygame.mixer.Sound('./graphics/sounds/scenario/taunt1.wav')  # Provocacão do boss ao entrar na fase5.
current_level = 0                                                     # Variável de checagem da fase.
coinflip = False                                                      # Verificacão do coinflip.
music_playing = False                                                 # Verificacão da música tema.

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# INSTÂNCIAS;

level =  Level(level_map, screen, current_level)  # Classe Level. 
level2 = Level(level_map2, screen, current_level) # Classe Leve2.
level3 = Level(level_map3, screen, current_level) # Classe Leve3.
level4 = Level(level_map4, screen, current_level) # Classe Leve4.
level5 = Level(level_map5, screen, current_level) # Classe Leve5. 
level7 = Level(level_map7, screen, current_level) # Classe Leve5. 

# O Construtor da Classe recebe três argumentos... 
# level_map representa o layout da Fase em Settings.  
# screen é a superfície onde será exibida, sendo a minha tela. 
# current_level recebe a variável de identificacão da fase.

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# EVENTOS;

while True:                           # O Loop principal verifica os eventos do jogo enquanto em execucão...
    for event in pygame.event.get():  # Para cada evento que rodar dentro do método de eventos do pygame...
        if event.type == pygame.QUIT: # Se o evento for Quit...
            pygame.quit()             # O programa é encerrado. 
            sys.exit()                # Encerra o sistema. 
   
    screen.fill((0, 0, 0))            # Preenche a tela com a cor preta.
    keys = pygame.key.get_pressed()   # Uma instância de um método pygame para pressionamento de teclas. 
    level.intro()                     # Método para desenhar a imagem da tela de introducão.

    if keys[pygame.K_c] and not music_playing: # Se a tecla Enter foi pressionada...
        current_level = 1                      # Altera o valor do level atual.
        start.play()                           # Reproduz o áudio.
        theme.play()                           # Reproduz o áudio.
        music_playing = True                   # Reproduz o áudio.

    if current_level == 1:                             # Se o level atual for 1...
        level.run(1)                                   # Vai para o estágio1. 
        text = font.render("Viktor", True, (0, 0, 0))  # Variável recebe o texto.
        text_rect = text.get_rect(center=(44, 25))     # Centraliza o texto na tela.        
        screen.blit(text, text_rect)                   # Escreve o texto no retângulo do texto.
        if (len(level.enemies) == 0 or all(enemy.rect.y > screen_height for enemy in level.enemies.sprites())):  # Verifica se não há mais inimigos no nível ou se todos os inimigos estão fora da tela
            current_level = 2       # Muda a variável do estágio.
            music_playing = False   # Encerra o áudio.

    if current_level == 2:                             # Se o level atual for 2...
        level2.run(2)                                  # Vai para o estágio2.ee
        text = font.render("Viktor", True, (0, 0, 0))  # Variável recebe o texto.
        text_rect = text.get_rect(center=(44, 25))     # Centraliza o texto na tela.
        screen.blit(text, text_rect)                   # Escreve o texto no retângulo do texto.
        if len(level2.enemies) == 0 or all(enemy.rect.y > screen_height for enemy in level2.enemies.sprites()) and (len(level2.hellhound) == 0 or all(hellhound.rect.y > screen_height for hellhound in level2.hellhound.sprites())): # Verifica se não há mais inimigos no nível ou se todos os inimigos estão fora da tela # Verifica se não há mais inimigos no nível ou se todos os inimigos estão fora da tela
            current_level = 3                                                                                                                                                                                                         # Muda a variável do estágio. 

    if current_level == 3:                             # Se o level atual for 3...
        level3.run(3)                                  # Vai para o estágio3.
        text = font.render("Viktor", True, (0, 0, 0))  # Variável recebe o texto.
        text_rect = text.get_rect(center=(44, 25))     # Centraliza o texto na tela.
        screen.blit(text, text_rect)                   # Escreve o texto no retângulo do texto.
        if len(level3.enemies) == 0 or all(enemy.rect.y > screen_height for enemy in level3.enemies.sprites()) and (len(level3.hellhound) == 0 or all(hellhound.rect.y > screen_height for hellhound in level3.hellhound.sprites())): # Verifica se não há mais inimigos no nível ou se todos os inimigos estão fora da tela
            current_level = 4                                                                                                                                                                                                         # Altera o valor do level atual.

    if current_level == 4:                                     # Se o level atual for 4...
        level4.run(4)                                          # Vai para o estágio4.
        text = font.render("Viktor", True, (0, 0, 0))          # Variável recebe o texto.
        text_rect = text.get_rect(center=(44, 25))             # Centraliza o texto na tela.
        screen.blit(text, text_rect)                           # Escreve o texto no retângulo do texto.
        text2 = font.render("Fallen Knight", True, (0, 0, 0))  # Variável recebe o texto.
        text2_rect = text2.get_rect(center=(1100, 25))         # Centraliza o texto na tela.
        screen.blit(text2, text2_rect)                         # Escreve o texto no retângulo do texto.   
        if len(level4.enemies) == 0 or all(enemy.rect.y > screen_height for enemy in level4.enemies.sprites()) and (len(level4.bodyguard) == 0 or all(bodyguard.rect.y > screen_height for bodyguard in level4.bodyguard.sprites())): # Verifica se não há mais inimigos no nível ou se todos os inimigos estão fora da tela:  # Verifica se não há mais inimigos no nível ou se todos os inimigos estão fora da tela: # Verifica se não há mais inimigos no nível ou se todos os inimigos estão fora da tela
            current_level = 5                                                                                    # Altera o valor do level atual.
            taunt1.play()

    if current_level == 5:                              # Se o level atual for 5...
        level5.run(5)                                   # Vai para o estágio5.
        taunt = False                                   # Encerra a provocacão.
        text = font.render("Viktor", True, (0, 0, 0))   # Variável recebe o texto.
        text_rect = text.get_rect(center=(44, 25))      # Centraliza o texto na tela.
        screen.blit(text, text_rect)                    # Escreve o texto no retângulo do texto.
        text2 = font.render("Moro's", True, (0, 0, 0))  # Variável recebe o texto.
        text2_rect = text2.get_rect(center=(1150, 25))  # Centraliza o texto na tela.
        screen.blit(text2, text2_rect)                  # Escreve o texto no retângulo do texto.        

    pygame.display.update()  # Atualiza a tela.
    clock.tick(60)           # O loop é executado em 60 FPS. 

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
