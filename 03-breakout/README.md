# Breakout — Mitosis Powerup

The **Mitosis** powerup is an active ability in Breakout that multiplies every active ball currently in play into three distinct projectiles.

---

## How to Obtain

1. **Brick Drops**: Destroying a brick has a **15% chance** (`POWERUP_CHANCE = 15` in `settings.py`) to spawn a powerup item.
2. **Random Roll**: When a drop occurs, the game randomly rolls among four possible powerups:
   - `TwoMoreBall`
   - `CatchBall`
   - `MissilePowerUp`
   - `MitosisPowerUp`
3. **Paddle Collection**: The powerup slowly falls down the screen; catching it with the paddle collects it.

---

## Charge Mechanism

- **Charge Accumulation**: Collecting the powerup awards **+1 mitosis charge** (`paddle.mitosis_charges += 1`). The player can stack multiple charges.
- **Visual Cue**: While holding at least one mitosis charge, all active balls pulse/blink to visually signal that mitosis is armed and ready to trigger.

---

## Activation

Press the **Action key** (**`F`**) while holding at least one mitosis charge.

When activated in [`src/states/PlayState.py`](src/states/PlayState.py):
1. For every active ball in the game:
   - **Ball 1**: Spawns at the current ball's position, angled **+60°** (`+π/3`) relative to its trajectory.
   - **Ball 2**: Spawns at the current ball's position, angled **−60°** (`−π/3`) relative to its trajectory.
   - **Ball 3**: Spawns at the current ball's position, traveling in the **exact opposite direction** (`−vx, −vy`).
   - All three balls preserve the original ball's speed magnitude.
   - The original ball is removed from play.
2. **Charge Consumption**: One charge is consumed (`paddle.mitosis_charges -= 1`).
3. **Sound Effect**: The activation sound (`activate_mitosis.wav`) plays.

As a result, a single ball triples into three, turning one ball into three, two into six, etc.

---

## Multi-Action Priority Order

The action button (**`F`**) also serves other equipped powerups. When pressed, the game resolves pending actions in the following order:

1. **Release caught balls** (`CatchBall`)
2. **Fire equipped missiles** (`MissilePowerUp`)
3. **Trigger Mitosis** (`MitosisPowerUp`)

---

## Reset Conditions

Mitosis charges are cleared back to 0 when:
- All balls in play are lost (losing a life).
- The level is successfully cleared (victory).
