from typing import Any
import pygame
import random
from settings import *

class Player(pygame.sprite.Sprite):
    """A class representing the player character in the game.

    Attributes:
        image (Surface): The image representing the player character.
        rect (Rect): The rectangular area occupied by the player character.
        speed (int): The movement speed of the player character.
        hearts (int): The number of hearts/lives the player has.
        blocks (Group): The group of blocks in the game.
        no_lasers (int): The number of lasers available to the player.
        lasers_grp (Group): The group of lasers fired by the player.
        start_laser (bool): Indicates whether the player can fire lasers.
        laser_time (int): The time when the last laser was fired.
        laser_cooldown (int): The cooldown time between laser shots.
        ready (bool): Indicates whether the player is ready to fire a laser.

    Methods:
        constraint(): Ensures that the player character stays within the game window.
        get_input(): Gets the user input to move the player character.
        upgrade(upgrade_type): Upgrades the player character based on the given upgrade type.
        laser_recharge(): Recharges the laser ability of the player.
        update(): Updates the player character's state and behavior.

    """

    def __init__(self, pos, blocks, speed=5):
        """Initialize the Player object.

        Args:
            pos (tuple): The initial position of the player character (x, y).
            blocks (Group): The group of blocks in the game.
            speed (int, optional): The movement speed of the player character. Defaults to 5.

        """
        super().__init__()

        #sprite setup
        self.image = pygame.image.load('PNG/51-Breakout-Tiles.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, Scale_Fac).convert_alpha()
        self.rect = self.image.get_rect(center = pos)

        self.speed = speed
        self.hearts = 3
        
        #blocks
        self.blocks = blocks

        #lasers setup
        self.no_lasers = 10
        self.lasers_grp = pygame.sprite.Group()
        self.start_laser = False
        self.laser_time = 0
        self.laser_cooldown = 2000
        self.ready = True
 
    def constraint(self):
        """Ensure that the player character stays within the game window."""
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= Width:
            self.rect.right = Width

    def get_input(self):
        """Get the user input to move the player character."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        self.constraint()

    def upgrade(self, upgrade_type):
        """Upgrade the player character based on the given upgrade type.

        Args:
            upgrade_type (str): The type of upgrade to apply.

        """
        if upgrade_type == 'slow':
            self.speed -= 1
        if upgrade_type == 'fast':
            self.speed += 1
        if upgrade_type == 'heart':
            self.hearts += 1
        if upgrade_type == 'laser':
            if self.start_laser:
                self.no_lasers += 10
            else:
                self.start_laser = True

    def laser_recharge(self):
        """Recharge the laser ability of the player."""

        if not self.ready:
            current_time = pygame.time.get_ticks()
            if (current_time - self.laser_time) >= self.laser_cooldown:
                self.ready = True

    def laser_update(self):
        """Update the laser state and behavior."""
        if self.no_lasers > 0:
            self.laser_recharge()

        # Update laser
        if self.start_laser and self.ready:
            self.laser_time = pygame.time.get_ticks()
            L = Laser(self.rect, self.blocks)
            self.lasers_grp.add(L)
            self.ready = False
            self.no_lasers -= 1

            #remove laser if it goes outside window
            for sprite in self.lasers_grp:
                if sprite.rect.y < -100:
                    sprite.kill()

        self.lasers_grp.update()            

class Ball(pygame.sprite.Sprite):
    """A class representing the ball in the game.

    Attributes:
        image (Surface): The image representing the ball.
        rect (Rect): The rectangular area occupied by the ball.
        velocity (list): The velocity of the ball in the (x, y) direction.
        player (Player): The player object representing the paddle.
        blocks (Group): The group of blocks in the game.
        active (Bool): Indicates whether the ball is in motion.

    Methods:
        update(): Updates the ball's position and handles collisions.
        check_paddle_collision(): Checks for collision with the paddle.
        check_block_collision(): Checks for collision with blocks.
        handle_paddle_collision(): Handles collision with the paddle.
        handle_block_collision(block): Handles collision with a block.
        handle_boundaries_collision(): Handles collision with the game boundaries.

    """
    
    def __init__(self, pos, player, blocks, vel = [2, -2]) -> None:
        """Initialize the Ball object.

        Args:
            pos (tuple): The initial position of the ball (x, y).
            player (Player): The player object representing the paddle.
            blocks (Group): The group of blocks in the game.

        """
        super().__init__()
        self.player = player
        self.blocks = blocks

        #sprite setup
        self.image = pygame.image.load('PNG/58-Breakout-Tiles.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.20).convert_alpha()
        self.rect = self.image.get_rect(midbottom = self.player.rect.midtop)

        self.pos = pos
        self.velocity = vel
        self.active = False

    def ball_movement(self):
        if self.rect.bottom >= Height:
            self.player.hearts -= 1
            self.ball_restart(self.pos)
        if self.rect.top <= 0:
            self.velocity[1] *= -1
        if self.rect.left <= 0 or self.rect.right >= Width:
            self.velocity[0] *= -1

    def ball_restart(self, pos):
        self.active = False
        self.velocity = [2, -2]
        self.rect.center = pos

    def collision(self):
        
        overlap_sprites = pygame.sprite.spritecollide(self, self.blocks, False)
        
        #player and ball collision
        if self.rect.colliderect(self.player.rect):
            overlap_sprites.append(self.player)
        
        #blocks and ball collision
        if overlap_sprites:
            sprite = overlap_sprites[0]
            # patch for the bug when ball hits block from vertical and horizontal both directions
            vertical_top= False
            vertical_bottom= False

            if abs(self.rect.bottom - sprite.rect.top) < Ball_Radius and self.velocity[1] > 0:
                self.rect.bottom = sprite.rect.top  - 1
                self.velocity[1] *= -1
                vertical_top = True
        
                if getattr(sprite,'health',None):
                    sprite.get_damage(Damage)

            if abs(self.rect.top - sprite.rect.bottom) < Ball_Radius and self.velocity[1] < 0:
                self.rect.top = sprite.rect.bottom + 1
                self.velocity[1] *= -1
                vertical_bottom = True

                if getattr(sprite,'health',None):
                    sprite.get_damage(Damage)

            if abs(self.rect.right - sprite.rect.left) < Ball_Radius and self.velocity[0] > 0:
                if not vertical_top and not vertical_bottom:
                    self.rect.right = sprite.rect.left 
                    self.velocity[0] *= -1
                    horizontal_left = True

                    if getattr(sprite,'health',None):
                        sprite.get_damage(Damage)

            if abs(self.rect.left - sprite.rect.right) < Ball_Radius and self.velocity[0] < 0:
                if not vertical_top and not vertical_bottom:
                    self.rect.left = sprite.rect.right 
                    self.velocity[0] *= -1
                    horizontal_right = True

                    if getattr(sprite,'health',None):
                        sprite.get_damage(Damage)
                
    def update(self) -> None:
        if self.active:
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
            self.ball_movement()
            self.collision()
        else:
            self.rect.midbottom = self.player.rect.midtop

class Block(pygame.sprite.Sprite):
    """A class representing a block in the game.

    Attributes:
        image (Surface): The image representing the block.
        rect (Rect): The rectangular area occupied by the block.
        type (int): The type of the block.
        health (int): The health or durability of the block.
        drop (bool): Indicates whether the blocks contains upgrade drop.
        create_upgrade (function) : A function passed from main file to create upgrade/drop animation.

    Methods:
        get_damage(): Reduce the health of the block when hit.
        check_drop(): Create a drop for a block with 0.3 probability.

    """
    def __init__(self, num, pos_x, pos_y, groups, create_up):
        """Initialize the Block object.

        Args:
            pos (tuple): The initial position of the block (x, y).
            block_type (int): The type of the block.
            create_up (function): create_upgrade function.

        """
        super().__init__(groups)
        
        self.type = 2*num
        print(self.type)
        self.health = (num) * 100 

        #sprite setup
        self.image = pygame.image.load('PNG/'+ Block_Type[self.type] + '-Breakout-Tiles.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, Scale_Fac).convert_alpha()
        self.rect = self.image.get_rect(topleft = (pos_x, pos_y))

        self.drop = False
        self.check_drop()

        #player upgrade
        self.create_upgrade = create_up

    def get_damage(self, dam):
        """Reduce the health of the block when hit."""
        self.health -= dam

        if self.health > 0:
            self.type -= 1
            #update block
            self.image = pygame.image.load('PNG/'+ Block_Type[self.type] + '-Breakout-Tiles.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, Scale_Fac).convert_alpha()
        else:
            if self.drop:
                self.create_upgrade(self.rect.midbottom, random.choice(['slow','fast','laser','heart']))
            self.kill()

    def check_drop(self):
        """Check the drop inside block"""
        if random.randint(0,10) > Drop_prob:
            self.drop = True
    
class Laser(pygame.sprite.Sprite):
    """A class representing lasers in the game.

    Attributes:
        image (Surface): The image representing the laser.
        rect (Rect): The rectangular area occupied by the laser.
        speed (int): The speed at which the laser moves.
        blocks (Group): The group of blocks in the game.

    Methods:
        update(): Updates the laser's position and handles collisions.
        collision(): Checks for collision and handles collision with a block.

    """
    def __init__(self, ply_rect : pygame.Rect, blocks) -> None:
        """Initialize the Laser object.

        Args:
            player_rect (Rect): The rectangular area occupied by the player.
            blocks (Group): The group of blocks in the game.

        """
        super().__init__()

        #sprite setup
        self.image = pygame.image.load('PNG/61-Breakout-Tiles.png').convert_alpha()
        #self.image = pygame.transform.rotozoom(self.image, 0, 5*Scale_Fac)
        self.rect = self.image.get_rect(midbottom = ply_rect.midtop)

        self.speed = 2
        self.blocks = blocks
       
    def collision(self):
        """Checks for collision and handles collision with a block."""
        overlap_sprites = pygame.sprite.spritecollide(self, self.blocks, False)
        if overlap_sprites:
            self.kill()
            for sprite in overlap_sprites:
                sprite.get_damage(Damage)
        
    def update(self):
        """Update the laser's position and handle collisions."""
        self.rect.y -= self.speed
        self.collision()

class Upgrade(pygame.sprite.Sprite):
    """A class representing upgrades in the game.

    Attributes:
        image (Surface): The image representing the upgrade.
        rect (Rect): The rectangular area occupied by the upgrade.
        up_type (str): The type of upgrade.
        speed (int): The speed at which the upgrade moves.

    Methods:
        update(): Updates the upgrade's position.

    """
    def __init__(self, pos, up_type, groups) -> None:
        """Initialize the Upgrade object.

        Args:
            pos (tuple): The position of the upgrade (x, y).
            up_type (str): The type of upgrade.

        """
        super().__init__(groups)
        self.up_type = up_type

        #sprite setup
        self.image = pygame.image.load(f'PNG/{Upgrade_Type[up_type]}-Breakout-Tiles.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.15).convert_alpha()
        self.rect = self.image.get_rect(midtop = pos)

        self.speed = 3

    def update(self):
        """Update the upgrade's position."""
        self.rect.y += self.speed
        if self.rect.top >= Height:
            self.kill()