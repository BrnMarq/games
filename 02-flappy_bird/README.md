# Flappy Bird — Hard Mode

This study case introduces an enhanced **Hard Mode** implemented using the Strategy pattern (`HardMode` vs `NormalMode` under [`src/gamemodes/`](src/gamemodes/)).

---

## Entering Hard Mode

From the title screen ([`src/states/TitleScreenState.py`](src/states/TitleScreenState.py)):
- Press **`N`**: Normal Mode (classic Flappy Bird gameplay).
- Press **`H`**: **Hard Mode** (dynamic hazards, movement freedom, and powerups).

---

## Hard Mode Mechanics & Features

### 1. Horizontal Movement Freedom
In addition to the standard jump mechanics (**`Space`**, **`W`**, or **Left Click**), Hard Mode gives the player lateral control:
- **`A`**: Move left at `settings.BIRD_X_SPEED` (100 px/s).
- **`D`**: Move right at `settings.BIRD_X_SPEED` (100 px/s).
- Releasing the key stops horizontal movement (`vx = 0`).

This lateral mobility is crucial for navigating dynamic and closing log obstacles.

---

### 2. Closing Logs & Variable Gaps
In Normal Mode, log pairs spawn at fixed intervals (1.5s) with a fixed gap (90px). Hard Mode introduces randomized difficulty modifiers:
- **Variable Gap Size**: The gap between the upper and lower logs is randomized between `settings.LOGS_GAP - 30` (60px) and `settings.LOGS_GAP` (90px), significantly narrowing the margin of error.
- **Dynamic Spawn Rates**: Logs spawn at unpredictable intervals between 1.0 and 2.0 seconds (`time_to_next_log = random.uniform(1, 2)`).
- **Closing Logs**: Each spawned log pair has a **30% chance** (`CLOSING_LOGS_CHANCE = 30`) to spawn with `closing = True`. While closing, the upper log shifts downward and the lower log shifts upward at `settings.LOG_CLOSE_SPEED` (50 px/s), continuously shrinking the passage.

---

### 3. Star Power-up (Ghost Mode / Invincibility)
To survive the increased difficulty, collectible Star powerups spawn during Hard Mode:

- **Spawn Conditions**:
  - Stars spawn on the right edge of the screen at random heights.
  - Require at least twice the star size clearance from the last log pair.
  - Evaluated every second with a 5% spawn chance (`STAR_SPAWN_CHANCE = 5`) and a 5-second cooldown between stars.
- **Ghost Effect**:
  - Collecting a star grants **10 seconds** of Ghost Mode (`GHOST_DURATION = 10`).
  - **Intangibility**: The bird can safely phase through all logs without colliding or dying (`not (self.bird.ghost_time_left > 0) and self.world.collides_with_logs(...)`).
  - **Ground Danger**: The ground remains solid and lethal; touching the ground will still end the run.
  - **Visuals**: The bird executes a pulsing alpha transparency effect (`bird.start_ghost_pulse()`).
  - **Dynamic Soundtrack**: The background music swaps from the default track (`marios_way.ogg`) to a high-energy track (`ttfaf.ogg` — *Through the Fire and Flames*), and reverts to the normal music once Ghost Mode expires.
