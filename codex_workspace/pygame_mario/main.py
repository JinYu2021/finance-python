import pygame

from audio import SoundManager
from camera import Camera
from coin import Coin
from enemy import Enemy
from level import Level
from player import Player
from settings import (
    BG_COLOR,
    COIN_SPAWNS,
    COIN_SFX_PATH,
    DEATH_SFX_PATH,
    ENEMY_SPAWNS,
    FPS,
    FPS_COLOR,
    HEIGHT,
    JUMP_SFX_PATH,
    LEVEL_CSV_PATH,
    PLAYER_SPAWN,
    WIDTH,
    WINDOW_TITLE,
)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    sounds = SoundManager(
        jump_path=JUMP_SFX_PATH,
        coin_path=COIN_SFX_PATH,
        death_path=DEATH_SFX_PATH,
    )

    def reset_level_state() -> tuple[Level, Player, list[Enemy], list[Coin], Camera, int]:
        level = Level(LEVEL_CSV_PATH)
        player = Player(*PLAYER_SPAWN)
        enemies = [Enemy(x, y) for x, y in ENEMY_SPAWNS]
        coins = [Coin(x, y) for x, y in COIN_SPAWNS]
        camera = Camera(level.world_width)
        score = 0
        return level, player, enemies, coins, camera, score

    level, player, enemies, coins, camera, score = reset_level_state()
    paused = False
    player_dead = False

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    level, player, enemies, coins, camera, score = reset_level_state()
                    paused = False
                    player_dead = False
                    continue

                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    continue

                if player_dead and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    player.respawn()
                    player_dead = False
                    continue

            if not paused and not player_dead and player.handle_event(event):
                sounds.play_jump()

        if not paused:
            if not player_dead:
                player.update(dt, level.solid_tiles, level.world_width, level.world_height)

            for enemy in enemies:
                enemy.update(dt, level.solid_tiles, level.world_width, level.world_height)

            if not player_dead:
                for enemy in enemies:
                    if not enemy.alive:
                        continue
                    if not player.rect.colliderect(enemy.rect):
                        continue

                    stomped = (
                        player.vy > 0
                        and player.prev_rect.bottom <= enemy.rect.top + 4
                        and player.rect.bottom >= enemy.rect.top
                    )
                    if stomped:
                        enemy.kill()
                        player.bounce()
                    else:
                        player_dead = True
                        sounds.play_death()
                        break

                for coin in coins:
                    if coin.collected:
                        continue
                    if player.rect.colliderect(coin.rect):
                        coin.collect()
                        score += 1
                        sounds.play_coin()

            camera.update(player.rect.centerx)

        screen.fill(BG_COLOR)
        level.draw(screen, camera)

        for coin in coins:
            coin.draw(screen, camera)

        for enemy in enemies:
            enemy_screen_rect = camera.world_to_screen_rect(enemy.rect)
            enemy.draw(screen, enemy_screen_rect)

        player_screen_rect = camera.world_to_screen_rect(player.rect)
        player.draw(screen, player_screen_rect)

        score_text = font.render(f"Score: {score}", True, FPS_COLOR)
        screen.blit(score_text, (12, 10))

        fps_value = clock.get_fps()
        fps_text = font.render(f"FPS: {fps_value:.1f}", True, FPS_COLOR)
        screen.blit(fps_text, (12, 36))

        if paused:
            paused_text = font.render("Paused - Esc Continue / R Restart", True, FPS_COLOR)
            screen.blit(paused_text, (12, 62))
        elif player_dead:
            dead_text = font.render("You Died - Press Enter to Respawn", True, FPS_COLOR)
            screen.blit(dead_text, (12, 62))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
