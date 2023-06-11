import pygame, time
from sys import exit
from classes import *
from random import choice
from settings import *
import warnings
warnings.filterwarnings("ignore")

class Game:
    def __init__(self): 

        pygame.init()
        pygame.display.set_caption('Breakout')

        self.screen = pygame.display.set_mode((Width, Height))
        self.can_shoot = True

        #Block sprite
        self.block_grp = pygame.sprite.Group()
        self.blocks_setup()

        #Player sprite
        self.player_sprite = Player((Width/2, Height - 50), self.block_grp, speed=5 )
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
 
        #Ball Sprite
        self.ball_sprite = Ball((Width/2,Height-80), self.player.sprite, self.block_grp, vel= [2,-2])
        self.ball = pygame.sprite.GroupSingle(self.ball_sprite) 

        #Heart display
        self.heart_surf = pygame.image.load('PNG/60-Breakout-Tiles.png').convert_alpha()
        self.heart_surf = pygame.transform.rotozoom(self.heart_surf, 0, Heart_Scale).convert_alpha()

        #Upgrade sprite
        self.upgrade_sprites = pygame.sprite.Group()
    
    def create_upgrade(self, pos, up_type):
        #Upgrading player block
        Upgrade(pos, up_type, self.upgrade_sprites)

    def upgrade_collide(self):
        overlap_sprite = pygame.sprite.spritecollide(self.player.sprite, self.upgrade_sprites, True)
        for sprite in overlap_sprite:
            self.player.sprite.upgrade(sprite.up_type)

    def blocks_setup(self):
        for row_index, row in enumerate(Shape):
            for col_index, col in enumerate(row):
                pos_x = col_index * (Block_Size[0] + Block_Offset)
                pos_y = Top_Offset + row_index * (Block_Size[1] + Block_Offset)
                Block(col, pos_x, pos_y, self.block_grp, self.create_upgrade)

    def display_hearts(self):
        heart_width = self.heart_surf.get_width()
        for i in range(self.player.sprite.hearts):
            self.screen.blit(self.heart_surf, ( i * (heart_width + 2) + 5, 5 ))

    def run(self):
        last_time = time.time()
        clock = pygame.time.Clock()

        while True:
            dt = time.time() - last_time
            last_time = time.time()
            self.screen.fill((51, 51, 51))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.player.sprite.hearts == 0:
                    pygame.quit()
                    exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.sprite.active = True

            #Blocks Setup
            self.block_grp.draw(self.screen)

            #Hearts Setup
            self.display_hearts()

            #Upgrades
            self.upgrade_sprites.update()
            self.upgrade_sprites.draw(self.screen)
            self.upgrade_collide()

            #Player Setup
            self.player.sprite.get_input()
            self.player.update()
            self.player.draw(self.screen)

            #Ball Setup
            self.ball.update()
            self.ball.draw(self.screen)

            #Lasers
            self.player.sprite.lasers_grp.draw(self.screen)

            pygame.display.update()
            clock.tick(60)

if __name__ == '__main__':
    
    game = Game()
    game.run()
    