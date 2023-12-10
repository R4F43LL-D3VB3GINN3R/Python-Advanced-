#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

import pygame 
from support import import_folder

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Classe 'Player' herda pygame.sprite.Sprite...                                                                          
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# A Classe Player representa um inimigo no seu jogo.                                                                     
# Ele possui uma representação visual (superfície) na forma de um retângulo vermelho                                     
# e tem um retângulo associado (self.rect) que é usado para posicionar o inimigo na tela e para interações de colisão.   
# A classe também inclui uma nova propriedade chamada 'direction', um vetor bidimensional usando pygame.math.Vector2,    
# que representa a direção atual do inimigo no plano (x, y).
# O inimigo também possui métodos 'apply_gravity' e 'jump' para lidar com a força da gravidade e saltos, respectivamente.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class Hellhound(pygame.sprite.Sprite):
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def __init__(self, pos):  # Este é o método construtor da classe Enemies, que é chamado automaticamente quando uma nova instância (objeto) da classe é criada. 
                              # Ele recebe um parâmetro pos, que representa a posição inicial do inimigo.
        #Setup do inimigo.
        super().__init__()                                      # Chama o construtor da Classe Base, no caso sprite.Sprite, antes de chamar os objetos da Classe Enemies.
        self.import_character_assets()                          # Este método é definido dentro da classe Enemies e é responsável por carregar as animações do inimigo a partir de arquivos de imagem.
        self.frame_index = 0                                    # frame_index é o valor do index que irá percorrer dentro do dicionário de cada animacão (self.animations). 
        self.animation_speed = 0.10                             # Define a velocidade em que os sprites se transformam.
        self.image = self.animations['run'][self.frame_index]   # self.image recebe self.animations que é um dicionário declarado dentro do método import_character_assets().
        self.rect = self.image.get_rect(topleft = pos)          # Obtém um retângulo associado à superfície da imagem na posicão do canto superior esquerdo.
        self.scale_factor = 1.9                                 # Tamanho do sprite. 

#------------------------------------------------------#

        #Movimentacão do inimigo. 
        self.direction = pygame.math.Vector2(0,0)   # Cria um vetor bidimensional para representar a direção do inimigo no plano (x, y)
        self.speed = 0.5                            # Recebe a Velocidade do inimigo.
        self.gravity = 1                            # Recebe a forca da gravidade.
        self.jump_speed = -14                       # Recebe a distancia do salto.
        self.cooldown = 0                           # Recebe o cooldown do inimigo após movimento. 
        self.cooldown_attack = 0                    # Recebe o cooldown do inimigo após ataque.
        self.attack_speed = 0.42                    # Recebe a velocidade de ataque. 
        self.skullmovel = 300                       # Recebe a distância que percorre na direcão esquerda.                       
        self.skullmover = 300                       # Recebe a distância que percorre na direcão direita.                                 

#------------------------------------------------------#

        #Status do inimigo. 
        self.status = 'run'       # Define o status default do inimigo como idle. 
        self.facing_right = True  # Define o status defaut do inimigo como virado para o lado direito

        self.on_ground = False    # Define o status de tocar no chão. 
        self.on_ceiling = False   # Define o status de estar no ar. 
        self.on_left = False      # Define o status de estar do lado esquerdo. 
        self.on_right = False     # Define o status de estar do lado direito.

        # Estas verificacões de Status servem para alinhar o sprite ao solo devidamente. 

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Para animar o inimigo é preciso saber o status do inimigo.
# Se ele estiver: pulando, correndo, caindo, parado, tocando a parede (para cada direcão) e etc... 
# Todas estas informacões nós precisamos obter da interacão entre o inimigo e o cenário. 
# Para animar o inimigo tem de se trabalhar com várias imagens.
# Também guardando-as de forma organizada e bem definida.
# Todas as animacões são armazenadas dentro de um dicionário.

    def import_character_assets(self):  # O método import_character_assets é responsável por carregar as animações do inimigo a partir de arquivos de imagem.

        character_path = './graphics/enemies/hellhound/'  # Define o caminho para a pasta que contém os recursos gráficos do personagem
        self.animations = {'run':[]}                      # Um dicionário que será preenchido com listas de imagens para diferentes animações do inimigo.

        for animation in self.animations.keys():                   # Itera sobre as chaves do dicionário (os estados de animação).
            full_path = character_path + animation                 # Concatena o diretório com o nome do arquivo que encontrar dentro da pasta.
            self.animations[animation] = import_folder(full_path)  # Chama a função import_folder definida em support.py para importar todas as imagens da pasta específica 

    def animate(self):  # O método animate atualiza o sprite do inimigo para a próxima imagem na sequência de animação.

        animation = self.animations[self.status]  # A variável animation é atribuída à lista de imagens associadas ao status atual do método get_status. 
        self.frame_index += self.animation_speed  # A variável self.frame_index é incrementada pela velocidade de animação (self.animation_speed).

        if self.frame_index >= len(animation): # Se o índice atual (self.frame_index) ultrapassou ou é igual ao comprimento da lista de imagens da animação. 
            self.frame_index = 0               # O índice recebe o valor de zero para voltar a revisitar os frames do comeco.

        image = animation[int(self.frame_index)]  # A variável image do inimigo recebe a imagem correspondente ao índice atual da animação.

        if self.facing_right:  # Se o inimigo estiver olhando para a direita...        
                
             flipped_image = pygame.transform.flip(image, True, False)  # Se o inimigo estiver olhando para a esquerda, flipped_image recebe a imagem invertida do lado horizontal. 
             self.image = pygame.transform.scale(flipped_image, (int(flipped_image.get_width() * self.scale_factor), int(flipped_image.get_height() * self.scale_factor)))  # self.image recebe a variável com a imagem flipada e escalada.
        else:  # Se o inimigo estiver olhando para a esquerda...                                                                        
            self.image = pygame.transform.scale(image, (int(image.get_width() * self.scale_factor), int(image.get_height() * self.scale_factor)))  # A propriedade self.image do inimigo recebe image.
            # Uma nova variável é criada e recebe o método flip do pygame... 
            # O método recebe a imagem como argumento e o True é referente ao X... 
            # Enquanto o False é referente ao Y... 
            # Significando que ele apenas vai virar da esquerda para direita.

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# DEFEITO DE COLISOES COM BLOCOS NAO RESOLVIDO. 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

        if self.on_ground and self.on_right:                                      # Se o inimigo está tocando o chão e do lado esquerdo...
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)  # Obtém um novo retângulo associado à imagem do inimigo (self.image) com o ponto inferior direito alinhado ao ponto inferior direito do retângulo original (self.rect.bottomright).
        elif self.on_ground and self.on_left:                                     # Se o inimigo está tocando o chão e do lado direito...
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)    # Obtém um novo retângulo associado à imagem do inimigo (self.image) com o ponto inferior esquerdo alinhado ao ponto inferior esquerdo do retângulo original (self.rect.bottomleft).
        elif self.on_ground:                                                      # Se o inimigo está tocando o chão...
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)      # Obtém um novo retângulo associado à imagem do inimigo (self.image) com o ponto inferior do meio alinhado ao ponto inferior do meio do retângulo original (self.rect.midbottom).
        elif self.on_ceiling and self.on_right:                                   # Se o inimigo está tocando o teto virado a direita...
            self.rect = self.image.get_rect(topright = self.rect.topright)        # Obtém um novo retângulo associado à imagem do inimigo (self.image) com o ponto superior direito (topright) alinhado ao ponto superior direito do retângulo original (self.rect.topright).
        elif self.on_ceiling and self.on_left:                                    # Se o inimigo está tocando o teto virado a esquerda...
            self.rect = self.image.get_rect(topleft = self.rect.topleft)          # Obtém um novo retângulo associado à imagem do inimigo (self.image) com o ponto superior esquerdo (topleft) alinhado ao ponto superior esquerdo do retângulo original (self.rect.topleft).
        elif self.on_ceiling:                                                     # Se não está tocando o teto...
            self.rect = self.image.get_rect(midtop = self.rect.midtop)            # Obtém um novo retângulo associado à imagem do inimigo (self.image) com o ponto superior do meio (midtop) alinhado ao ponto superior do meio do retângulo original (self.rect.midtop).
                                                                                  # self.image.get_rect(center = self.rect.center): Obtém um novo retângulo associado à imagem do inimigo (self.image) com o centro (center) alinhado ao centro do retângulo original (self.rect.center).

        # Mudando a posicão do retângulo conforme o inimigo colide com o teto ou chão... 
        # Alinha o sprite com a superfície de forma que uma imagem não se sobreponha a outra. 

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def get_status(self):              # Este método é responsável por verificar a condicão do inimigo. 

        if self.direction.y < 0:       # Se a direcão do vetor y do inimigo for menor do que zero...
            self.status = 'run'        # O inimigo estará pulando.
        if self.direction.y > 1:       # Se a direcão do vetor y do inimigo for maior do que 1...
            self.status = 'run'        # O estará agindo normal...
        else:                          # Sendo nenhum dos casos...
            if self.direction.x != 0:  # Se a direcão do vetor x do inimigo for diferente de zero...
                self.status = 'run'    # O inimigo está correndo.
            else:                      # Sendo zero...
                self.status = 'run'    # O inimigo estará parado.

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def apply_gravity(self):  # Este método aplica a forca da gravidade. 
  
        self.direction.y += self.gravity  # A coordenada y da direção do inimigo recebe o incremento da forca da gravidade puxando-o para baixo.
        self.rect.y += self.direction.y   # O retângulo do inimigo é pressionado pelo incremento da posicão y do vetor puxando-o para baixo.

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
            
    def move(self): # Método para definir os movimentos dos inimigos.

        # Movimento do Esqueleto (Esquerda-Direita)

        if self.skullmovel > 0:                                             # Se a variável for maior que zero...
            self.skullmovel -= 4                                            # Decrementa 1 da variável iniciada como 25.
            self.direction.x = 4                                            # Direcão x recebe 1 (direita).
            self.rect.x += self.direction.x                                 # O retângulo do inimigo é incrementado com 1.
        elif self.skullmover > 0:                                           # Se a variável for maior que zero...
            self.skullmover -= 4                                            # Decrementa 1 da vriável iniciada como 25.
            self.direction.x = -4                                           # A direcão x recebe -1 (esquerda)
            self.rect.x += self.direction.x                                 # O retângulo do inimigo é incrementado com -1
            flipped_skull = pygame.transform.flip(self.image, True, False)  # Variável local recebe o flip da imagem. 
            self.image = flipped_skull                                      # A imagem recebe a variável local com o flip da imagem.

        if self.skullmovel == 0 and self.skullmover == 0:                   # Se as duas variáveis forem decrementadas até 0...
            self.skullmovel = 300                                           # Elas recebem o valor original para que o código funcione como um ciclo. 
            self.skullmover = 300 

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def update(self): # Este método é responsável por atualizar o inimigo nos eventos.

        self.animate()    
        self.get_status() 
        self.move()                                 
      
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
