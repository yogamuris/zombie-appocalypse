import sys
import pygame
from bullet import Bullet
from zombie import Zombie
from time import sleep

def check_keydown_events(event, ai_settings, screen, fighter, bullets):
    if event.key == pygame.K_RIGHT:
        fighter.moving_right = True
    elif event.key == pygame.K_LEFT:
        fighter.moving_left = True
    elif event.key == pygame.K_SPACE:
        shoot_bullet(ai_settings, screen, fighter, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def shoot_bullet(ai_settings, screen, fighter, bullets):
    if len(bullets) < ai_settings.bullets.allowed:
        new_bullet = Bullet(ai_settings, screen, fighter)
        bullets.add(new_bullet)

def check_keyup_events(event, fighter):
    if event.key == pygame.K_RIGHT:
        fighter.moving_right = False
    elif event.key == pygame.K_LEFT:
        fighter.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, fighter, zombies, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, fighter, zombies, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, fighter, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, fighter)

def check_play_button(ai_settings, screen, stats, sb, play_button, fighter, zombies, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False), 
        
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()

        zombies.empty()
        bullets.empty()

        create_fighter(ai_settings, screen, fighter, zombies)
        fighter.center_fighter()

def get_number_zombies_x(ai_settings, zombie_width):
    available_space_x = ai_settings.screen_width - 2 * zombie_width
    number_zombies_x = int(available_space_x / (2 * zombie_width))
    return number_zombies_x

def get_number_rows(ai_settings, fighter_height, zombie_height):
    available_space_y = (ai_settings.screen_height - (3 * zombie_height) - fighter_height)
    number_rows = int(available_space_y / (2 * zombie_height))
    return number_rows

def create_zombie(ai_settings, screen, zombies, zombie_number, row_number):
    zombie = Zombie(ai_settings, screen)
    zombie_width = zombie.rect.width
    zombie.x = zombie_width + 2 * zombie_width * zombie_number
    zombie.rect.x = zombie.x
    zombie.rect.y = zombie.rect.height + 2 * zombie.rect.height * row_number
    zombies.add(zombie)

def create_fighter(ai_settings, screen, fighter, zombies):
    zombie = Zombie(ai_settings, screen)
    number_zombies_x = get_number_zombies_x(ai_settings, zombie.rect.width)
    number_rows = get_number_rows(ai_settings, fighter.rect.height, zombie.rect.height)

    for row_number in range(number_rows):
        for zombie_number in range(number_zombies_x):
            create_zombie(ai_settings, screen, zombies, zombie_number, row_number)

def update_screen(ai_settings, screen, stats, sb, fighter, zombies, bullets, play_button):
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()
    fighter.blitme()
    zombies.draw(screen)

    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()
    
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, fighter, zombies, bullets):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_zombie_collisions(ai_settings, screen, stats, sb, fighter, zombies, bullets)

def check_bullet_zombie_collisions(ai_settings, screen, stats, sb, fighter, zombies, bullets):
    collisions = pygame.sprite.groupcollide(bullets, zombies, True, True)
    if collisions:
        for zombies in collisions.values():
            stats.score += ai_settings.zombie_points * len(zombies)
            sb.prep_score()
        
        check_high_score(stats, sb)

    if len(zombies) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        stats.level += 1
        sb.prep_level()

        create_fighter(ai_settings, screen, fighter, zombies)

def check_fighter_edges(ai_settings, zombies):
    for zombie in zombies.sprites():
        if zombie.check_edges():
            change_fighter_direction(ai_settings, zombies)
            break


def change_fighter_direction(ai_settings, zombies):
    for zombie in zombies.sprites():
        zombie.rect.y += ai_settings.fighter_drop_speed
    ai_settings.fighter_direction *= -1

def update_zombies(ai_settings, stats, screen, fighter, zombies, bullets):
    check_fighter_edges(ai_settings, zombies)
    zombies.update()

    if pygame.sprite.spritecollideany(fighter, zombies):
        fighter_hit(ai_settings, stats, screen, fighter, zombies, bullets)

    check_zombies_bottom(ai_settings, stats, screen, fighter, zombies, bullets)

def fighter_hit(ai_settings, stats, screen, fighter, zombies, bullets):
    if stats.fighters_left > 0:
        stats.fighters_left -= 1

        zombies.empty()
        bullets.empty()

        create_fighter(ai_settings, screen, fighter, zombies)
        fighter.center_fighter()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_zombies_bottom(ai_settings, stats, screen, fighter, zombies, bullets):
    screen_rect = screen.get_rect()
    for zombie in zombies.sprites():
        if zombie.rect.bottom >= screen_rect.bottom:
            fighter_hit(ai_settings, stats, screen, fighter, zombies, bullets)
            break

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
