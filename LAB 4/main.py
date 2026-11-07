import pygame
from game.game_engine import GameEngine

WIDTH, HEIGHT = 500, 560
FPS = 60
GRASS_GREEN = (120, 170, 90)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Whack-a-Mole")
    clock = pygame.time.Clock()
    engine = GameEngine(WIDTH, HEIGHT)
    running = True

    while running:
        screen.fill(GRASS_GREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                engine.handle_event(event)

        engine.handle_input()
        engine.update()
        engine.render(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
