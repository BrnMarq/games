import random
import pygame

import settings

from gale.state import BaseState
from gale.input_handler import InputData, KeyboardData

from src.rendering import render_table
from src.Paddle import Paddle


class PlayState(BaseState):
    def enter(self, pong, *args, **kwargs) -> None:
        self.pong = pong

    def render(self, surface: pygame.Surface) -> None:
        render_table(surface, self.pong)

    def _randomize_vy(self) -> None:
        magnitude = random.randint(10, 149)
        self.pong.ball.vy = -magnitude if self.pong.ball.vy < 0 else magnitude

    def _score(self, scorer: int) -> None:
        pong = self.pong
        pong.player1.vy = 0
        pong.player2.vy = 0

        settings.SOUNDS["score"].play()

        if scorer == 1:
            pong.p1_score += 1
            pong.serving_player = 2
        else:
            pong.p2_score += 1
            pong.serving_player = 1

        if pong.p1_score == settings.MAX_POINTS or pong.p2_score == settings.MAX_POINTS:
            pong.winning_player = scorer
            self.state_machine.change("done", pong=pong)
            return

        pong.ball.reset(
            settings.VIRTUAL_WIDTH / 2 - pong.ball.width / 2,
            settings.VIRTUAL_HEIGHT / 2 - pong.ball.height / 2,
        )
        self.state_machine.change("serve", pong=pong)

    def update(self, dt) -> None:
        pong = self.pong

        self.ai_player(pong.player2)

        pong.player1.update(dt)
        pong.player2.update(dt)
        pong.ball.update(dt)

        ball_rect = pong.ball.get_rect()

        if ball_rect.right >= settings.VIRTUAL_WIDTH:
            self._score(1)
            return
        elif ball_rect.left <= 0:
            self._score(2)
            return

        if ball_rect.top <= 0:
            pong.ball.y = 0
            pong.ball.vy *= -1
            settings.SOUNDS["wall_hit"].play()
        elif ball_rect.bottom >= settings.VIRTUAL_HEIGHT:
            pong.ball.y = settings.VIRTUAL_HEIGHT - pong.ball.height
            pong.ball.vy *= -1
            settings.SOUNDS["wall_hit"].play()

        ball_rect = pong.ball.get_rect()
        p1_rect = pong.player1.get_rect()
        p2_rect = pong.player2.get_rect()

        if ball_rect.colliderect(p1_rect):
            pong.ball.x = p1_rect.right
            pong.ball.vx *= -1.03
            self._randomize_vy()
            settings.SOUNDS["paddle_hit"].play()
        if ball_rect.colliderect(p2_rect):
            pong.ball.x = p2_rect.left - pong.ball.width
            pong.ball.vx *= -1.03
            self._randomize_vy()
            settings.SOUNDS["paddle_hit"].play()

    def on_input(self, input_id: str, input_data: InputData) -> None:
        pong = self.pong
        if isinstance(input_data, KeyboardData):
            if input_id in ("p1_up", "p1_down"):
                if input_data.pressed:
                    pong.player1.vy = (
                        -settings.PADDLE_SPEED
                        if input_id == "p1_up"
                        else settings.PADDLE_SPEED
                    )
                elif input_data.released:
                    sign = -1 if input_id == "p1_up" else 1
                    if pong.player1.vy == sign * settings.PADDLE_SPEED:
                        pong.player1.vy = 0

    def ai_player(self, player: Paddle) -> None:
        ball = self.pong.ball

        ball_center = ball.y + (ball.width / 2)
        p_center = player.y + (player.height / 2)

        acceptance_margin = 4

        if p_center > ball_center + acceptance_margin:
            player.vy = -settings.PADDLE_SPEED
        elif p_center < ball_center - acceptance_margin:
            player.vy = settings.PADDLE_SPEED
        else:
            player.vy = 0
