#----------------------------------------------------------------------------------------------------------------------#

level_map = [
'                   ', # string 0
'                N  ', # string 1
'                   ', # string 2
'S     S  S  S      ', # string 3
'                   ', # string 4
'                   ', # string 5
'                   ', # string 6
'                   ', # string 7
'                   ', # string 8
'P                  ', # string 9
'XXXXXXXXXXXXXXXXXXX'] # string 10

level_map2 = [
'                   ', # string 0
'                N  ', # string 1
'                   ', # string 2
'   S  S  S  S  S   ', # string 3
'                   ', # string 4
'                   ', # string 5
'                   ', # string 6
'                   ', # string 7
'                   ', # string 8
'P                  ', # string 9
'X XXXXXXXXXXXXXXX X'] # string 10

level_map3 = [
'                   ', # string 0
'                N  ', # string 1
'                   ', # string 2
'      S  S  S  S   ', # string 3
'                   ', # string 4
'                   ', # string 5
'                   ', # string 6
'    XXXXXXXXX      ', # string 7
'   XX              ', # string 8
'P XXX              ', # string 9
'X XXXXXXXXXXXXXXX X'] # string 10

level_map4 = [
'                   ', # string 0
'    S   S  S  S N  ', # string 1
'                   ', # string 2
'      S  S  S  S   ', # string 3
'                   ', # string 4
'    S     S    S   ', # string 5
'                   ', # string 6
'    XXXXXXXXX      ', # string 7
'   XX              ', # string 8
'P XXX              ', # string 9
'X XXXXXXXXXXXXXXX X'] # string 10

level_map5 = [
'                   ', # string 0
'      S   S        ', # string 1
'                   ', # string 2
'                   ', # string 3
'                   ', # string 4
'                   ', # string 5
'        X  X       ', # string 6
'      X      X     ', # string 7
'  B X          X   ', # string 8
'P X              X ', # string 9
'XXX X X X X X X X X'] # string 10

# Cada string na lista representa várias colunas no mapa.
# Cada string na lista representa uma linha no mapa.
# Os espaços em branco e os caracteres X são usados para representar diferentes elementos no mapa.
# Espaços em branco representam áreas vazias ou passáveis.
# X representa paredes ou obstáculos.
# P representa o ponto de partida do personagem. 
# S representa o ponto de partida do esqueleto. 

#----------------------------------------------------------------------------------------------------------------------#

tile_size = 64                             # Define o tamanho de cada bloco do mapa. 
screen_width = 1200                        # Define a largura da tela.
screen_height = len(level_map) * tile_size  

# 'screen_height' recebe o número de elementos da lista 'level_map'...
# Os elementos neste caso são a quantidade de linhas da lista (11)... 
# 'len(level_map) * 'tile_size' = altura da tela... 
# Ou seja, "A altura da tela recebe = Quantidade de Linhas * Tamanho dos Blocos. 

#----------------------------------------------------------------------------------------------------------------------#


