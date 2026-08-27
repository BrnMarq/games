import pygame

import settings


class Missile:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.texture = settings.TEXTURES["rocket"]
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
        self.vy = -200
        self.active = True

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def collides(self, another) -> bool:
        return self.get_collision_rect().colliderect(another.get_collision_rect())

    def update(self, dt: float) -> None:
        self.y += self.vy * dt
        if self.y + self.height < 0:
            self.active = False

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, (self.x, self.y))
