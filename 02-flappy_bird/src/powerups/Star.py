import pygame

import settings


class Star:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = settings.STAR_SIZE
        self.height: float = settings.STAR_SIZE
        self.texture = pygame.transform.smoothscale(
            settings.TEXTURES["star"], (settings.STAR_SIZE, settings.STAR_SIZE)
        )

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def update(self, dt: float) -> None:
        self.x += -settings.MAIN_SCROLL_SPEED * dt

    def is_out_of_game(self) -> bool:
        return self.x < -settings.STAR_SIZE

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, self.get_rect())
