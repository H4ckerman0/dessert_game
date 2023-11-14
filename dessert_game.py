import pygame 
import os, sys
from random import randint, choice

if getattr(sys, 'frozen', False):
    game_path = os.path.dirname(sys.executable)
elif __file__:
    game_path = os.path.dirname(__file__)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load(game_path + r'\graphics\player\player_walk1.png').convert_alpha()
        player_walk2 = pygame.image.load(game_path + r'\graphics\player\player_walk2.png').convert_alpha()
        self.player_jump = pygame.image.load(game_path + r'\graphics\player\player_jump.png').convert_alpha()
        self.player_walk = [player_walk1,player_walk2]
        self.player_index = 0
        self.gravity = 0
        self.player_surf = self.player_walk[self.player_index]
        self.image = self.player_surf
        self.rect = self.image.get_rect(midbottom = (100,410))

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 410: self.rect.bottom = 410

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 410:
            self.gravity = -20

    def animation(self):
        if self.rect.bottom < 410:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index > len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.animation()
        self.apply_gravity()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == "enemy_ground":
            enemyground_walk1 = pygame.image.load(game_path + r"\graphics\enemy\enemy_ground\enemy_ground_walk1.png").convert_alpha()
            enemyground_walk2 = pygame.image.load(game_path + r"\graphics\enemy\enemy_ground\enemy_ground_walk2.png").convert_alpha()
            self.frames = [enemyground_walk1,enemyground_walk2]
            y_pos = 410
        elif type == "enemy_fly": 
            enemyfly1 = pygame.image.load(game_path + r"\graphics\enemy\enemy_fly\enemy_fly1.png").convert_alpha()
            enemyfly2 = pygame.image.load(game_path + r"\graphics\enemy\enemy_fly\enemy_fly2.png").convert_alpha()
            self.frames = [enemyfly1,enemyfly2]
            y_pos = 210
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom = (randint(1250,1500),y_pos))

    def animation(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animation()
        self.movement()

    def movement(self):
        self.rect.x -= 7
        if self.rect.right <= -100: self.kill()

def display_score():
    time = pygame.time.get_ticks() - start_time
    score_surf = font.render(f"Score: {int(time/1000)}", False, (100,100,75))
    score_rect = score_surf.get_rect(center = (500,100))
    pygame.draw.rect(screen,(50,50,25),score_rect)
    screen.blit(score_surf,score_rect)
    return time

def collision():
    if pygame.sprite.spritecollide(player.sprite, obst_group, False):
        obst_group.empty()
        return False
    return True

pygame.init()

screen = pygame.display.set_mode((1000,500))
clock = pygame.time.Clock()
font = pygame.font.Font(game_path + r"\font\slkscr.ttf", 50)
pygame.display.set_caption("First PyGame")
game_active = False
start_time = 0
score = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

obst_group = pygame.sprite.Group()

sky_surf = pygame.image.load(game_path + r"\graphics\background\dessert_Sky.png").convert_alpha()
ground_surf = pygame.image.load(game_path + r"\graphics\background\dessert_ground.png").convert_alpha()

title_surf = font.render("Game", False, (50,50,25))
title_surf = pygame.transform.rotozoom(title_surf,0,2)
title_rect = title_surf.get_rect(center = (500,100))

instr_surf = font.render("Press Space to play", False, (50,50,25))
instr_rect = instr_surf.get_rect(center = (500,400))

playerfront_surf = pygame.image.load(game_path + r"\graphics\player\player _front.png").convert_alpha()
playerfront_surf = pygame.transform.rotozoom(playerfront_surf,0,2)
playerfront_rect = playerfront_surf.get_rect(center = (500,250))

obstacle_event = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_event,1500)

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:  
                
            if event.type == obstacle_event:
                obst_group.add(Obstacle(choice(["enemy_fly","enemy_ground"])))
        else:
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_active = True
                        score = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_active = True

    if game_active:
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,410))
        score = display_score()

        player.update()
        player.draw(screen)

        obst_group.draw(screen)
        obst_group.update()

        game_active = collision()
    else:
        score_surf = font.render(f"Score: {int(score/1000)}", False, (50,50,25))
        score_rect = score_surf.get_rect(center = (500,400))
        screen.fill((120,110,85))
        screen.blit(title_surf,title_rect)
        screen.blit(playerfront_surf,playerfront_rect)
        start_time = pygame.time.get_ticks()

        if score == 0:
            screen.blit(instr_surf,instr_rect)
        else:
            screen.blit(score_surf,score_rect)

    clock.tick(60)