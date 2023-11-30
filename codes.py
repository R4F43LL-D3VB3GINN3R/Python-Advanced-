# Gravidade aos inimigos. 

for enemy in self.enemies.sprites():                 # Itera sobre todos os sprites de inimigos no grupo de enemies.
    enemy.apply_gravity()                            # Aplica a gravidade aos inimigos.

    for sprite in self.tiles.sprites():              # Itera sobre todos os sprites de blocos no grupo de tiles.
        if sprite.rect.colliderect(enemy.rect):      # Se houver uma colisão entre o inimigo e um Bloco...
            if enemy.direction.y > 0:                # Se o inimigo estiver se movendo para baixo...
                enemy.rect.bottom = sprite.rect.top  # Ajusta a posição do inimigo para a parte superior do bloco.
                enemy.direction.y = 0                # O inimigo não está nem se movendo para cima e nem para baixo. 
                enemy.on_ground = True               # O inimigo está tocando no chão. 
            elif enemy.direction.y < 0:              # Se o inimigo estiver se movendo para cima...
                enemy.rect.top = sprite.rect.bottom  # Ajusta a posição do inimigo para a parte inferior do bloco.
                enemy.direction.y = 0                # O inimigo não está nem se movendo para cima e nem para baixo. 
                enemy.on_ground = True               # O inimigo está tocando no chão. 

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def scroll_x(self):                            # O método scroll_x é chamado para fazer com que a câmera acompanhe o Jogador horizontalmente. 

        player = self.player.sprite                # player recebe o sprite do Jogador. 
        player_x = player.rect.centerx             # player_x recebe a posicão x do centro do retângulo do Jogador. 
        direction_x = player.direction.x           # direction_x recebe a direcão horizontal do Jogador.


        if player_x < screen_width / 4 and direction_x < 0:                     # Se o jogador estiver se movendo para a esquerda e estiver a menos de um quarto da largura da tela da borda esquerda...
            self.world_shift = 3                                                # A mudanca de câmera é definida para 8. 
            player.speed = 0                                                    # A velocidade do Jogador é definida para 0. 
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:  # Se o jogador estiver se movendo para a direita e estiver a menos de um quarto da largura da tela da borda direita...
            self.world_shift = -3                                               # A mudanca de câmera é definida para -8. 
            player.speed = 0                                                    # A velocidade do Jogador é definida para 0. 
        else:                                                                   # Se a posicão x do Jogador estiver entre 200 e 1000... 
            self.world_shift = 0                                                # A mudanca de câmera é definida para 0. 
            player.speed = 3                                                    # A velocidade do Jogador é definida para 8.

            # Em Resumo...a câmera anda com o Jogador quando ele ultrapassa os limites de pixels na tela... 
            # E fica parada quando está entre as definicões dos limites. 
            # Isso passa a ideia de que ele esteja em movimento mesmo parado.  

        self.scroll_x() # Usa o método scroll_x para ajustar a câmera em relacão a direcão do Jogador.