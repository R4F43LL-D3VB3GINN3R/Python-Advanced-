#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

from os import walk
import pygame

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def import_folder(path): # É uma função que recebe o caminho de uma pasta e retorna uma lista de superfícies (imagens).

    surface_list = []                                                  # Lista que armazenará as superfícies (imagens) importadas.

    for _, __, img_files in walk(path):                                # Usa a função os.walk para percorrer todos os arquivos na pasta especificada por path
        for image in img_files:                                        # Itera sobre os nomes dos arquivos na pasta.
            full_path = path + '/' + image                             # Constrói o caminho completo para cada imagem.
            image_surf = pygame.image.load(full_path).convert_alpha()  # Carrega a imagem usando o Pygame e aplica a conversão alpha para otimização.
            surface_list.append(image_surf)                            # Adiciona a superfície (imagem) à lista.

    return surface_list                                                # Retorna a lista de superfícies (imagens).

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
