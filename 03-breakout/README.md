# Mitosis Powerup

The **Mitosis** powerup lets you split every ball in play into three at equal angles(60 degrees)

## How to get it

- Each brick destroyed has a **15% chance** (`POWERUP_CHANCE` in `settings.py`) to drop a random powerup.
- When a drop occurs, one of four powerups is chosen at random: `TwoMoreBall`, `CatchBall`, `MissilePowerUp`, or `MitosisPowerUp`.
- Like every other powerup, it falls from the destroyed brick; catch it with the paddle to collect it.

## Collecting a charge

- On pickup it grants **one mitosis charge** (`paddle.mitosis_charges += 1`). You can carry multiple charges.
- All balls currently in play immediately **blink** — a visual cue that the charge is armed and ready.

## Activating

Press the **action button** (key **F**) while holding a charge. For every ball in play:

1. A new ball is spawned at the same position, rotated **+60°** (`π/3`).
2. A new ball is spawned at the same position, rotated **−60°** (`−π/3`).
3. A new ball is spawned travelling in the **exact opposite direction** of the original.
4. All three keep the original ball's speed.
5. The original ball is removed.

The result is **three balls where there was one**, and the charge counter drops by 1. The activation sound (`activate_mitosis.wav`) plays.

## Order of operations

The action button also releases caught balls (`CatchBall`) and fires missiles (`MissilePowerUp`). On a single press the game handles all of them in sequence:

1. Release any caught balls.
2. Fire missiles.
3. Activate mitosis.

## Resetting

Mitosis charges are removed when:

- The paddle loses every ball in play (a life), or
- The level is cleared (victory).

