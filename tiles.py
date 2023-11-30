#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

import pygame 

#--------------------------------------------------------------------------------------------------------------------------------------------#
# Classe 'Tile' herda pygame.sprite.Sprite... 
#--------------------------------------------------------------------------------------------------------------------------------------------#
# A Classe Tile representa um bloco no jogo. 
# Ela herda da classe pygame.sprite.Sprite, indicando que é um sprite manipulável no Pygame.
# Cada bloco tem uma superfície (onde desenhamos a aparência do bloco),
# uma posição (onde colocamos o bloco no jogo), e
# um retângulo associado (que ajuda a posicionar e detectar colisões).
# 
# O método __init__ é chamado automaticamente ao criar uma nova instância.
# Ele inicializa a classe base, cria uma superfície retangular preenchida com a cor branca e obtém um retângulo associado à superfície.
# 
# O método update é usado para controlar o deslocamento horizontal do mundo (ou nível).
# O deslocamento horizontal (x_shift) é passado para o método update de cada bloco no grupo self.tiles.
# O método update de cada bloco ajusta a posição horizontal do bloco com base no deslocamento do mundo.
# Isso é comum em jogos side-scrolling para criar a ilusão de movimento ao mover a câmera pelo mundo do jogo.
#---------------------------------------------------------------------------------------------------------------------------------------------#

class Tile(pygame.sprite.Sprite):      
                    
    def __init__(self, pos, size):                      # O método __init__ é chamado automaticamente quando uma nova instância é criada. 

        super().__init__()                              # Garante que a inicializacão da Classe base seja realizada antes da inicializacão específica da Classe Tile. 
        brick_size = size - 2
        border_size = 2
        self.image = pygame.Surface((size,size))        # Cria uma superfície retangular com as dimensões de 'size'. Ambos sendo Altura e Largura. 
        self.image.fill((128, 0, 128))                      # Preenche a superfície com a cor branca.
        self.rect = self.image.get_rect(topleft = pos)  
        brick_surface = pygame.Surface((brick_size, brick_size))
        brick_surface.fill((0, 0, 0))
        self.image.blit(brick_surface, (border_size, border_size))

        # Obtém um retângulo associado a superfície... 
        # O retângulo representa a área ocupada pela imagem... 
        # O Argumento 'topleft = pos' define a posicão no canto superior esquerdo do retângulo com base na posicão 'pos'... 
        # O retângulo é útil para posicionar o bloco na tela e para detecção de colisões.

#---------------------------------------------------------------------------------------------------------------------------------------------#

    def update(self, x_shift,): # O método update é usado para controlar o deslocamento horizontal do mundo (ou nível),...
                                # ...e esse deslocamento é passado para o método update de cada bloco no grupo self.tiles...
                                # ...O método update em cada bloco, por sua vez, ajusta a posição horizontal do bloco com base no deslocamento do mundo. 
                                # ...Essa abordagem é comum em jogos side-scrolling para criar a ilusão de movimento ao mover a câmera pelo mundo do jogo.

        self.rect.x += x_shift  # Aqui, ele está sendo usado para mover horizontalmente o retângulo associado à superfície do bloco (self.rect.x) com base no valor de x_shift.

#---------------------------------------------------------------------------------------------------------------------------------------------#