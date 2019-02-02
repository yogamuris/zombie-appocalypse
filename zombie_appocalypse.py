import sys

import pygame
from pygame.sprite import Group

from settings import Settings
from fighter import Fighter
from zombie import Zombie
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Zombie Appocalypse')

    play_button = Button(ai_settings, screen, "Play Game")

    fighter = Fighter(ai_settings, screen)
    bullets = Group()
    zombies = Group()

    gf.create_fighter(ai_settings, screen, fighter, zombies)

    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, fighter, zombies, bullets)
        if stats.game_active:
            fighter.update()
            bullets.update()
            gf.update_bullets(ai_settings, screen, stats, sb, fighter, zombies, bullets)
            gf.update_zombies(ai_settings, stats, screen, fighter, zombies, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, fighter, zombies, bullets, play_button)

run_game()