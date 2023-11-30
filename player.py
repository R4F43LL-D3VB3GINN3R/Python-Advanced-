#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

import pygame 
from support import import_folder

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Classe 'Player' herda pygame.sprite.Sprite...                                                                          
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# A Classe Player representa um jogador no seu jogo.                                                                     
# Ele possui uma representação visual (superfície) na forma de um retângulo vermelho.                                  
# e tem um retângulo associado (self.rect) que é usado para posicionar o jogador na tela e para interações de colisão.   
# A classe também inclui uma nova propriedade chamada 'direction', um vetor bidimensional usando pygame.math.Vector2,    
# que representa a direção atual do jogador no plano (x, y).
# 
# Além disso, foi adicionado o método 'get_input', que obtém as entradas do teclado e atualiza a direção do jogador
# com base nessas entradas. A coordenada x da propriedade 'direction' é ajustada para 1 se a tecla direcional para a 
# direita estiver pressionada, -1 se a tecla direcional para a esquerda estiver pressionada, ou 0 se nenhuma tecla 
# direcional estiver pressionada.
# O jogador também possui métodos 'apply_gravity' e 'jump' para lidar com a força da gravidade e saltos, respectivamente.
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class Player(pygame.sprite.Sprite):

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def __init__(self, pos):  # Este é o método construtor da classe Player, que é chamado automaticamente quando uma nova instância (objeto) da classe é criada. 
                              # Ele recebe um parâmetro pos, que representa a posição inicial do jogador.
        #Setup do Jogador.
        super().__init__()                                      # Chama o construtor da Classe Base.
        self.import_character_assets()                          # Este método é definido dentro da classe Player e é responsável por carregar as animações do jogador a partir de arquivos de imagem.
        self.frame_index = 0                                    # frame_index é o valor do index que irá percorrer dentro do dicionário de cada animacão (self.animations). 
        self.animation_speed = 0.15                             # Define a velocidade em que os sprites se transformam.
        self.image = self.animations['idle'][self.frame_index]  # Define o sprite como 'Idle'. 
        self.rect = self.image.get_rect(topleft = pos)          # Obtém um retângulo associado à superfície do jogador na posicão do canto superior esquerdo.
        self.scale_factor = 1.5                                   # AUMENTAR O TAMANHO DO SPRITE... 

#------------------------------------------------------#

        #Movimentacão do Jogador. 
        self.direction = pygame.math.Vector2(0,0)   # Cria um vetor bidimensional para representar a direção do jogador no plano (x, y)
        self.speed = 3                              # Recebe a Velocidade do Jogador.
        self.gravity = 0.7                          # Recebe a forca da gravidade.
        self.jump_speed = -20                       # Recebe a velocidade do salto.
        self.cooldown = 0                           # Recebe o cooldown do jogador após movimento. 
        self.cooldown_attack = 0                    # Recebe o cooldown do ataque do jogador.
        self.attack_speed = 0.42                    # Recebe a velocidade de ataque. 
        self.blow = False                           # Recebe o ato de golpear.

#------------------------------------------------------#

        #Status do Jogador. 
        self.status = 'idle'      # Define o status default do jogador como idle. 
        self.facing_right = True  # Define o status defaut do jogador como virado para o lado direit

        self.on_ground = False    # Define o status de tocar no chão. 
        self.on_ceiling = False   # Define o status de estar no ar. 
        self.on_left = False      # Define o status de estar do lado esquerdo. 
        self.on_right = False     # Define o status de estar do lado direito.
                                  # Estas verificacões de Status servem para alinhar o sprite ao solo devidamente. 

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Para animar o jogador é preciso saber o status do jogador.
# Se ele estiver: pulando, correndo, caindo, parado, tocando a parede (para cada direcão)e etc... 
# Todas estas informacões nós precisamos obter da interacão entre o jogador e o cenário. 
# Para animar o jogador tem de se trabalhar com várias imagens.
# Também guardando-as de forma organizada e bem definida.
# Todas as animacões são armazenadas dentro de um dicionário.

    def import_character_assets(self): # O método import_character_assets é responsável por carregar as animações do jogador a partir de arquivos de imagem.

        character_path = './graphics/character/'  # Define o caminho para a pasta que contém os recursos gráficos do personagem
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[], 'attack1':[], 'hurt':[]} # Um dicionário que será preenchido com listas de imagens para diferentes animações do jogador.

        for animation in self.animations.keys():                  # Itera sobre as chaves do dicionário (os estados de animação).
            full_path = character_path + animation                # Concatena o caminho do personagem (character_path) com o estado atual de animação (animation).
            self.animations[animation] = import_folder(full_path) # Chama a função import_folder definida em support.py para importar todas as imagens da pasta específica.

    def animate(self):  # O método animate atualiza o sprite do jogador para a próxima imagem na sequência de animação.

        animation = self.animations[self.status]  # A variável animation é atribuída à lista de imagens associadas ao status atual do método get_status. 
        self.frame_index += self.animation_speed  # A variável self.frame_index é incrementada pela velocidade de animação (self.animation_speed).

        if self.frame_index >= len(animation):  # Se o índice atual (self.frame_index) ultrapassou ou é igual ao comprimento da lista de imagens da animação. 
            self.frame_index = 0                # O índice recebe o valor de zero para voltar a revisitar os frames.

        image = animation[int(self.frame_index)] # A variável image do jogador recebe a imagem correspondente ao índice atual da animação.

        if self.facing_right:   # Se o jogador estiver olhando para a direita...           
            self.image = pygame.transform.scale(image, (int(image.get_width() * self.scale_factor), int(image.get_height() * self.scale_factor)))
        else:                   # Se o jogador estiver olhando para a esquerda...
            flipped_image = pygame.transform.flip(image, True, False) # flipped_image recebe a imagem invertida do lado horizontal. 
            self.image = pygame.transform.scale(flipped_image, (int(flipped_image.get_width() * self.scale_factor), int(flipped_image.get_height() * self.scale_factor)))  # self.image recebe a variável com a imagem flipada e escalada.

            # Uma nova variável é criada e recebe o método flip do pygame... 
            # O método recebe a imagem como argumento e o True é referente ao X... 
            # Enquanto o False é referente ao Y... 
            # Significando que ele apenas vai virar da esquerda para direita.

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# DEFEITO DE COLISOES COM BLOCOS NAO RESOLVIDO. 
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        if self.on_ground and self.on_right:                                      # Se o jogador está tocando o chão e do lado esquerdo...
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)  # Obtém um novo retângulo associado à imagem do jogador (self.image) com o ponto inferior direito alinhado ao ponto inferior direito do retângulo original (self.rect.bottomright).
        elif self.on_ground and self.on_left:                                     # Se o jogador está tocando o chão e do lado direito...
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)    # Obtém um novo retângulo associado à imagem do jogador (self.image) com o ponto inferior esquerdo alinhado ao ponto inferior esquerdo do retângulo original (self.rect.bottomleft).
        elif self.on_ground:                                                      # Se o jogador está tocando o chão...
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)      # Obtém um novo retângulo associado à imagem do jogador (self.image) com o ponto inferior do meio alinhado ao ponto inferior do meio do retângulo original (self.rect.midbottom).
        elif self.on_ceiling and self.on_right:                                   # Se o jogador está tocando o teto virado a direita...
            self.rect = self.image.get_rect(topright = self.rect.topright)        # Obtém um novo retângulo associado à imagem do jogador (self.image) com o ponto superior direito (topright) alinhado ao ponto superior direito do retângulo original (self.rect.topright).
        elif self.on_ceiling and self.on_left:                                    # Se o jogador está tocando o teto virado a esquerda...
            self.rect = self.image.get_rect(topleft = self.rect.topleft)          # Obtém um novo retângulo associado à imagem do jogador (self.image) com o ponto superior esquerdo (topleft) alinhado ao ponto superior esquerdo do retângulo original (self.rect.topleft).
        elif self.on_ceiling:                                                     # Se não está tocando o teto...
            self.rect = self.image.get_rect(midtop = self.rect.midtop)            # Obtém um novo retângulo associado à imagem do jogador (self.image) com o ponto superior do meio (midtop) alinhado ao ponto superior do meio do retângulo original (self.rect.midtop).
                                                                                  # self.image.get_rect(center = self.rect.center): Obtém um novo retângulo associado à imagem do jogador (self.image) com o centro (center) alinhado ao centro do retângulo original (self.rect.center).

        # Mudando a posicão do retângulo conforme o jogador colide com o teto ou chão... 
        # Alinha o sprite com a superfície de forma que uma imagem não se sobreponha a outra. 

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def get_input(self):                # Este método é responsável por obter as entradas do teclado e ajustar a direção do jogador com base nessas entradas.

        keys = pygame.key.get_pressed() # Obtém uma lista de teclas pressionadas no momento.

        if keys[pygame.K_d]:            # Se a tecla direcional para a direita estiver pressionada...
            self.direction.x = 1        # A coordenada x da direção do jogador é definida como 1.
            self.facing_right = True    # O jogador estará olhando para a direita.
        elif keys[pygame.K_a]:          # Se a tecla direcional para a esquerda estiver pressionada...
            self.direction.x = -1       # A coordenada x da direção do jogador é definida como -1.
            self.facing_right = False   # O jogador estará olhando para a esquerda. 
        else:                           # Se nenhuma tecla direcional estiver pressionada...
            self.direction.x = 0        # A coordenada x da direção do jogador é definida como 0.

        if self.cooldown == 0:                      # Se o cooldown for zero... 
            if keys[pygame.K_w] and self.on_ground: # Se a tecla direcional para a cima estiver pressionada...
                self.cooldown = 33                  # Altera o valor do cooldown.
                self.jump()                         # O método jump é chamado.

        if self.cooldown > 0:                       # Se o cooldown for maior que zero...
            self.cooldown = self.cooldown - 1       # Decrementa o Cooldown. 

        if self.cooldown_attack == 0:                           # Se o cooldown de ataque for default... 
            if keys[pygame.K_e]:                                # E se a tecla for pressionada... 
                self.animation_speed = self.attack_speed        # A velocidade de animacão recebe a velocidade do ataque. 
                self.status = 'attack1'                         # O status é alterado para atacar e animar os sprites. 
                self.cooldown_attack = self.cooldown_attack + 1 # E o cooldown de ataque é incrementado para fluir os sprites. 

        if self.cooldown_attack > 0:                            # Se o cooldown de ataque for maior do que zero...
                self.cooldown_attack = self.cooldown_attack - 1 # O cooldown de ataque comeca a decrementar. 
                self.animation_speed = 0.15                     # E a velocidade de animacão recebe o valor default. 
                self.blow = True                                # O jogador estará golpeando.

        if self.status != 'attack1': # Se o status do jogador for diferente do de ataque...
            self.blow = False        # Ele não estará golpeando e pode ser golpeado. 

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def get_status(self):              # Este método é responsável por verificar a condicão do jogador. 
                                                
        if self.direction.y < 0:       # Se a direcão do vetor y do jogador for menor do que zero...
            self.status = 'jump'       # O jogador estará pulando.
        if self.direction.y > 1:       # Se a direcão do vetor y do jogador for maior do que 1...
            self.status = 'fall'       # O jogador está caindo.
        else:                          # Sendo nenhum dos casos...
            if self.direction.x != 0:  # Se a direcão do vetor x do jogador for diferente de zero...
                self.status = 'run'    # O jogador está correndo.
            else:                      # # Sendo zero...
                self.status = 'idle'   # O jogador estará parado.

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def apply_gravity(self):               # Este método aplica a forca da gravidade. 

        self.direction.y += self.gravity   # A coordenada y da direção do jogador recebe o incremento da forca da gravidade.
        self.rect.y += self.direction.y    # O retângulo do jogador é pressionado pelo incremento da posicão y do vetor.

    def jump(self):                        # Este método aplica a forca do salto no vetor y. 

        self.direction.y = self.jump_speed # A coordenada y da direção do jogador recebe a velocidade do salto.

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def update(self):                                  # Este método é responsável por atualizar o jogador nos eventos.

        self.get_input()                               # Chama o Método get_input da própria Classe...
        self.animate()                                 # Chama o Método animate da própria Classe.
        self.get_status()                              # Chama o Método get_status da própria Classe.

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#