import pygame, time
from sys import exit
from classes import *
from random import choice
from settings import *
import warnings
warnings.filterwarnings("ignore")

class Game:
    """
    Breakout Game

    This class represents the Breakout game. It manages the game loop, handles events,
    updates game objects, and renders the game screen.

    Attributes:
        screen (pygame.Surface): The game screen surface.
        clock (pygame.time.Clock): The game clock for controlling the frame rate.
        all_sprites (pygame.sprite.Group): A sprite group containing all game sprites.
        blocks (pygame.sprite.Group): A sprite group containing the blocks in the game.
        upgrades (pygame.sprite.Group): A sprite group containing the upgrades in the game.
        can_shoot (bool): Laser shooting indication.
        block_grp (pygame.sprite.Group) = A sprite group containing the blocks in the game.
        player (pygame.sprite.GroupSingle) = A sprite groupsingle containing player sprite.
        ball_sprite (Ball) = Ball object.
        ball (pygame.sprite.GroupSingle) = A sprite groupsingle containing ball sprite.
        heart_surf (pygame.Surface) = Image of heart.
        upgrade_sprites (pygame.sprite.Group) = Sprite group containing upgrade sprites.
        game_over (bool) = Flag indicating if the game is over.
        font (pygame.font.SysFont) = Font type.
        game_over_text (pygame.Surface) = Game Over text.
        text_rect (pygame.Rect) = Rectangle for Game Over text.

    Methods:
        __init__(self): Initializes the Game object.
        game_over_display(self): Display game over text.
        create_upgrade(self, pos, up_type): create upgrade sprites.
        upgrade_collide(self): updating the game for upgrade collision with player.
        block_setup(self): Display blocks on the screen.
        display_hearts(self): Display hearts on the screen.
        run(self): Runs the game loop.
    """
    def __init__(self): 
        """
        Initialize the Game object.

        Creates the game window, sets up game objects, and initializes flags.
        """
        pygame.init()
        pygame.display.set_caption('Breakout')

        self.screen = pygame.display.set_mode((Width, Height))
        
        self.can_shoot = True

        #Block sprite
        self.block_grp = pygame.sprite.Group()
        self.blocks_setup()

        #Player sprite
        self.player = pygame.sprite.GroupSingle(Player((Width/2, Height - 50), self.block_grp, speed=5 ))
 
        #Ball Sprite
        self.ball_sprite = Ball((Width/2,Height-80), self.player.sprite, self.block_grp, vel= [2,-2])
        self.ball = pygame.sprite.GroupSingle(self.ball_sprite) 

        #Heart display
        self.heart_surf = pygame.image.load('PNG/60-Breakout-Tiles.png').convert_alpha()
        self.heart_surf = pygame.transform.rotozoom(self.heart_surf, 0, Heart_Scale).convert_alpha()

        #Upgrade sprite
        self.upgrade_sprites = pygame.sprite.Group()

        #Game over setup
        self.game_over = False
        self.font = pygame.font.SysFont(None, 48)
        self.game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        self.text_rect = self.game_over_text.get_rect(center=(Width // 2, Height // 2))
        
        #Winner Text
        self.winner_text = self.font.render('Winner', True, (0,255,0))
        self.winner_text_rect = self.winner_text.get_rect(center=(Width // 2, Height // 2))
    
    def game_over_display(self):
        """Display game over text."""
        self.screen.blit(self.game_over_text, self.text_rect)
       
    def Winner(self):
        """Display Winner text."""
        self.screen.blit(self.winner_text, self.winner_text_rect)
      
    def create_upgrade(self, pos, up_type):
        """Upgrade player."""
        Upgrade(pos, up_type, self.upgrade_sprites)

    def upgrade_collide(self):
        """Updating the game for upgrade collision with player."""
        overlap_sprite = pygame.sprite.spritecollide(self.player.sprite, self.upgrade_sprites, True)
        for sprite in overlap_sprite:
            self.player.sprite.upgrade(sprite.up_type)

    def blocks_setup(self):
        """Display blocks on the screen."""
        for row_index, row in enumerate(Shape):
            for col_index, col in enumerate(row):
                pos_x = col_index * (Block_Size[0] + Block_Offset)
                pos_y = Top_Offset + row_index * (Block_Size[1] + Block_Offset)
                Block(col, pos_x, pos_y, self.block_grp, self.create_upgrade)

    def display_hearts(self):
        """Display hearts on the screen."""
        heart_width = self.heart_surf.get_width()
        for i in range(self.player.sprite.hearts):
            self.screen.blit(self.heart_surf, ( i * (heart_width + 2) + 5, 5 ))

    def run(self):
        """Update all the game sprites"""

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
        
        #Laser Update
        if self.ball.sprite.active:
            self.player.sprite.laser_update()

        #Ball Setup
        self.ball.update()
        self.ball.draw(self.screen)

        #Lasers
        self.player.sprite.lasers_grp.draw(self.screen)
        

if __name__ == '__main__':
    
    game = Game()

    clock = pygame.time.Clock()
    
    #Background_img
    bg_img = pygame.image.load('PNG/bg_image.png').convert_alpha()
    # game loop
    while True:
        #game.screen.fill((51, 51, 51))
        game.screen.blit(bg_img, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.ball.sprite.active = True
        
        if game.player.sprite.hearts == 0:
            game.game_over_display()
        
        elif len(game.block_grp) == 0:    
            game.Winner()

        else:
            game.run()

        pygame.display.update()
        clock.tick(60)      
    game.game_over_display()

   
