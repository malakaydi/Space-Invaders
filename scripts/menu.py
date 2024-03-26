from .data import Highscore
from pygame.locals import *
import pygame
import pygame.display

highscore = Highscore()
#menu
class Menu():
    def __init__(self, width, height, title, game_class, planets):
        self.menu = True
        self.game = game_class()
        
        self.width = width
        self.height = height

        self.title = title

        self.planets = planets

        self.title_font = pygame.font.SysFont("ComicSans", 200)
        self.font = pygame.font.SysFont("ComicSans", 120)

        self.play_render = self.font.render("Play", True, (255, 255, 255))
        self.play_rect = pygame.Rect(
                self.width/2 - self.play_render.get_width()/2,
                self.height/2 - self.play_render.get_height()/2 - 50,
                self.play_render.get_width(),
                self.play_render.get_height()
            )


    def start(self, display):

        while self.menu:
            display.fill((50, 50, 50))


            title_render = self.title_font.render(self.title, True, (255, 255, 255))
            highscore_render = self.font.render(
                f"Highscore : {highscore.get_highscore()}", True, (255, 255, 255))

            # Draw
            for planet in self.planets:
                display.blit(planet[0], (planet[1].x, planet[1].y))

            display.blit(self.play_render, (self.play_rect.x, self.play_rect.y))
            
            display.blit(
                title_render, (self.width/2 - title_render.get_width()/2, 20))
            display.blit(highscore_render, (self.width/2 - highscore_render.get_width() /
                                2, self.height/2-highscore_render.get_height()/2 + 50))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.menu = False
                        self.game.play()

            mouse_pos = pygame.mouse.get_pos()  
            mouse_pressed = list(pygame.mouse.get_pressed())

            if self.play_rect.collidepoint(mouse_pos):
                if mouse_pressed[0] == True:
                    self.menu = False
                    self.game.play()

            pygame.display.update()

