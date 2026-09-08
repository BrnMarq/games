# Pong — AI Paddle Implementation

This project implements an autonomous AI opponent for Player 2 (the right paddle) to enable single-player gameplay against the computer.

---

## AI Implementation Details

The AI logic is implemented in [`01-pong/src/states/PlayState.py`](src/states/PlayState.py) within the `ai_player` method, which is executed every frame during `PlayState.update(dt)`.

```python
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
```

### How It Works

1. **Center Calculation**:
   - The AI computes the vertical center of the ball: `ball_center = ball.y + (ball.width / 2)`.
   - The AI computes the vertical center of the paddle: `p_center = player.y + (player.height / 2)`.

2. **Deadband / Acceptance Margin (`acceptance_margin = 4`)**:
   - Without an acceptance margin, a tracking AI can jitter rapidly back and forth around the ball's center line whenever the difference in height is smaller than the frame step (`vy * dt`).
   - A margin of ±4 pixels introduces a deadband: if the paddle center is within 4 pixels of the ball center, `player.vy` is set to `0`, producing smooth and stable paddle motion.

3. **Directional Steering**:
   - **Move Up**: If `p_center > ball_center + acceptance_margin`, the paddle is lower than the ball, so `player.vy = -settings.PADDLE_SPEED` (-140 px/s).
   - **Move Down**: If `p_center < ball_center - acceptance_margin`, the paddle is higher than the ball, so `player.vy = settings.PADDLE_SPEED` (140 px/s).
   - **Stop**: If within the margin, the paddle stops vertical movement (`player.vy = 0`).

4. **Clamping & Constraints**:
   - Paddle vertical positions are automatically constrained between `0` and `settings.VIRTUAL_HEIGHT - self.height` in [`01-pong/src/Paddle.py`](src/Paddle.py) on every `update(dt)`, preventing the AI from escaping the playing field boundaries.
