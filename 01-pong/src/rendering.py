import pygame

import settings

from gale.text import render_text


def render_table(surface: pygame.Surface, pong):
    pygame.draw.rect(
        surface,
        pygame.Color(settings.COLOR_WHITE),
        pygame.Rect(
            settings.VIRTUAL_WIDTH / 2 - settings.MID_LINE_WIDTH / 2,
            0,
            settings.MID_LINE_WIDTH,
            settings.VIRTUAL_HEIGHT,
        ),
    )
    pong.player1.render(surface)
    pong.player2.render(surface)
    pong.ball.render(surface)

    render_text(
        surface,
        str(pong.p1_score),
        settings.FONTS["score"],
        settings.VIRTUAL_WIDTH / 2 - 50,
        settings.VIRTUAL_HEIGHT / 6,
        pygame.Color(settings.COLOR_WHITE),
        center=True,
    )
    render_text(
        surface,
        str(pong.p2_score),
        settings.FONTS["score"],
        settings.VIRTUAL_WIDTH / 2 + 50,
        settings.VIRTUAL_HEIGHT / 6,
        pygame.Color(settings.COLOR_WHITE),
        center=True,
    )
