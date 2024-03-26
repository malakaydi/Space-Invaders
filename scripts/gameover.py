from .data import Highscore
from pygame.locals import *
import pygame
from .menu import Menu

highscore = Highscore()
#gameover
class GameOver():
    def __init__(self, width, height, title, planets, game_class):
        self.width = width
        self.height = height
        self.title = title
        self.planets = planets

        self.gameover = True

        self.game = game_class

        self.game_over_font = pygame.font.SysFont("ComicSans", 130)
        self.font = pygame.font.SysFont("ComicSans", 100)


        self.menu_render = self.font.render("Space To Menu", True, (255,255,255))
        self.menu_rect = pygame.Rect(
            width/2 - self.menu_render.get_width()/2,
            height/2 - self.menu_render.get_height()/2 - 80 ,
            self.menu_render.get_width(),
            self.menu_render.get_height()
        )

    def start(self, score, kills, display):
        while self.gameover:

            display.fill((50,50,50))
            
            game_over_render = self.game_over_font.render("Game Over", True, (255,255,255))

            score_render = self.font.render(f"Score : {int(score)}", True, (255,255,255))
            kills_render = self.font.render(f"Kills : {kills}", True, (255,255,255))
            highscore_render = self.font.render(f"Highscore : {highscore.get_highscore()}", True, (255,255,255))




            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        Menu(
                            self.width,
                            self.height,
                            self.title,
                            self.game,
                            self.planets,
                        ).start(display)


            # Draw
            for planet in self.planets:
                display.blit(planet[0], (planet[1].x, planet[1].y))

            display.blit(game_over_render, (self.width/2 - game_over_render.get_width()/2, 50))
            display.blit(self.menu_render, (self.menu_rect.x, self.menu_rect.y))
            
            display.blit(
                score_render,
                (
                    self.width/2 - score_render.get_width()/2,
                    self.height/2 - score_render.get_height()/2 + 40
                )
            )
            
            display.blit(
                kills_render,
                (
                    self.width/2 - kills_render.get_width()/2,
                    self.height/2 - kills_render.get_height()/2 + 60 + score_render.get_height()
                )
            )

            display.blit(
                highscore_render,
                (
                    self.width/2 - highscore_render.get_width()/2,
                    self.height/2 - highscore_render.get_height()/2 + 140 + kills_render.get_height()
                )
            )

            pygame.display.update()


