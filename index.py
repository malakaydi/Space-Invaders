import pygame
import time
import pygame.display
import pygame.event
from pygame.time import Clock
import pygame.transform
import pygame.key
import pygame.font
import pygame.mouse
import sys
import os
import random
from os import path

from pygame.locals import *
from scripts.data import Highscore
from scripts.menu import Menu
from scripts.gameover import GameOver
sound_folder = path.join(path.dirname(__file__), 'sounds')
pygame.init()
pygame.font.init()
pygame.mixer.init()


title = "Space Invaders"
width, height = 1700, 900

FPS = 60

display = pygame.display.set_mode((width, height))
pygame.display.set_caption(title)

clock = Clock()


# Earth
earth_img = pygame.image.load(
    os.path.join("assets", "planets","earth.png")).convert_alpha()
earth = pygame.Rect(
    width - earth_img.get_height() - 100, 100,
    earth_img.get_width(), earth_img.get_height())

# Mars
mars_img = pygame.image.load(
    os.path.join("assets", "planets","mars.png")).convert_alpha()
mars = pygame.Rect(
    100, 450,
    mars_img.get_width(), mars_img.get_height())

# Venus
venus_img = pygame.image.load(
    os.path.join("assets", "planets","venus.png")).convert_alpha()
venus = pygame.Rect(
    width/2 - venus_img.get_width(), 40,
    venus_img.get_width(), venus_img.get_height())

# jupiter
jupiter_img = pygame.image.load(
    os.path.join("assets", "planets","jupiter.png")).convert_alpha()
jupiter = pygame.Rect(
    width - jupiter_img.get_width() - 200, height - jupiter_img.get_height() - 100,
    jupiter_img.get_width(), jupiter_img.get_height())



planets = []

planets.append([jupiter_img, jupiter])
planets.append([earth_img, earth])
planets.append([mars_img, mars])
planets.append([venus_img, venus])




# Player
player_img = pygame.image.load(
    os.path.join("assets","player.png")).convert_alpha()
# PlayerBullet
bullet_img = pygame.image.load(
    os.path.join("assets", "bullet.png"))





# Enemy
enemy_img = pygame.image.load(os.path.join("assets", "enemy.png")).convert_alpha()


# Font
font = pygame.font.SysFont("ComicSans", 70)


# Pause
pause_render = font.render("Pause", True, (255,255,255))


highscore = Highscore()






class Game():
    
    def __init__(self):
        self.run = True
        self.lives = 15
        self.level = 1
        self.score = 0
        self.kills = 0

        self.bullet_ready = False

        self.bullets = []
        self.enemies = []

        self.player = pygame.Rect(
            width/2, height/2, player_img.get_width(), player_img.get_height())

        self.pause_rect = pygame.Rect(
            0 + 30,
            0 + 10,
            pause_render.get_width(),
            pause_render.get_height()
        )

        self.pause = False
        self.lost = False

        self.wavelength = 5
        self.enemy_speed = 3

        self.player_speed = 10


    def draw(self):

        # Draw
        display.fill((50,50,50))



        # Planets
        for planet in planets:
            display.blit(planet[0], (planet[1].x, planet[1].y))



        # Enemy
        for enemy in self.enemies:
            display.blit(enemy_img, (enemy.x, enemy.y))
            enemy.y += self.enemy_speed

            if enemy.y > height + enemy_img.get_height():
                remove_enemy = self.enemies.remove(enemy)
                if remove_enemy == None:
                    self.lives -= 1

            if enemy.colliderect(self.player):
                remove_enemy = self.enemies.remove(enemy)
                if remove_enemy == None:
                    self.lives -= 1
                    self.kills += 1

        display.blit(player_img, (self.player.x, self.player.y))



        # Bullets
        for bullet in self.bullets:
            display.blit(bullet_img, (bullet.x, bullet.y))
            bullet.y -= 10

            if bullet.y < 0:
                if bullet in self.bullets:
                    self.bullets.remove(bullet)   
            else:
                for enemy in self.enemies:
                    if bullet.colliderect(enemy):
                        enemy_remove = self.enemies.remove(enemy)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        else:
                            pass

                        if enemy_remove == None:
                            self.kills += 1


        
        # Texts
        display.blit(pause_render, (self.pause_rect.x, self.pause_rect.y))        
        display.blit(
            self.lives_render,
            (self.pause_rect.x, self.pause_rect.y + 30 + self.lives_render.get_height())
        )
        display.blit(
            self.score_render,
            (width - self.score_render.get_width() - 30, self.pause_rect.y)
        )
        display.blit(
            self.level_render,
            (
                width - self.score_render.get_width() - 30 ,
                self.pause_rect.y + 30 + self.level_render.get_height()
            )
        )
        display.blit(
            self.kills_render,
            (
                width - self.kills_render.get_width() - 55 ,
                self.pause_rect.y + 60 + self.level_render.get_height() + self.kills_render.get_height()
            )
        )
        pygame.display.update()




    def in_while(self):
        self.lives_render = font.render(f"Lives : {self.lives}", True, (255,255,255))
        self.level_render = font.render(f"Level : {self.level}", True, (255,255,255))
        self.score_render = font.render(f"Score : {int(self.score)}", True, (255,255,255))
        self.kills_render = font.render(f"Kills : {self.kills}", True, (255,255,255))




    def movement(self):
        keys_pressed = pygame.key.get_pressed()
    
        if keys_pressed[K_LEFT] and self.player.x > 0:
            self.player.x -= self.player_speed

        if keys_pressed[K_RIGHT] and self.player.x < width - player_img.get_height() - 10:
            self.player.x += self.player_speed

        if keys_pressed[K_UP] and self.player.y > 0:
            self.player.y -= self.player_speed

        if keys_pressed[K_DOWN] and self.player.y < height - player_img.get_height() - 10:
            self.player.y += self.player_speed



    
    def pause_game(self):
        
        display.fill((50,50,50))

        font = pygame.font.SysFont("ComicSans", 100)
        
        resume_render = font.render("Resume", True, (255,255,255))
        resume = pygame.Rect(
            width/2 - resume_render.get_width()/2,
            height/2 - resume_render.get_height()/2 - 75,
            resume_render.get_width(),
            resume_render.get_height()
        )

        menu_render = font.render("Menu", True, (255,255,255))
        menu_rect = pygame.Rect(
            width/2 - menu_render.get_width()/2,
            height/2 - menu_render.get_height()/2 + 75,
            menu_render.get_width(),
            menu_render.get_height()
        )


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == K_ESCAPE:
                if event.key == K_SPACE:
                    return "resume"

        # Draw
        display.blit(resume_render, (resume.x, resume.y))
        display.blit(menu_render, (menu_rect.x, menu_rect.y))

        
        # mouse pos
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = list(pygame.mouse.get_pressed())
            

        if resume.collidepoint(mouse_pos):

            if mouse_pressed[0] == True:
                self.pause = False                

        if menu_rect.collidepoint(mouse_pos):

            if mouse_pressed[0] == True:
                self.run = False
                self.pause = False
                Menu(width, height, title, Game, planets).start(display)

        pygame.display.update()



    def play(self):
        while self.run:

            clock.tick(FPS)

            self.in_while()
            self.draw()
            self.movement()

            for event in pygame.event.get():
            
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.pause = True
                    
                    if event.key == K_SPACE:
                        self.bullet_ready = True
                    


            # If enemies == 0
            if len(self.enemies) == 0:
                for i in range(self.wavelength):
                    enemy = pygame.Rect(
                        random.randrange(0, width - enemy_img.get_width()),
                        random.randrange(-1000, 0-enemy_img.get_height()),
                        enemy_img.get_width(),
                        enemy_img.get_height()
                    )
                    self.enemies.append(enemy)

                self.level += 1 
                self.wavelength += 2
                self.enemy_speed += 1





            # LevelsETC
            self.score += 1/FPS
            if self.lives <= 0:
                self.lost = True
                

            if self.lost:
                time.sleep(1)
                self.run = False

                GameOver(
                    width,
                    height,
                    title,
                    planets,
                    Game           
                ).start(self.score, self.kills, display)



            
            # Score
            if int(self.score) > int(highscore.get_highscore()):
                highscore.write_highscore(f"{int(self.score)}")



            # Bullet
            if self.bullet_ready:
                bullet = pygame.Rect(
                    self.player.x + player_img.get_width()/2 - bullet_img.get_width()/2,
                    self.player.y,
                    bullet_img.get_width(),
                    bullet_img.get_height()
                )
                
                self.bullets.append(bullet)
                self.bullet_ready = False


            # Buttons Clicks
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = list(pygame.mouse.get_pressed())
                
            if self.pause_rect.collidepoint(mouse_pos):
                if mouse_pressed[0] == True:
                    self.pause = True 

            
            while self.pause:
                self.pause_game()

menu_song = pygame.mixer.music.load(path.join(sound_folder, "menu.ogg"))
pygame.mixer.music.play(-1)
if __name__ == "__main__":
    menu = Menu(width, height, title, Game, planets)
    menu.start(display)