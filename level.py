#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

import pygame 
import random
from tiles import Tile
from settings import tile_size, screen_width, screen_height
from player import Player
from enemies import Enemies
from necroboss import Necroboss
from hellhound import Hellhound

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Classe 'Level'
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
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
# - blastattack(self, screen):  # Método para simular o ataque do boss.
# 
# - gameover(self): # Método para rodar a tela de game over.
#
# A classe utiliza grupos de sprites para armazenar os blocos ('tiles') e o jogador ('player_group'), permitindo a atualização e desenho eficientes dos elementos na tela durante a execução do jogo.

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class Level:
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def __init__(self, level_data, surface, current_level): # O método __init__ é chamado automaticamente quando uma nova instância do jogo é criada.
                                                            # level_data contém informacões sobre a disposicão do blocos... 
                                                            # surface é a superfície onde o nível será exibido. 
                                                            # current_level recebe o número da fase a qual o jogador acessa. 

        # Level Setup.
        self.display_surface = surface # Armazena a superfície onde a Fase será exibida. 
        self.setup_level(level_data)   # A funcao recebe a lista com os mapas e sprites inseridose a devolve tudo como argumento da classe.

#----------------------------------------------------------#

        # Backgrounds.
        self.background = pygame.image.load('./graphics/scenarios/1.png').convert()                         # Recebe a imagem de fundo.
        self.backgroundintro = pygame.image.load('./graphics/scenarios/intro.jpg').convert()                # Recebe a imagem de fundo da intro.
        self.backgroundintro = pygame.transform.scale(self.backgroundintro, (screen_width, screen_height))  # Recebe o tamanho da imagem da intro. 
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))            # Recebe o tamanho da imagem. 
        self.stage2 = pygame.image.load('./graphics/scenarios/stage2.png').convert()                        # Recebe a imagem do estágio2.
        self.stage2 = pygame.transform.scale(self.stage2, (screen_width, screen_height))                    # Recebe o tamanho da imagem.
        self.stage3 = pygame.image.load('./graphics/scenarios/stage3.jpg').convert()                        # Recebe a imagem do estágio3.
        self.stage3 = pygame.transform.scale(self.stage3, (screen_width, screen_height))                    # Recebe o tamanho da imagem.
        self.stage4 = pygame.image.load('./graphics/scenarios/stage4.png').convert()                        # Recebe a imagem do estágio4.
        self.stage4 = pygame.transform.scale(self.stage4, (screen_width, screen_height))                    # Recebe o tamanho da imagem.
        self.stage5 = pygame.image.load('./graphics/scenarios/stage5.jpg').convert()                        # Recebe a imagem do estágio5.
        self.stage5 = pygame.transform.scale(self.stage5, (screen_width, screen_height))                    # Recebe o tamanho da imagem.
        self.finaldeath = pygame.image.load('./graphics/scenarios/gameover.jpg').convert()                  # Recebe a imagem da tela de gameover.
        self.finaldeath = pygame.transform.scale(self.finaldeath, (screen_width, screen_height))            # Recebe o tamanho da imagem.
        self.end = pygame.image.load('./graphics/scenarios/ending.png').convert()                           # Recebe a imagem da tela de encerramento.
        self.end = pygame.transform.scale(self.end, (screen_width, screen_height))                          # Recebe o tamanho da imagem.

#----------------------------------------------------------#

        # Ferramentas.
        self.health = 100                            # Valor default da barra de HP do jogador.
        self.healthboss = 100                        # Valor default da barra de HP do chefe. 
        self.x = 10                                  # Coordenada x (horizontal) onde a barra de saúde será desenhada na tela. 
        self.y = 10                                  # Coordenada y (vertical) onde a barra de saúde será desenhada na tela. 
        self.hurt_timer = 0                          # Recebe o tempo de tempo em que muda o comportamento para machucado.
        self.splashspeed = 10                        # Velocidade dos projéteis atirados pelo chefe.
        self.random_width = random.randint(1, 604)   # Altura randômica dos projéteis atirados pelo chefe.
        self.count_taunt = 0                         # Contador de provocacões do boss que referencia qual arquivo de áudio será usado.
        self.timer = 100                             # Um timer para cronometrar de quanto tempo o comportamento do boss muda.
        self.timer_teleport = 200                    # Um timer para cronometrar de quanto em quanto tempo o chefe teleporta estando ele sem ser atacado.
        self.current_x = 0                           # Recebe a posicão horizontal atual. 
        self.game_state = "running"                  # Boleana para ajudar em transicões de tela.

#----------------------------------------------------------#

        # Projéteis.
        self.attack_rect = pygame.Rect(600, self.random_width, 50, 50)   # Retângulo de projétil atirado pelo chefe.
        self.attack_rect2 = pygame.Rect(600, self.random_width, 50, 50)  # Retângulo de projétil atirado pelo chefe.
        self.attack_rect3 = pygame.Rect(600, self.random_width, 50, 50)  # Retângulo de projétil atirado pelo chefe.                                                                     

#----------------------------------------------------------#

        # Áudios.
        pygame.mixer.init()
        self.blow_sfx = pygame.mixer.Sound('./graphics/sounds/scenario/blow.mp3')          # Áudio de ataque.
        self.blow_skull = pygame.mixer.Sound('./graphics/sounds/scenario/blow_skull.mp3')  # Áudio de esqueleto sendo atingido.
        self.hurt_sfx = pygame.mixer.Sound('./graphics/sounds/scenario/hurt.mp3')          # Áudio do personagem se machucando.
        self.taunt2_sfx = pygame.mixer.Sound('./graphics/sounds/scenario/taunt2.wav')      # Áudio de provocacão do chefe.
        self.taunt3_sfx = pygame.mixer.Sound('./graphics/sounds/scenario/taunt3.wav')      # Áudio de provocacão do chefe.
        self.taunt4_sfx = pygame.mixer.Sound('./graphics/sounds/scenario/taunt4.wav')      # Áudio de provocacão do chefe.
        self.taunt5_sfx = pygame.mixer.Sound('./graphics/sounds/scenario/taunt5.wav')      # Áudio de provocacão do chefe.
        self.taunt6_sfx = pygame.mixer.Sound('./graphics/sounds/scenario/taunt6.wav')      # Áudio de provocacão do chefe.
        self.taunt7_sfx = pygame.mixer.Sound('./graphics/sounds/scenario/taunt7.wav')      # Áudio de risada do chefe.

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def setup_level(self, layout):  # O método setup_level é responsável por inicializar o nível do jogo com base em um layout fornecido
                                    # layout é a representacão do layout da Fase que está em settings.py. 
                                    # Todo o layout será entregue como argumento para a classe principal.

        self.tiles = pygame.sprite.Group()              # Um grupo de sprites chamado tiles é criado para armazenar os Blocos que serão criados.
        self.player = pygame.sprite.GroupSingle()       # Um grupo de sprites chamado player é criado para armazenar o personagem que será criado.
        self.enemies = pygame.sprite.Group()            # Um grupo de sprites chamado enemies é criado para armazenar o inimigo que será criado.
        self.necroboss = pygame.sprite.GroupSingle()    # Um grupo de sprites chamado necroboss é criado para armazenar o personagem que será criado.
        self.hellhound = pygame.sprite.Group()          # Um grupo de sprites chamado hellhound é criado para armazenar os Blocos que serão criados.

        for row_index, row in enumerate(layout):   # Um loop aninhado percorre cada célula no layout usando enumerate...
            for col_index, cell in enumerate(row): # ...para obter tanto os índices quanto os valores.
                x = col_index * tile_size          # x Recebe o index das colunas. 
                y = row_index * tile_size          # y Recebe o index das linhas.

                if cell == 'X':                               # Se ao percorrer o layout for encontrado um X...
                    tile = Tile((x, y), tile_size)            # Cria uma instância do Bloco (tile), com a posicão x e y.
                    self.tiles.add(tile)                      # Esse bloco é adicionado ao grupo de sprites tiles.
                if cell == 'P':                               # Se ao percorrer o layout for encontrado um P...
                    player_sprite = Player((x, y))            # Cria uma instância do Jogador (Player), com a posicão x e y.
                    self.player.add(player_sprite)            # Esse bloco é adicionado ao grupo de sprites player.
                if cell == 'S':                               # Se ao percorrer o layout for encontrado um S...
                    enemies_sprite = Enemies((x, y))          # Cria uma instância do inimigo, com a posicão x e y.
                    self.enemies.add(enemies_sprite)          # Esse bloco é adicionado ao grupo de sprites enemies.
                if cell == 'B':                               # Se ao percorrer o layout for encontrado um B...
                    necroboss_sprite = Necroboss((x, y))      # Cria uma instância do Chefe, com a posicão x e y.
                    self.necroboss.add(necroboss_sprite)      # Esse bloco é adicionado ao grupo de sprites necrboss.
                if cell == 'H':
                    hellhound_sprite = Hellhound((x, y))
                    self.hellhound.add(hellhound_sprite)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        # O pygame é capaz de detectar colisões, mas ele não é capaz de dizer onde as colisões ocorreram.
        # Então devemos separar os movimentos verticais e horizontais juntamente com as suas respectivas colisões.

        # 1.Aplicacao de Movimento Vertical. 
        # 2.Verificacão de Colisão Vertical. 
        # 3.Aplicacao de Movimento Horizontal. 
        # 4.Verificacão de Colisão Horizontal. 

    def horizontal_movement_collision(self): # Método responsável por lidar com o movimento horizontal do jogador e verificar colisões horizontais.

        player = self.player.sprite                          # player recebe o sprite do Jogador. 
        player.rect.x += player.direction.x * player.speed   # Atualiza a posicão horizontal do retângulo do jogador incrementando-o. 
                                                             # Multiplicá-lo por qualquer número aumenta a velocidade. 
                                                             
        enemies = self.enemies.sprites()[0]                    # Os inimigos recebem os sprite deles.  
        enemies.rect.x += enemies.direction.x * enemies.speed  # Atualiza a posicão horizontal dos retângulos dos inimigos incrementando-os. 
                                                               # Multiplicá-lo por qualquer número aumenta a velocidade. 
        hellhound_sprite = self.hellhound.sprites()            # Corrigindo a variável hellhound_sprite.

        if hellhound_sprite:                 # Verifica se o sprite do hellhound existe.
            hellhound = hellhound_sprite[0]  # Corrigindo o acesso ao sprite do hellhound.
            hellhound.rect.x += hellhound.direction.x * hellhound.speed

        necroboss_sprite = self.necroboss.sprite # O chefe recebe o seu sprite.

        if necroboss_sprite:                                             # Se o sprite do boss existir.
            necroboss = necroboss_sprite                                 # Cria-se uma nova variável para receber o sprite.
            necroboss.rect.x += necroboss.direction.x * necroboss.speed  # Atualiza a posicão horizontal dos retângulos dos inimigos incrementando-os. 
                                                                         # Multiplicá-lo por qualquer número aumenta a velocidade. 

        # Esta condicão foi criada para acabar com os erros de frame_index.
 
#----------------------------------------------------------#

        # Jogador vs Inimigos. 

        # Esqueletos.
        for enemy in self.enemies.sprites():                 # Itera sobre todos os sprites de inimigos no grupo de enemies.
            enemy.rect.x += enemy.direction.x * enemy.speed  # Atualiza a posição horizontal (x) de um inimigo no seu jogo.

            if player.rect.colliderect(enemy.rect):          # Se o retângulo do jogador colidir com o do inimigo.
                if player.direction.x < 0:                   # Se o jogador estiver indo para a esquerda. 
                    player.rect.left = enemy.rect.right      # O retângulo do jogador recebe o valor do retângulo direito do inimigo.
                    player.on_left = True                    # O jogador estará indo para a esquerda.
                    self.current_x = player.rect.left        # A posição atual do jogador em x é atualizada para a borda esquerda do retângulo do jogador.
                    if player.blow == True:                  # Se o jogador estiver golpeando...
                        self.blow_sfx.play()                 # Reproduz o áudio.
                        self.blow_skull.play()               # Reproduz o áudio.
                        self.enemies.remove(enemy)           # Remove o inimigo do grupo de sprites.
                        player.blow = False                  # Redefine a flag de ataque.
                    else:                                    # Se o jogador não estiver golpeando...
                        player.status = 'hurt'               # O jogador recebe o status de machucado.
                        self.hurt_sfx.play()                 # Reproduz o áudio.
                        self.health -= 1                     # Deduz da saúde do jogador.
                elif player.direction.x > 0:                 # Se o jogador estiver indo para a direita.
                    player.rect.right = enemy.rect.left      # Se o jogador estiver indo para a direita, o retângulo do jogador recebe o valor do retângulo esquerdo do inimigo.
                    player.on_right = True                   # O jogador estará indo para a direita.
                    self.current_x = player.rect.right       # A posição atual do jogador em x é atualizada para a borda direita do retângulo do jogador.
                    if player.blow == True:                  # Se o jogador estiver golpeando...
                        self.blow_sfx.play()                 # Reproduz o áudio.
                        self.blow_skull.play()               # Reproduz o áudio.
                        self.enemies.remove(enemy)           # Remove o inimigo do grupo de sprites.
                        player.blow = False                  # Redefine a flag de ataque.
                    else:                                    # Se o jogador não estiver golpeando...
                        player.status = 'hurt'               # O jogador recebe o status de machucado.
                        self.hurt_sfx.play()                 # Reproduz o áudio.
                        self.health -= 1                     # Deduz da saúde do jogador.      

                if player.status == 'hurt':                  # Se o jogador estiver machucado...
                    if player.direction.x < 0:               # E estiver indo para a esquerda...
                        player.rect.x += 20                  # Ele é afastado para a direita. 
                    elif player.direction.x > 0:             # E se estiver indo para a direita... 
                        player.rect.x -= 20                  # Ele é afastado para a esquerda. 

                if self.health <= 0:                         # Se a barra de pontos de vida chegar a zero...
                    self.gameover()                          # O método de saída do jogo é ativado...

        # Hellhounds.
        for hound in hellhound_sprite:                       # Itera sobre todos os sprites de inimigos no grupo de enemies.
            hound.rect.x += hound.direction.x * hound.speed  # Atualiza a posição horizontal (x) de um inimigo no seu jogo.

            if player.rect.colliderect(hound.rect):      # Se o retângulo do jogador colidir com o do hellhound.
                if player.direction.x < 0:               # Se o jogador estiver indo para a direita.
                    player.rect.left = hound.rect.right  # O retângulo do jogador recebe o valor do retângulo direito do hellhound.
                    player.on_left = True                # O jogador estará indo para a esquerda.
                    self.current_x = player.rect.left    # A posição atual do jogador em x é atualizada para a borda esquerda do retângulo do jogador.
                    if player.blow == True:              # Se o jogador estiver golpeando...
                        self.blow_sfx.play()             # Reproduz o áudio.
                        self.blow_skull.play()           # Reproduz o áudio.
                        self.hellhound.remove(hound)     # Remove o hellhound do grupo de sprites.
                        player.blow = False              # Redefine a flag de ataque.
                    else:                                # Se o jogador não estiver golpeando...
                        player.status = 'hurt'           # O jogador recebe o status de machucado.
                        self.hurt_sfx.play()             # Reproduz o áudio.
                        self.health -= 1                 # Deduz da saúde do jogador.
                elif player.direction.x > 0:             # Se o jogador estiver indo para a direita.
                    player.rect.right = hound.rect.left  # Se o jogador estiver indo para a direita, o retângulo do jogador recebe o valor do retângulo esquerdo do hellhound.
                    player.on_right = True               # O jogador estará indo para a direita.
                    self.current_x = player.rect.right   # A posição atual do jogador em x é atualizada para a borda direita do retângulo do jogador.
                    if player.blow == True:              # Se o jogador estiver golpeando...
                        self.blow_sfx.play()             # Reproduz o áudio.
                        self.blow_skull.play()           # Reproduz o áudio.
                        self.hellhound.remove(hound)     # Remove o hellhound do grupo de sprites.
                        player.blow = False              # Redefine a flag de ataque.
                    else:                                # Se o jogador não estiver golpeando...
                        player.status = 'hurt'           # O jogador recebe o status de machucado.
                        self.hurt_sfx.play()             # Reproduz o áudio.
                        self.health -= 1                 # Deduz da saúde do jogador.

                if player.status == 'hurt':              # Se o jogador estiver machucado...
                    if player.direction.x < 0:           # E estiver indo para a esquerda...
                        player.rect.x += 20              # Ele é afastado para a direita.
                    elif player.direction.x > 0:         # E se estiver indo para a direita...
                        player.rect.x -= 20              # Ele é afastado para a esquerda.

                if self.health <= 0:                     # Se a barra de pontos de vida chegar a zero...
                    self.gameover()                      # O método de saída do jogo é ativado...

#----------------------------------------------------------#

        # Jogador vs Boss.

        for boss in self.necroboss.sprites():           # Itera sobre todos os sprites do chefe no grupo de necroboss.                
        
            if player.rect.colliderect(boss.rect):      # Se o retângulo do jogador colidir com o do chefe.
                if player.direction.x < 0:              # Se o jogador estiver indo para a esquerda.
                    player.rect.left = boss.rect.right  # O retângulo do jogador recebe o valor do retângulo direito do chefe.
                    player.on_left = True               # O jogador estará indo para a esquerda.
                    self.current_x = player.rect.left   # A posição atual do jogador em x é atualizada para a borda esquerda do retângulo do jogador.
                    if player.blow == True:             # Se o jogador estiver golpeando...
                        necroboss.special_moves()       # O boss ativa o Teletransporte.
                        self.healthboss -= 20           # Remove o chefe do grupo de sprites.
                        self.count_taunt += 1           # Aumenta o contador para reproduzir o próximo áudio.
                        necroboss.status = 'hurt'       # O status do boss muda.
                        player.blow = False             # Redefine a flag de ataque.
                    else:                               # Se o jogador não estiver golpeando...
                        player.status = 'hurt'          # O jogador recebe o status de machucado.
                        self.hurt_sfx.play()            # Reproduz o áudio.
                        necroboss.status = 'teleport'   # O status do boss muda. 
                        necroboss.special_moves()       # O boss usa teletransporte.
                        self.health -= 10               # Deduz da saúde do jogador.
                elif player.direction.x > 0:            # Se o jogador estiver indo para a direita.
                    player.rect.right = boss.rect.left  # Se o jogador estiver indo para a direita, o retângulo do jogador recebe o valor do retângulo esquerdo do chefe.
                    player.on_right = True              # O jogador estará indo para a direita.
                    self.current_x = player.rect.right  # A posição atual do jogador em x é atualizada para a borda direita do retângulo do jogador.
                    if player.blow == True:             # Se o jogador estiver golpeando...
                        necroboss.special_moves()       # O boss ativa o Teletransporte.
                        self.healthboss -= 20           # Remove o chefe do grupo de sprites.
                        self.count_taunt += 1           # Aumenta o contador para reproduzir o próximo áudio.
                        necroboss.status = 'hurt'       # O status do boss muda.
                        player.blow = False             # Redefine a flag de ataque.
                    else:                               # Se o jogador não estiver golpeando...
                        player.status = 'hurt'          # O jogador recebe o status de machucado.
                        self.hurt_sfx.play()            # Reproduz o áudio.
                        necroboss.status = 'teleport'   # O status do boss muda. 
                        necroboss.special_moves()       # O boss usa teletransporte.
                        self.health -= 10               # Deduz da saúde do jogador.

                if player.status == 'hurt':             # Se o jogador estiver machucado...
                    if player.direction.x < 0:          # E estiver indo para a esquerda...
                        player.rect.x += 20             # Ele é afastado para a direita.
                    elif player.direction.x > 0:        # E se estiver indo para a direita...
                        player.rect.x -= 20             # Ele é afastado para a esquerda.

#----------------------------------------------------------#

                # Transicão de Tela.

                if self.health <= 0:        # Se a barra de pontos de vida chegar a zero...
                    self.taunt7_sfx.play()  # Reproduz o áudio.
                    self.gameover()         # O evento de saída do jogo é ativado...

                if self.healthboss <= 0:    # Se o pv do boss chegar a 0 ou menos...
                    self.ending()           # Chama o método de encerramento.

#----------------------------------------------------------#

                # Mudanca de Provocacões.

                if self.count_taunt == 1:    # Se o contador de provocacões receber 1.
                    self.taunt2_sfx.play()   # Reproduz o áudio.
                elif self.count_taunt == 2:  # Se o contador de provocacões receber 1.
                    self.taunt3_sfx.play()   # Reproduz o áudio.
                elif self.count_taunt == 3:  # Se o contador de provocacões receber 1.
                    self.taunt4_sfx.play()   # Reproduz o áudio.
                elif self.count_taunt == 4:  # Se o contador de provocacões receber 1.
                    self.taunt5_sfx.play()   # Reproduz o áudio.
                elif self.count_taunt == 5:  # Se o contador de provocacões receber 1.
                    self.taunt6_sfx.play()   # Reproduz o áudio.

#----------------------------------------------------------#
            
        # Cronômetro de Comportamentos.
            
        self.timer -= 1          # Decrementa sempre o timer.
        self.timer_teleport -=1  # Decrementa sempre o timer.

        if self.timer == 0:            # Se o cronômetro chegar a zero...
            self.timer = 100           # Reseta o cronômetro.
            necroboss.status = 'idle'  # Reseta o comportamento.

        if self.timer_teleport == 0:       # Se o cronômetro chegar a zero...
            necroboss.status = 'teleport'  # Reproduz o comportamento.
            necroboss.special_moves()      # O boss usa teletransporte.
            self.timer_teleport = 200      # Reseta o cronômetro.

#----------------------------------------------------------#

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

#----------------------------------------------------------#

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

#----------------------------------------------------------#

            # Jogador vs Projéteis.

            if self.attack_rect.colliderect(player.rect):      # Se houver colisão de retângulos entre o projétil e o jogador.
                player.status == 'hurt'                        # Altera o comportamento do jogador.
                self.hurt_sfx.play()                           # Reproduz o comportamento.
                self.health -= 1                               # Decrementa o valor da saúde do jogador.
                if player.direction.x < 0:                     # Se o jogador estiver indo para a direita...
                    player.rect.left = self.attack_rect.right  # O retângulo do lado esquerdo do jogador recebe o retângulo do lado direito do projétil.
                    player.on_left = True                      # Define o lugar do jogador como estando do lado esquerdo.
                    self.current_x = player.rect.left          # A posicão atual do jogador recebe o lado direito do retângulo.
                elif player.direction.x > 0:                   # Se o jogador estiver indo para a esquerda...
                    player.rect.right = self.attack_rect.left  # O retângulo do lado direito do jogador recebe o retângulo do lado esquerdo do projétil.
                    player.on_right = True                     # Define o lugar do jogador como estando do lado direito.
                    self.current_x = player.rect.right         # A posicão atual do jogador recebe o lado esquerdo do retângulo.
                elif player.direction.x == 0:                  # Se o jogador estiver parado.
                    player.rect.right = self.attack_rect.left  # O retângulo do lado direito do jogador recebe o retângulo do lado esquerdo do projétil.
                    player.on_right = True                     # Define o lugar do jogador como estando do lado direito.
                    self.current_x = player.rect.right         # A posicão atual do jogador recebe o lado direito do retângulo.
                if player.direction.y > 0:                     # Se o jogador estiver caindo...
                    player.rect.bottom = self.attack_rect.top  # O retângulo de baixo do jogador recebe o retângulo de cima do projétil.
                    player.on_ground = True                    # Define o lugar do jogador como estando no chão.
                if player.direction.y < 0:                     # Se estiver saltando...
                    player.rect.top = self.attack_rect.bottom  # O retângulo de cima do jogador recebe o retângulo de cima do baixo.
                    player.on_ground = True                    # O jogador estará no chão
            
            if self.attack_rect2.colliderect(player.rect):      # Se houver colisão de retângulos entre o projétil e o jogador.
                player.status == 'hurt'                         # Altera o comportamento do jogador.
                self.hurt_sfx.play()                            # Reproduz o comportamento.
                self.health -= 1                                # Decrementa o valor da saúde do jogador.
                if player.direction.x < 0:                      # Se o jogador estiver indo para a direita...
                    player.rect.left = self.attack_rect2.right  # O retângulo do lado esquerdo do jogador recebe o retângulo do lado direito do projétil.
                    player.on_left = True                       # Define o lugar do jogador como estando do lado esquerdo.
                    self.current_x = player.rect.left           # A posicão atual do jogador recebe o lado direito do retângulo.
                elif player.direction.x > 0:                    # Se o jogador estiver indo para a esquerda...
                    player.rect.right = self.attack_rect2.left  # O retângulo do lado direito do jogador recebe o retângulo do lado esquerdo do projétil.
                    player.on_right = True                      # Define o lugar do jogador como estando do lado direito.
                    self.current_x = player.rect.right          # A posicão atual do jogador recebe o lado esquerdo do retângulo.
                elif player.direction.x == 0:                   # Se o jogador estiver parado.
                    player.rect.right = self.attack_rect2.left  # O retângulo do lado direito do jogador recebe o retângulo do lado esquerdo do projétil.
                    player.on_right = True                      # Define o lugar do jogador como estando do lado direito.
                    self.current_x = player.rect.right          # A posicão atual do jogador recebe o lado direito do retângulo.
                if player.direction.y > 0:                      # Se o jogador estiver caindo...
                    player.rect.bottom = self.attack_rect2.top  # O retângulo de baixo do jogador recebe o retângulo de cima do projétil.
                    player.on_ground = True                     # Define o lugar do jogador como estando no chão.
                if player.direction.y < 0:                      # Se estiver saltando...
                    player.rect.top = self.attack_rect2.bottom  # O retângulo de cima do jogador recebe o retângulo de cima do baixo.
                    player.on_ground = True                     # O jogador estará no chão

            if self.attack_rect3.colliderect(player.rect):      # Se houver colisão de retângulos entre o projétil e o jogador.
                player.status == 'hurt'                         # Altera o comportamento do jogador.
                self.hurt_sfx.play()                            # Reproduz o comportamento.
                self.health -= 1                                # Decrementa o valor da saúde do jogador.
                if player.direction.x < 0:                      # Se o jogador estiver indo para a direita...
                    player.rect.left = self.attack_rect3.right  # O retângulo do lado esquerdo do jogador recebe o retângulo do lado direito do projétil.
                    player.on_left = True                       # Define o lugar do jogador como estando do lado esquerdo.
                    self.current_x = player.rect.left           # A posicão atual do jogador recebe o lado direito do retângulo.
                elif player.direction.x > 0:                    # Se o jogador estiver indo para a esquerda...
                    player.rect.right = self.attack_rect3.left  # O retângulo do lado direito do jogador recebe o retângulo do lado esquerdo do projétil.
                    player.on_right = True                      # Define o lugar do jogador como estando do lado direito.
                    self.current_x = player.rect.right          # A posicão atual do jogador recebe o lado esquerdo do retângulo.
                elif player.direction.x == 0:                   # Se o jogador estiver parado.
                    player.rect.right = self.attack_rect3.left  # O retângulo do lado direito do jogador recebe o retângulo do lado esquerdo do projétil.
                    player.on_right = True                      # Define o lugar do jogador como estando do lado direito.
                    self.current_x = player.rect.right          # A posicão atual do jogador recebe o lado direito do retângulo.
                if player.direction.y > 0:                      # Se o jogador estiver caindo...
                    player.rect.bottom = self.attack_rect3.top  # O retângulo de baixo do jogador recebe o retângulo de cima do projétil.
                    player.on_ground = True                     # Define o lugar do jogador como estando no chão.
                if player.direction.y < 0:                      # Se estiver saltando...
                    player.rect.top = self.attack_rect3.bottom  # O retângulo de cima do jogador recebe o retângulo de cima do baixo.
                    player.on_ground = True                     # O jogador estará no chão

#----------------------------------------------------------#

        # Limitacões de Movimento.

        if player.rect.left < 0:               # Se o retângulo esquerdo do jogador ultrapassar a tela...
            player.rect.left = 0               # A posicão dele receberá 0.
        elif player.rect.right > screen_width: # Se o retângulo esquerdo do jogador ultrapassar a tela do lado direito...
            player.rect.right = screen_width   # # A posicão dele receberá o limite do lado direito.

#----------------------------------------------------------#

        # Verificacão de Posicão.

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):    # Se o jogador estiver a esquerda e o retângulo alinhado a esquerda for menor que a variável que o recebe ou maior ou igual a zero...
            player.on_left = False                                                               # O jogador não está do lado esquerdo.
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):  # Se o jogador estiver a direita e o retângulo alinhado a direita for maior que a variável que o recebe ou menor ou igual a zero...
            player.on_right = False                                                              # O jogador não está do lado direito.

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def vertical_movement_collision(self): # Método responsável por lidar com o movimento vertical do jogador e verificar colisões verticais.

        # Gravidade aos Inimigos. 

        for enemy in self.enemies.sprites():                      # Itera sobre todos os sprites de inimigos no grupo de enemies.
            enemy.apply_gravity()                                 # Aplica a gravidade aos inimigos.

            for sprite in self.tiles.sprites():                   # Itera sobre todos os sprites de blocos no grupo de tiles.
                if sprite.rect.colliderect(enemy.rect):           # Se houver uma colisão entre o inimigo e um Bloco...
                    if enemy.direction.y > 0:                     # Se o inimigo estiver se movendo para baixo...
                        enemy.rect.bottom = sprite.rect.top  -13  # Ajusta a posição do inimigo para a parte superior do bloco.
                        enemy.direction.y = 0                     # O inimigo não está nem se movendo para cima e nem para baixo. 
                        enemy.on_ground = True                    # O inimigo está tocando no chão. 
                    elif enemy.direction.y < 0:                   # Se o inimigo estiver se movendo para cima...
                        enemy.rect.top = sprite.rect.bottom       # Ajusta a posição do inimigo para a parte inferior do bloco.
                        enemy.direction.y = 0                     # O inimigo não está nem se movendo para cima e nem para baixo. 
                        enemy.on_ground = True                    # O inimigo está tocando no chão.
                    else:                                         # Do contrário... 
                        enemy.on_ground = False                   # Ele não estará tocando no chão. 

        for hellhound in self.hellhound.sprites():
            hellhound.apply_gravity()

            for sprite in self.tiles.sprites():                   # Itera sobre todos os sprites de blocos no grupo de tiles.
                if sprite.rect.colliderect(hellhound.rect):       # Se houver uma colisão entre o inimigo e um Bloco...
                    if hellhound.direction.y > 0:                 # Se o inimigo estiver se movendo para baixo...
                        hellhound.rect.bottom = sprite.rect.top   # Ajusta a posição do inimigo para a parte superior do bloco.
                        hellhound.direction.y = 0                 # O inimigo não está nem se movendo para cima e nem para baixo. 
                        hellhound.on_ground = True                # O inimigo está tocando no chão. 
                    elif hellhound.direction.y < 0:               # Se o inimigo estiver se movendo para cima...
                        hellhound.rect.top = sprite.rect.bottom   # Ajusta a posição do inimigo para a parte inferior do bloco.
                        hellhound.direction.y = 0                 # O inimigo não está nem se movendo para cima e nem para baixo. 
                        hellhound.on_ground = True                # O inimigo está tocando no chão.
                    else:                                         # Do contrário... 
                        hellhound.on_ground = False               # Ele não estará tocando no chão.

#----------------------------------------------------------#

        # Gravidade ao Jogador.

        player = self.player.sprite                         # player recebe o sprite do Jogador. 
        player.apply_gravity()                              # Chama o método apply_gravity.

        for sprite in self.tiles.sprites():                 # Itera sobre todos os sprites de blocos no grupo de tiles.
            if sprite.rect.colliderect(player.rect):        # Se houver uma colisão entre o Jogador e um Bloco...
                if player.direction.y > 0:                  # Se o jogador estiver se movendo para baixo...
                    player.rect.bottom = sprite.rect.top    # Ajusta a posição do jogador para a parte superior do bloco.
                    player.direction.y = 0                  # O jogador não está nem se movendo para cima e nem para baixo. 
                    player.on_ground = True                 # O jogador está tocando no chão. 
                elif player.direction.y < 0:                # Se o jogador estiver se movendo para cima...
                    self.hurt_sfx.play()
                    player.rect.top = sprite.rect.bottom    # Ajusta a posição do jogador para a parte inferior do bloco.
                    player.direction.y = 0                  # O jogador não está nem se movendo para cima e nem para baixo. 
                    player.on_ground = True                 # O jogador está tocando no chão. 
                else:                                       # Do contrário... 
                    player.on_ground = False                # Ele não estará tocando no chão. 

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:  # Se o jogador estiver tocando no chão e estiver se movendo para cima ou estiver caindo...
            player.on_ground = False                                               # O jogador não está tocando no chão.
        if player.on_ceiling and player.direction.y > 0:                           # Se o jogador estiver tocando o teto e está se movendo para baixo... 
            player.on_ceiling = False                                              # O jogador não está tocando no teto.

#----------------------------------------------------------#

        # Verificacão de Limite de Tela.

        if player.rect.y > screen_height:                # Se o jogador cair além do limite do mapa...
            self.game_state = "gameover"                 # O estado do jogo recebe game over.

        if player.rect.y > 650 and player.rect.y < 700:  # Se o jogador cair além do limite do mapa...
            self.taunt7_sfx.play()                       # Reproduz o áudio.
            
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def blastattack(self, screen):  # Método para simular o ataque do boss.

        self.attack_rect.x -= self.splashspeed       # Decrementa a posicão horizontal do retângulo.
        self.attack_rect2.x -= self.splashspeed + 2  # Decrementa a posicão horizontal do retângulo.
        self.attack_rect3.x -= self.splashspeed + 3  # Decrementa a posicão horizontal do retângulo.

        # Os retângulos são decrementados em velocidades diferentes para se movimentarem em velocidades diferentes.

        pygame.draw.rect(screen, (0, 0, 0), self.attack_rect3)       # Desenha o retângulo na tela.
        pygame.draw.rect(screen, (0, 0, 255), self.attack_rect3, 2)  # Desenha o retângulo na tela com mais dois de tamanho para simular a borda.

        if self.healthboss < 30:                                                          # Se o pv do boss estiver menor do que 30...
            if self.attack_rect3.x < 0:                                                   # Se o retângulo na posicão horizontal tiver ultrapassado a tela...
                self.attack_rect3.x = 1200                                                # Ele recebe a posicão 1200 da tela.
                self.attack_rect3.y = random.randint(1, 604)                              # A posicão horizontal recebe o valor randômico.
                pygame.draw.rect(self.display_surface, (255, 0, 255), self.attack_rect3)  # O retângulo é desenhado.

        pygame.draw.rect(screen, (0, 0, 0), self.attack_rect2)       # Desenha o retângulo na tela.
        pygame.draw.rect(screen, (255, 0, 0), self.attack_rect2, 2)  # Desenha o retângulo na tela com mais dois de tamanho para simular a borda.

        if self.healthboss < 60:                                                          # Se o pv do boss estiver menor do que 60...
            if self.attack_rect2.x < 0:                                                   # Se o retângulo na posicão horizontal tiver ultrapassado a tela...
                self.attack_rect2.x = 1200                                                # Ele recebe a posicão 1200 da tela.
                self.attack_rect2.y = random.randint(1, 604)                              # A posicão horizontal recebe o valor randômico.
                pygame.draw.rect(self.display_surface, (255, 0, 255), self.attack_rect2)  # O retângulo é desenhado.

        pygame.draw.rect(screen, (0, 0, 0), self.attack_rect)         # Desenha o retângulo na tela.
        pygame.draw.rect(screen, (255, 0, 255), self.attack_rect, 2)  # Desenha o retângulo na tela com mais dois de tamanho para simular a borda.

        if self.attack_rect.x < 100:                                                      # Se o pv do boss estiver menor do que 100...
            self.attack_rect.x = 1200                                                     # Se o retângulo na posicão horizontal tiver ultrapassado a tela...
            self.attack_rect.y = random.randint(1, 604)                                   # Ele recebe a posicão 1200 da tela.
            pygame.draw.rect(self.display_surface, (0, 0, 0), self.attack_rect)           # A posicão horizontal recebe o valor randômico.
            pygame.draw.rect(self.display_surface, (255, 0, 255), self.attack_rect, 2)    # O retângulo é desenhado.

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def draw_health_bar(self, health, x, y, screen): # Método para criar uma barra de pontos de vida na tela. 

        WHITE = (255, 255, 255)  # Recebe a cor branca. 
        RED = (255, 0, 0)        # Recebe a cor vermelha. 
        YELLOW = (255, 255, 0)   # Recebe a cor amarela. 

        ratio = health / 100     # Recebe os pontos de vida / pelos pontos de saúde.  

        pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))  # Desenha um retângulo branco que serve como fundo da barra de saúde. 
                                                                  # Ele é ligeiramente maior que a barra de saúde para criar uma borda ao redor dela.
        pygame.draw.rect(screen, RED, (x, y, 400, 30))            # Desenha um retângulo vermelho representando a parte da barra de saúde que está faltando devido à perda de saúde.
        pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30)) # Desenha um retângulo amarelo representando a parte da barra de saúde proporcional à saúde atual. 
                                                                  # A largura desse retângulo é proporcional à variável ratio, indicando a porcentagem de saúde atual em relação à saúde máxima.

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def intro(self):  # Método para rodar a tela de introducão. 
        self.display_surface.blit(self.backgroundintro, (0, 0))  # O método apenas chama o método de renderizacão para carregar a tela. 

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def gameover(self): # Método para rodar a tela de game over.

        # Como este método pode rodar enquanto as outras fases estão rodando...
        # Precisou-se de uma variável de confirmacão.

        if self.game_state == "gameover":                       # Se o estado do jogo for 'gameover'.
            self.display_surface.blit(self.finaldeath, (0, 0))  # Chama o método de renderizacão para carregar a tela. 

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def ending(self): # Método para rodar a tela de fim de jogo.

        # Como este método pode rodar enquanto as outras fases estão rodando...
        # Precisou-se de uma variável de confirmacão.

        if self.game_state == "endgame":                 # Se o estado do jogo estiver como endgame...
            self.display_surface.blit(self.end, (0, 0))  # Chama o método de renderizacão para carregar a tela. 

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

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

#----------------------------------------------------------#
        
        # Eventos do Jogador/Inimigos. 
        self.player.update()       # Invoca todos os métodos da classe Player. 
        self.enemies.update()      # Invoca todos os métodos da classe Enemies. 

        
        self.hellhound.update() 
        self.hellhound.draw(self.display_surface)

        if len(self.necroboss) > 0:                    # Verifica se o grupo necroboss não está vazio.
            self.necroboss.update()                    # Invoca todos os métodos da classe Necroboss. 
            self.necroboss.draw(self.display_surface)  # Usa o método draw do groupsingle para desenhar o inimigo na superfície display_surface.

#----------------------------------------------------------#

        # Sprites das Classes.
        self.player.draw(self.display_surface)   # Usa o método draw do groupsingle para desenhar o personagem na superfície display_surface.
        self.enemies.draw(self.display_surface)  # Usa o método draw do group  para desenhar o inimigo na superfície display_surface.

#----------------------------------------------------------#

        # Métodos de Colisão.
        self.horizontal_movement_collision()  # Usa o método horizontal_movement_collision para verificar colisões horizontais.
        self.vertical_movement_collision()    # Usa o método horizontal_movement_collision para verificar colisões verticais.

#----------------------------------------------------------#

        # Método dos Projéteis.
        if current_level == 5:                      # Se o level for o 5...
            self.blastattack(self.display_surface)  # Ativa o método Blastattack.

#----------------------------------------------------------#

        if self.health <= 0:              # Se o pv do jogador for menor do que zero...
            self.game_state = "gameover"  # Muda o estado do jogo para game over.

        if self.game_state == "gameover":                       # Se o estado do jogo for game over...
            self.display_surface.blit(self.finaldeath, (0, 0))  # Desenha a tela referente ao game over.
            current_level = 6                                   # Altera esta variável para não interromper a prioridade da tela que estiver rodando.
            self.gameover()                                     # Chama o método de game over.

        if self.healthboss <= 0:        # Se o pv do boss for igual ou menor do que zero...
            self.game_state = "ending"  # O estado do jogo muda para encerramento.

        if self.game_state == "ending":                 # Se o estado do jogo for de encerramento...
            self.display_surface.blit(self.end, (0, 0)) # Desenha a tela de encerramento.      
            current_level = 7                           # Muda a fase.
            self.ending()                               # Chama o método de encerramento.

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
