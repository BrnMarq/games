# Throw a Bird — Bird Divider (Split) Powerup

This project implements an airborne **Bird Divider (Split)** ability, allowing the player to split a launched bird into three distinct projectiles mid-flight.

---

## How It Works

When activated, the flying bird splits into a spread of **three independent birds**

---

## Activation & Preconditions

### 1. Trigger
- Key Binding: Press the **`Space`** key (`split` input action in [`settings.py`](settings.py)).

### 2. Preconditions
In [`src/states/game/PlayState.py`](src/states/game/PlayState.py), splitting is allowed only when:
```python
if self.flinging and self.can_split and not self.has_split:
    self._split_bird()
```
- **In Flight (`flinging = True`)**: The bird must already be launched from the slingshot.
- **Single Use per Turn (`not has_split`)**: The ability can only be triggered once per shot.
- **Mid-Air Only (`can_split = True`)**:
  - `can_split` is enabled the moment the bird is released from the slingshot.
  - While flying, the game monitors all physical bodies touching the bird:
    ```python
    for other in self.bird.body.touching_bodies:
        if other.user_data != "wind":
            self.can_split = False
            break
    ```
  - If the bird collides with any solid obstacle, structure block, ground, or enemy (anything other than wind zones), `can_split` is permanently disabled for that shot.
  - **The player must activate the split while airborne before impact.**

---

## Division Mechanics (`_split_bird`)

When the split triggers:
1. **Sampling Velocity & Heading**:
   - The engine measures the current velocity vector, total speed, and trajectory angle of the parent bird:
     ```python
     velocity = self.bird.body.velocity
     speed = velocity.length()
     angle = math.atan2(velocity.y, velocity.x)
     ```
2. **Spawning Two Additional Birds**:
   - Two new `Bird` physics instances are instantiated at the exact coordinates of the original bird.
   - **Bird 1 (Upper Angle)**: Deflected by **−15°** (`angle - 15°`), retaining the original speed:
     ```python
     angle1 = angle - math.radians(15)
     bird1.body.velocity = (speed * math.cos(angle1), speed * math.sin(angle1))
     ```
   - **Bird 2 (Lower Angle)**: Deflected by **+15°** (`angle + 15°`), retaining the original speed:
     ```python
     angle2 = angle + math.radians(15)
     bird2.body.velocity = (speed * math.cos(angle2), speed * math.sin(angle2))
     ```
   - **Original Bird (Center)**: Continues along its current forward trajectory with unaffected velocity.
3. **Tri-Spread Trajectory**:
   - The result is a fan spread of three active physics bodies covering a much wider area.

---

## Multi-Bird Physics & Turn Reset

- **Active Physics Simulation**:
  - Both new birds are added to `self.additional_birds`.
  - All three birds possess full physical properties (mass, friction, restitution, collision callbacks, and gravity).
- **Turn Idle Detection (`_update_idle`)**:
  - The turn only ends when **all active birds** come to a complete rest:
    ```python
    all_birds = [self.bird] + self.additional_birds
    ```
  - If any bird is still moving (linear or angular velocity above threshold), the turn continues.
- **Cleanup & Reset**:
  - Once all birds are stationary for `IDLE_FRAMES_LIMIT` frames:
    - The physics bodies of all extra spawned birds are safely destroyed from the physics world (`self.world.destroy_body(b.body)`).
    - `self.additional_birds.clear()` empties the secondary list.
    - `self.has_split = False` resets the ability flag.
    - The main bird returns to the slingshot for the next shot.
