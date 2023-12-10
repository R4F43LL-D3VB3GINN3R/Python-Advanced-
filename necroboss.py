#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

from enemies import Enemies 
from support import import_folder
import pygame
import random 
from settings import *

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class Necroboss(Enemies): # Classe Necroboss herda a Classe Enemies.
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def __init__(self, pos):  # Este é o método construtor da classe Necroboss, que é chamado automaticamente quando uma nova instância (objeto) da classe é criada. 
                              # Ele recebe um parâmetro pos, que representa a posição inicial do inimigo.
        # Setup do inimigo.
        super().__init__(pos)                                   # Chama o construtor da Classe Base.
        self.import_character_assets()                          # Este método é definido dentro da classe Enemies e é responsável por carregar as animações do inimigo a partir de arquivos de imagem.
        self.frame_index = 0                                    # frame_index é o valor do index que irá percorrer dentro do dicionário de cada animacão (self.animations). 
        self.animation_speed = 0.15                             # Define a velocidade em que os sprites se transformam.
        self.image = self.animations['idle'][self.frame_index]  # Define o sprite como 'Idle'. 
        self.rect = self.image.get_rect(topleft = pos)          # Obtém um retângulo associado à superfície do inimigo na posicão do canto superior esquerdo.
        self.scale_factor = 3                                   # AUMENTAR O TAMANHO DO SPRITE... 
        self.random_value = random.randint(1, 50)               # Valor randomico para guardar a possibilidade de local de teletransporte.

#------------------------------------------------------#

        # Movimentacão do inimigo. 
        self.direction = pygame.math.Vector2(0,0)   # Cria um vetor bidimensional para representar a direção do inimigo no plano (x, y)

#------------------------------------------------------#

        #Status do inimigo. 
        self.status = 'idle' # Define o status default do inimigo como idle. 

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Para animar o inimigo é preciso saber o status do inimigo.
# Se ele estiver: pulando, correndo, caindo, parado, tocando a parede (para cada direcão)e etc... 
# Todas estas informacões nós precisamos obter da interacão entre o inimigo e o cenário. 
# Para animar o inimigo tem de se trabalhar com várias imagens.
# Também guardando-as de forma organizada e bem definida.
# Todas as animacões são armazenadas dentro de um dicionário.

    def import_character_assets(self): # O método import_character_assets é responsável por carregar as animações do inimigo a partir de arquivos de imagem.

        character_path = './graphics/enemies/necromancer/'                           # Define o caminho para a pasta que contém os recursos gráficos do personagem
        self.animations = {'idle':[], 'hurt':[], 'teleport':[]}                      # Um dicionário que será preenchido com listas de imagens para diferentes animações do inimigo.

        for animation in self.animations.keys():                                     # Itera sobre as chaves do dicionário (os estados de animação).
            full_path = character_path + animation                                   # Concatena o caminho do personagem (character_path) com o estado atual de animação (animation)
            self.animations[animation] = import_folder(full_path)                    # Chama a função import_folder definida em support.py para importar todas as imagens da pasta específica 
    
    def animate(self):                                                               # O método animate atualiza o sprite do inimigo para a próxima imagem na sequência de animação.

        animation = self.animations[self.status]                                     # A variável animation é atribuída à lista de imagens associadas ao status atual do método get_status. 
        self.frame_index += self.animation_speed                                     # A variável self.frame_index é incrementada pela velocidade de animação (self.animation_speed).

        if self.frame_index >= len(animation):                                       # Se o índice atual (self.frame_index) ultrapassou ou é igual ao comprimento da lista de imagens da animação. 
            self.frame_index = 0                                                     # O índice recebe o valor de zero para voltar a revisitar os frames.

        image = animation[int(self.frame_index)]                                     # A variável image do inimigo recebe a imagem correspondente ao índice atual da animação.

        if self.facing_right:                                                        # Se o inimigo estiver olhando para a direita...           
             self.image = pygame.transform.scale(image, (int(image.get_width() * self.scale_factor), int(image.get_height() * self.scale_factor)))   
        else:                                                                        # Se o inimigo estiver olhando para a esquerda...
            flipped_image = pygame.transform.flip(image, True, False)                # flipped_image recebe a imagem invertida do lado horizontal. 
            self.image = pygame.transform.scale(flipped_image, (int(flipped_image.get_width() * self.scale_factor), int(flipped_image.get_height() * self.scale_factor)))  # self.image recebe a variável com a imagem flipada e escalada.

            # Uma nova variável é criada e recebe o método flip do pygame... 
            # O método recebe a imagem como argumento e o True é referente ao X... 
            # Enquanto o False é referente ao Y... 
            # Significando que ele apenas vai virar da esquerda para direita.

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def special_moves(self): # Este método guarda os métodos de ataques especiais do boss.

        def teleport(): # Método de teletransporte.
 
            new_x = random.randint(0, screen_width - self.rect.width)  # Recebe o valor aleatório da linha.
            new_y = random.randint(0, 250)                             # Recebe o valor aleatório da altura.
            self.rect.topleft = (new_x, new_y)                         # O retângulo recebe a nova posicão.                                                   

        if self.random_value > 1:  # Se o valor randômico for maior do que um...
            for _ in range(1):     # Itera 5 vezes na variável qualquer.
                teleport()         # Reproduz o teletransporte.

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def get_status(self, status):  # Este método é responsável por verificar a condicão do jogador. 
                                                
        self.status = status # Recebe a condicão do jogador.

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    def update(self): # Este método é responsável por atualizar o inimigo nos eventos.

        self.animate()                                 

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
