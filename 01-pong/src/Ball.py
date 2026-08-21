import pygame

import settings


class Ball:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        self.vy: float = 0.0
        self.vx: float = 0.0

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def update(self, dt: float) -> None:
        self.y += self.vy * dt
        self.x += self.vx * dt

    def render(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, pygame.Color(settings.COLOR_WHITE), self.get_rect())

    def reset(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
