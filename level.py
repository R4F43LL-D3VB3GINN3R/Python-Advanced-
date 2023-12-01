#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

import pygame 
import random
from tiles import Tile
from settings import tile_size, screen_width, screen_height
from player import Player
from enemies import Enemies
from necromancer import Necromancer
from necroboss import Necroboss

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Classe 'Level'
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# A classe 'Level' é responsável por representar e gerenciar o ambiente de jogo. Ela organiza os blocos da classe 'Tile' de acordo com o layout do mapa definido em 'Settings'.
# 
# Métodos:
#
# - __init__(self, level_data, surface): Inicializa a classe, recebendo dados sobre o layout do nível (level_data) e a superfície onde será exibido (surface). 
#                                        Configura o nível utilizando o método 'setup_level' e define o deslocamento do mundo como 0.
# 
# - setup_level(self, layout): Configura o nível com base no layout fornecido. Cria instâncias de blocos ('Tile') e um jogador ('Player') com base nas informações do layout.
# 
# - run(self): Desenha o nível na tela. Atualiza a posição dos blocos e do jogador, e em seguida, desenha esses elementos na superfície.
# 
# - horizontal_movement_collision(self): Lida com o movimento horizontal do jogador e verifica colisões horizontais.
# 
# - vertical_movement_collision(self): Lida com o movimento vertical do jogador e verifica colisões verticais.
# 
# - draw_health_bar(self, health, x, y, screen): Cria uma barra de pontos de vida na tela.
# 
# - intro(self): Exibe a tela de introdução.
#
# A classe utiliza grupos de sprites para armazenar os blocos ('tiles') e o jogador ('player_group'), permitindo a atualização e desenho eficientes dos elementos na tela durante a execução do jogo.

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class Level:

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def __init__(self, level_data, surface, current_level): # O método __init__ é chamado automaticamente quando uma nova instância é criada.
                                             # level_data contém informacões sobre a disposicão do blocos... 
                                             # surface é a superfície onde o nível será exibido. 

                # Level Setup.
        self.display_surface = surface                                                                     # Armazena a superfície onde a Fase será exibida. 
        self.setup_level(level_data)                                                                       # Inicia a fase. 
        self.current_x = 0                                                                                 # Recebe a posicão horizontal atual. 
        self.background = pygame.image.load('./graphics/scenarios/1.png').convert()                        # Recebe a imagem de fundo.
        self.backgroundintro = pygame.image.load('./graphics/scenarios/intro.jpg').convert()               # Recebe a imagem de fundo da intro.
        self.backgroundintro = pygame.transform.scale(self.backgroundintro, (screen_width, screen_height)) # Recebe o tamanho da imagem da intro. 
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))           # Recebe o tamanho da imagem. 
        self.stage2 = pygame.image.load('./graphics/scenarios/stage2.png').convert()
        self.stage2 = pygame.transform.scale(self.stage2, (screen_width, screen_height))
        self.stage3 = pygame.image.load('./graphics/scenarios/stage3.jpg').convert()
        self.stage3 = pygame.transform.scale(self.stage3, (screen_width, screen_height))
        self.stage4 = pygame.image.load('./graphics/scenarios/stage4.png').convert()
        self.stage4 = pygame.transform.scale(self.stage4, (screen_width, screen_height))
        self.stage5 = pygame.image.load('./graphics/scenarios/stage5.jpg').convert()
        self.stage5 = pygame.transform.scale(self.stage5, (screen_width, screen_height))
        self.health = 100  
        self.healthboss = 100                                                                               # Valor default da barra de HP. 
        self.x = 10                                                                                        # Coordenada x (horizontal) onde a barra de saúde será desenhada na tela. 
        self.y = 10                                                                                        # Coordenada y (vertical) onde a barra de saúde será desenhada na tela. 
        self.hurt_timer = 0                                                                                # Recebe o tempo de tempo em que muda o comportamento para machucado.
        self.current_level = current_level
        self.splashspeed = 10
        self.random_width = random.randint(1, 604)
        self.random_width2 = random.randint(1, 604)
        self.attack_rect = pygame.Rect(600, self.random_width, 50, 50)
        self.attack_rect2 = pygame.Rect(600, self.random_width2, 50, 50)
        self.attack_rect3 = pygame.Rect(600, self.random_width, 50, 50)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def setup_level(self, layout):                            # O método setup_level é responsável por inicializar o nível do jogo com base em um layout fornecido
                                                              # layout é a representacão do layout da Fase que está em settings.py. 

        self.tiles = pygame.sprite.Group()                    # Um grupo de sprites chamado tiles é criado para armazenar os Blocos que serão criados.
        self.player = pygame.sprite.GroupSingle()             # Um grupo de sprites chamado player é criado para armazenar o personagem que será criado.
        self.enemies = pygame.sprite.Group()                  # Um grupo de sprites chamado enemies é criado para armazenar o inimigo que será criado.
        self.necromancer = pygame.sprite.GroupSingle()        # Um grupo de sprites chamado player é criado para armazenar o personagem que será criado.
        self.necroboss = pygame.sprite.GroupSingle()          # Um grupo de sprites chamado player é criado para armazenar o personagem que será criado.

        for row_index, row in enumerate(layout):              # Um loop aninhado percorre cada célula no layout usando enumerate...
            for col_index, cell in enumerate(row):            # ...para obter tanto os índices quanto os valores.
                x = col_index * tile_size                     # x Recebe o index das colunas. 
                y = row_index * tile_size                     # y Recebe o index das linhas.

                if cell == 'X':                               # Se ao percorrer o layout for encontrado um X...
                    tile = Tile((x, y), tile_size)            # Cria uma instância do Bloco (tile), com a posicão x e y.
                    self.tiles.add(tile)                      # Esse bloco é adicionado ao grupo de sprites tiles.
                if cell == 'P':                               # Se ao percorrer o layout for encontrado um P...
                    player_sprite = Player((x, y))            # Cria uma instância do Jogador (Player), com a posicão x e y.
                    self.player.add(player_sprite)            # Esse bloco é adicionado ao grupo de sprites player.
                if cell == 'S':                               # Se ao percorrer o layout for encontrado um S...
                    enemies_sprite = Enemies((x, y))          # Cria uma instância do inimigo, com a posicão x e y.
                    self.enemies.add(enemies_sprite)          # Esse bloco é adicionado ao grupo de sprites enemies.
                if cell == 'N':
                    necromancer_sprite = Necromancer((x, y))
                    self.necromancer.add(necromancer_sprite)
                if cell == 'B':
                    necroboss_sprite = Necroboss((x, y))
                    self.necroboss.add(necroboss_sprite)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        # O pygame é capaz de detectar colisões, mas ele não é capaz de dizer onde as colisões ocorreram.
        # Então devemos separar os movimentos verticais e horizontais juntamente com as suas respectivas colisões.

        # 1.Aplicacao de Movimento Vertical. 
        # 2.Verificacão de Colisão Vertical. 
        # 3.Aplicacao de Movimento Horizontal. 
        # 4.Verificacão de Colisão Horizontal. 

    def horizontal_movement_collision(self): # Método responsável por lidar com o movimento horizontal do jogador e verificar colisões horizontais.

        print(self.health)
        print(self.healthboss)

        player = self.player.sprite                          # player recebe o sprite do Jogador. 
        player.rect.x += player.direction.x * player.speed   # Atualiza a posicão horizontal do jogador incrementando-a. 
                                                             # Multiplicá-lo por qualquer número aumenta a velocidade. 
                                                             
        enemies = self.enemies.sprites()[0]                    # O inimigo recebe o sprite dele.  
        enemies.rect.x += enemies.direction.x * enemies.speed  # Atualiza a posicão horizontal do inimigo incrementando-a. 
                                                               # Multiplicá-lo por qualquer número aumenta a velocidade. 

        necroboss_sprite = self.necroboss.sprite

        if necroboss_sprite:
            necroboss = necroboss_sprite
            necroboss.rect.x += necroboss.direction.x * necroboss.speed

        # Jogador vs Inimigo. 

        for enemy in self.enemies.sprites():                 # Itera sobre todos os sprites de inimigos no grupo de enemies.
            enemy.rect.x += enemy.direction.x * enemy.speed  # Atualiza a posição horizontal (x) de um inimigo no seu jogo.

            if player.rect.colliderect(enemy.rect):          # Se o retângulo do jogador colidir com o do inimigo.
                if player.direction.x < 0:                   # Se o jogador estiver indo para a esquerda. 
                    player.rect.left = enemy.rect.right      # O retângulo do jogador recebe o valor do retângulo direito do inimigo.
                    player.on_left = True                    # O jogador estará indo para a esquerda.
                    self.current_x = player.rect.left        # A posição atual do jogador em x é atualizada para a borda esquerda do retângulo do jogador.
                    if player.blow == True:                  # Se o jogador estiver golpeando...
                        self.enemies.remove(enemy)           # Remove o inimigo do grupo de sprites.
                        player.blow = False                  # Redefine a flag de ataque.
                    else:                                    # Se o jogador não estiver golpeando...
                        player.status = 'hurt'               # O jogador recebe o status de machucado.
                        self.health -= 1                     # Deduz da saúde do jogador.
                elif player.direction.x > 0:                 # Se o jogador estiver indo para a direita.
                    player.rect.right = enemy.rect.left      # Se o jogador estiver indo para a direita, o retângulo do jogador recebe o valor do retângulo esquerdo do inimigo.
                    player.on_right = True                   # O jogador estará indo para a direita.
                    self.current_x = player.rect.right       # A posição atual do jogador em x é atualizada para a borda direita do retângulo do jogador.
                    if player.blow == True:                  # Se o jogador estiver golpeando...
                        self.enemies.remove(enemy)           # Remove o inimigo do grupo de sprites.
                        player.blow = False                  # Redefine a flag de ataque.
                    else:                                    # Se o jogador não estiver golpeando...
                        player.status = 'hurt'               # O jogador recebe o status de machucado.
                        self.health -= 1                     # Deduz da saúde do jogador.      

                if player.status == 'hurt':      # Se o jogador estiver machucado...
                    if player.direction.x < 0:   # E estiver indo para a esquerda...
                        player.rect.x += 20      # Ele é afastado para a direita. 
                    elif player.direction.x > 0: # E se estiver indo para a direita... 
                        player.rect.x -= 20      # Ele é afastado para a esquerda. 

                if self.health == 0: # Se a barra de pontos de vida chegar a zero...
                    pygame.quit()    # O evento de saída do jogo é ativado...

        # Jogador vs Boss.

        for boss in self.necroboss.sprites():  # Itera sobre todos os sprites do chefe no grupo de necroboss.
        
            if player.rect.colliderect(boss.rect):  # Se o retângulo do jogador colidir com o do chefe.
                if player.direction.x < 0:  # Se o jogador estiver indo para a esquerda.
                    player.rect.left = boss.rect.right  # O retângulo do jogador recebe o valor do retângulo direito do chefe.
                    player.on_left = True  # O jogador estará indo para a esquerda.
                    self.current_x = player.rect.left  # A posição atual do jogador em x é atualizada para a borda esquerda do retângulo do jogador.
                    if player.blow == True:  # Se o jogador estiver golpeando...
                        necroboss.special_moves()
                        self.healthboss -= 20  # Remove o chefe do grupo de sprites.
                        player.blow = False  # Redefine a flag de ataque.
                    else:  # Se o jogador não estiver golpeando...
                        player.status = 'hurt'  # O jogador recebe o status de machucado.
                        self.health -= 1  # Deduz da saúde do jogador.
                elif player.direction.x > 0:  # Se o jogador estiver indo para a direita.
                    player.rect.right = boss.rect.left  # Se o jogador estiver indo para a direita, o retângulo do jogador recebe o valor do retângulo esquerdo do chefe.
                    player.on_right = True  # O jogador estará indo para a direita.
                    self.current_x = player.rect.right  # A posição atual do jogador em x é atualizada para a borda direita do retângulo do jogador.
                    if player.blow == True:  # Se o jogador estiver golpeando...
                        necroboss.special_moves()
                        self.healthboss -= 20  # Remove o chefe do grupo de sprites.
                        player.blow = False  # Redefine a flag de ataque.
                    else:  # Se o jogador não estiver golpeando...
                        player.status = 'hurt'  # O jogador recebe o status de machucado.
                        self.health -= 1  # Deduz da saúde do jogador.

                if player.status == 'hurt':  # Se o jogador estiver machucado...
                    if player.direction.x < 0:  # E estiver indo para a esquerda...
                        player.rect.x += 20  # Ele é afastado para a direita.
                    elif player.direction.x > 0:  # E se estiver indo para a direita...
                        player.rect.x -= 20  # Ele é afastado para a esquerda.

                if self.health == 0:  # Se a barra de pontos de vida chegar a zero...
                    pygame.quit()  # O evento de saída do jogo é ativado...

        # Jogador vs Blocos. 

        for sprite in self.tiles.sprites():                  # Itera sobre todos os sprites de blocos no grupo de tiles.

            if sprite.rect.colliderect(player.rect):         # Se houver uma colisão entre o Jogador e um Bloco...
                if player.direction.x < 0:                   # Se o jogador estiver se movendo para a esquerda...
                    player.rect.left = sprite.rect.right     # Ajusta a posição do jogador para a direita do bloco.
                    player.on_left = True                    # O jogador está do lado esquerdo.
                    self.current_x = player.rect.left        # Ajusta a posicão para a borda esquerda do bloco para efetuar devida a colisão.
                elif player.direction.x > 0:                 # Se o jogador estiver se movendo para a direita...
                    player.rect.right = sprite.rect.left     # Ajusta a posição do jogador para a esquerda do bloco.
                    player.on_right = True                   # O jogador está do lado direito.
                    self.current_x = player.rect.right       # Ajusta a posicão para a borda direita do bloco para efetuar devida a colisão.

            # Inimigo vs Blocos.

            if sprite.rect.colliderect(enemies.rect):        # Itera sobre todos os sprites de blocos no grupo de tiles.
                if enemies.direction.x < 0:                  # Se houver uma colisão entre o inimigo e um Bloco...
                    enemies.rect.left = sprite.rect.right    # Ajusta a posição do jogador para a direita do bloco.
                    enemies.on_left = True                   # O jogador está do lado esquerdo.
                    self.current_x = enemies.rect.left       # Ajusta a posicão para a borda esquerda do bloco para efetuar devida a colisão.
                elif enemies.direction.x > 0:                # Se o jogador estiver se movendo para a direita...
                    enemies.rect.right = sprite.rect.left    # Ajusta a posição do jogador para a esquerda do bloco.
                    enemies.on_right = True                  # O jogador está do lado direito.
                    self.current_x = enemies.rect.right      # Ajusta a posicão para a borda direita do bloco para efetuar devida a colisão.

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):    # Se o jogador estiver a esquerda e o retângulo alinhado a esquerda for menor que a variável que o recebe ou maior ou igual a zero...
            player.on_left = False                                                               # O jogador não está do lado esquerdo.
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):  # Se o jogador estiver a direita e o retângulo alinhado a direita for maior que a variável que o recebe ou menor ou igual a zero...
            player.on_right = False                                                              # O jogador não está do lado direito.

    def vertical_movement_collision(self): # Método responsável por lidar com o movimento vertical do jogador e verificar colisões verticais.

        # Gravidade aos Inimigos. 

        for enemy in self.enemies.sprites():                 # Itera sobre todos os sprites de inimigos no grupo de enemies.
            enemy.apply_gravity()                            # Aplica a gravidade aos inimigos.

            for sprite in self.tiles.sprites():                   # Itera sobre todos os sprites de blocos no grupo de tiles.
                if sprite.rect.colliderect(enemy.rect):           # Se houver uma colisão entre o inimigo e um Bloco...
                    if enemy.direction.y > 0:                     # Se o inimigo estiver se movendo para baixo...
                        enemy.rect.bottom = sprite.rect.top  + 11 # Ajusta a posição do inimigo para a parte superior do bloco.
                        enemy.direction.y = 0                     # O inimigo não está nem se movendo para cima e nem para baixo. 
                        enemy.on_ground = True                    # O inimigo está tocando no chão. 
                    elif enemy.direction.y < 0:                   # Se o inimigo estiver se movendo para cima...
                        enemy.rect.top = sprite.rect.bottom       # Ajusta a posição do inimigo para a parte inferior do bloco.
                        enemy.direction.y = 0                     # O inimigo não está nem se movendo para cima e nem para baixo. 
                        enemy.on_ground = True                    # O inimigo está tocando no chão.
                    else:                                         # Do contrário... 
                        enemy.on_ground = False                   # Ele não estará tocando no chão. 

        # Gravidade ao Jogador.

        player = self.player.sprite                          # player recebe o sprite do Jogador. 
        player.apply_gravity()                               # Chama o método apply_gravity.

        for sprite in self.tiles.sprites():                  # Itera sobre todos os sprites de blocos no grupo de tiles.
            if sprite.rect.colliderect(player.rect):         # Se houver uma colisão entre o Jogador e um Bloco...
                if player.direction.y > 0:                   # Se o jogador estiver se movendo para baixo...
                    player.rect.bottom = sprite.rect.top     # Ajusta a posição do jogador para a parte superior do bloco.
                    player.direction.y = 0                   # O jogador não está nem se movendo para cima e nem para baixo. 
                    player.on_ground = True                  # O jogador está tocando no chão. 
                elif player.direction.y < 0:                 # Se o jogador estiver se movendo para cima...
                    player.rect.top = sprite.rect.bottom     # Ajusta a posição do jogador para a parte inferior do bloco.
                    player.direction.y = 0                   # O jogador não está nem se movendo para cima e nem para baixo. 
                    player.on_ground = True                  # O jogador está tocando no chão. 
                else:                                        # Do contrário... 
                    player.on_ground = False                 # Ele não estará tocando no chão. 

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1: # Se o jogador estiver tocando no chão e estiver se movendo para cima ou estiver caindo...
            player.on_ground = False                                              # O jogador não está tocando no chão.
        if player.on_ceiling and player.direction.y > 0:                          # Se o jogador estiver tocando o teto e está se movendo para baixo... 
            player.on_ceiling = False                                             # O jogador não está tocando no teto.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def blastattack(self, screen):

        self.attack_rect.x -= self.splashspeed
        self.attack_rect2.x -= self.splashspeed 
        self.attack_rect3.x -= self.splashspeed 

        pygame.draw.rect(screen, (255, 255, 255), self.attack_rect3)

        if self.healthboss < 99:
            if self.attack_rect3.x < 0:
                self.attack_rect3.x = 1200  
                self.attack_rect3.y = random.randint(1, 604)
                pygame.draw.rect(self.display_surface, (255, 255, 0), self.attack_rect3)

        pygame.draw.rect(screen, (255, 255, 0), self.attack_rect2)

        print(self.healthboss)

        if self.healthboss < 99:
            if self.attack_rect2.x < 0:
                self.attack_rect2.x = 1200  
                self.attack_rect2.y = random.randint(1, 604)
                pygame.draw.rect(self.display_surface, (255, 255, 0), self.attack_rect2)

        pygame.draw.rect(screen, (255, 0, 0), self.attack_rect)

        if self.attack_rect.x < 0:
            self.attack_rect.x = 1200
            self.attack_rect.y = random.randint(1, 604)
            pygame.draw.rect(self.display_surface, (255, 0, 0), self.attack_rect)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def draw_health_bar(self, health, x, y, screen): # Método para criar uma barra de pontos de vida na tela. 

        WHITE = (255, 255, 255) # Recebe a cor branca. 
        RED = (255, 0, 0)       # Recebe a cor vermelha. 
        YELLOW = (255, 255, 0)  # Recebe a cor amarela. 

        ratio = health / 100    # Recebe os pontos de vida / pelos pontos de saúde.  

        pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))  # Desenha um retângulo branco que serve como fundo da barra de saúde. 
                                                                  # Ele é ligeiramente maior que a barra de saúde para criar uma borda ao redor dela.
        pygame.draw.rect(screen, RED, (x, y, 400, 30))            # Desenha um retângulo vermelho representando a parte da barra de saúde que está faltando devido à perda de saúde.
        pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30)) # Desenha um retângulo amarelo representando a parte da barra de saúde proporcional à saúde atual. 
                                                                  # A largura desse retângulo é proporcional à variável ratio, indicando a porcentagem de saúde atual em relação à saúde máxima.

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def intro(self): # Método para rodar a tela de introducão. 
        self.display_surface.blit(self.backgroundintro, (0, 0)) # O método apenas chama o método de renderizacão para carregar a tela. 

    def run(self, current_level): # O método run é chamado para desenhar a Fase na tela.
                   # A ordem de sobreposicão vai de quem é desenhado primeiro em ordem de surgimento.    
                                                           
                   # Eventos de Cenário. 
        if current_level == 1:
            self.display_surface.blit(self.background, (0, 0))                      # O método apenas chama o método de renderizacão para carregar a tela. 
            self.tiles.draw(self.display_surface)                                   # Usa o método draw do grupo de sprites tiles para desenhar todos os Blocos na superfície display_surface.
            self.draw_health_bar(self.health, self.x, self.y, self.display_surface) # Chama o método para desenhar barra de saúde na tela. 
        elif current_level == 2:
            self.display_surface.blit(self.stage2, (0, 0))
            self.tiles.draw(self.display_surface)
            self.draw_health_bar(self.health, self.x, self.y, self.display_surface) # Chama o método para desenhar barra de saúde na tela. 
        elif current_level == 3:
            self.display_surface.blit(self.stage3, (0, 0))
            self.tiles.draw(self.display_surface)
            self.draw_health_bar(self.health, self.x, self.y, self.display_surface) # Chama o método para desenhar barra de saúde na tela. 
        elif current_level == 4:
            self.display_surface.blit(self.stage4, (0, 0))
            self.tiles.draw(self.display_surface)
            self.draw_health_bar(self.health, self.x, self.y, self.display_surface) # Chama o método para desenhar barra de saúde na tela. 
        elif current_level == 5:
            self.display_surface.blit(self.stage5, (0, 0))
            self.tiles.draw(self.display_surface)
            self.draw_health_bar(self.health, self.x, self.y, self.display_surface) # Chama o método para desenhar barra de saúde na tela. 
            self.draw_health_bar(self.healthboss, 790, self.y, self.display_surface)
        
             # Eventos do Jogador/Inimigos. 
        self.player.update()                     # Invoca todos os métodos da classe Player. 
        self.enemies.update()                    # Invoca todos os métodos da classe Enemies. 
        self.necromancer.update()

        self.player.draw(self.display_surface)   # Usa o método draw do groupsingle para desenhar o personagem na superfície display_surface.
        self.enemies.draw(self.display_surface)      # Usa o método draw do groupsingle para desenhar o inimigo na superfície display_surface.
        self.necromancer.draw(self.display_surface)  # Usa o método draw do groupsingle para desenhar o inimigo na superfície display_surface.

        if len(self.necroboss) > 0:  # Verifica se o grupo necroboss não está vazio.
            self.necroboss.update()    
            self.necroboss.draw(self.display_surface)  # Usa o método draw do groupsingle para desenhar o inimigo na superfície display_surface.

        self.horizontal_movement_collision()     # Usa o método horizontal_movement_collision para verificar colisões horizontais.
        self.vertical_movement_collision()       # Usa o método horizontal_movement_collision para verificar colisões verticais.
        self.blastattack(self.display_surface)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
