from typing import Any
import pygame
import random
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, blocks, speed=5):
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
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= Width:
            self.rect.right = Width

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        self.constraint()

    def upgrade(self, upgrade_type):
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
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if (current_time - self.laser_time) >= self.laser_cooldown:
                self.ready = True

    def update(self):
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
    def __init__(self, pos, player, blocks, vel = [2, -2]) -> None:
        super().__init__()
        self.player = player
        self.blocks = blocks

        #sprite setup
        self.image = pygame.image.load('PNG/58-Breakout-Tiles.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.20).convert_alpha()
        self.rect = self.image.get_rect(midbottom = self.player.rect.midtop)

        self.pos = pos
        self.ball_vel = vel
        self.active = False

    def ball_movement(self):
        if self.rect.bottom >= Height:
            self.player.hearts -= 1
            self.ball_restart(self.pos)
        if self.rect.top <= 0:
            self.ball_vel[1] *= -1
        if self.rect.left <= 0 or self.rect.right >= Width:
            self.ball_vel[0] *= -1

    def ball_restart(self, pos):
        self.active = False
        self.ball_vel = [2, -2]
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

            if abs(self.rect.bottom - sprite.rect.top) < Ball_Radius and self.ball_vel[1] > 0:
                self.rect.bottom = sprite.rect.top  - 1
                self.ball_vel[1] *= -1
                vertical_top = True
        
                if getattr(sprite,'health',None):
                    sprite.get_damage(50)

            if abs(self.rect.top - sprite.rect.bottom) < Ball_Radius and self.ball_vel[1] < 0:
                self.rect.top = sprite.rect.bottom + 1
                self.ball_vel[1] *= -1
                vertical_bottom = True

                if getattr(sprite,'health',None):
                    sprite.get_damage(50)

            if abs(self.rect.right - sprite.rect.left) < Ball_Radius and self.ball_vel[0] > 0:
                if not vertical_top and not vertical_bottom:
                    self.rect.right = sprite.rect.left 
                    self.ball_vel[0] *= -1
                    horizontal_left = True

                    if getattr(sprite,'health',None):
                        sprite.get_damage(50)

            if abs(self.rect.left - sprite.rect.right) < Ball_Radius and self.ball_vel[0] < 0:
                if not vertical_top and not vertical_bottom:
                    self.rect.left = sprite.rect.right 
                    self.ball_vel[0] *= -1
                    horizontal_right = True

                    if getattr(sprite,'health',None):
                        sprite.get_damage(50)
                
    def update(self) -> None:
        if self.active:
            self.rect.x += self.ball_vel[0]
            self.rect.y += self.ball_vel[1]
            self.ball_movement()
            self.collision()
        else:
            self.rect.midbottom = self.player.rect.midtop

class Block(pygame.sprite.Sprite):
    def __init__(self, num, pos_x, pos_y, groups, create_up):
        super().__init__(groups)

        self.num = 2*num
        self.health = (num) * 100 

        #sprite setup
        self.image = pygame.image.load('PNG/'+ Block_Type[self.num] + '-Breakout-Tiles.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, Scale_Fac).convert_alpha()
        self.rect = self.image.get_rect(topleft = (pos_x, pos_y))

        self.drop = False
        self.check_drop()

        #player upgrade
        self.create_upgrade = create_up

    def get_damage(self, dam):
        self.health -= dam

        if self.health > 0:
            self.num -= 1
            #update block
            self.image = pygame.image.load('PNG/'+ Block_Type[self.num] + '-Breakout-Tiles.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, Scale_Fac).convert_alpha()
        else:
            if self.drop:
                self.create_upgrade(self.rect.midbottom, random.choice(['slow','fast','laser','heart']))
            self.kill()

    def check_drop(self):
        if random.randint(0,10) > 7:
            self.drop = True
    
class Laser(pygame.sprite.Sprite):
    def __init__(self, ply_rect : pygame.Rect, blocks) -> None:
        super().__init__()

        #sprite setup
        self.image = pygame.image.load('PNG/61-Breakout-Tiles.png').convert_alpha()
       #self.image = pygame.transform.rotozoom(self.image, 0, 5*Scale_Fac)
        self.rect = self.image.get_rect(midbottom = ply_rect.midtop)

        self.speed = 2
        self.blocks = blocks
       
    def collision(self):
        #Laser block collision
        overlap_sprites = pygame.sprite.spritecollide(self, self.blocks, False)
        if overlap_sprites:
            self.kill()
            for sprite in overlap_sprites:
                sprite.get_damage(50)
        
    def update(self):
        self.rect.y -= self.speed
        self.collision()

class Upgrade(pygame.sprite.Sprite):
    def __init__(self, pos, up_type, groups) -> None:
        super().__init__(groups)
        self.up_type = up_type

        #sprite setup
        self.image = pygame.image.load(f'PNG/{Upgrade_Type[up_type]}-Breakout-Tiles.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.15).convert_alpha()
        self.rect = self.image.get_rect(midtop = pos)

        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= Height:
            self.kill()