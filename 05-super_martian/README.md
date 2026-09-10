# Super Martian — Key Block & Level Progression

This study case introduces an objective-driven level completion mechanic centered around a hidden **Key Block** and collectible **Key**.

---

## The Key Block Lifecycle

The key block acts as the bridge to clearing a level. Its behavior spans four distinct phases: hidden state, reveal upon reaching the score objective, hitting the block to spawn the key, and collecting the key to advance.

---

### 1. Level Start: Hidden State
- In the level's tilemap, special blocks are defined on the `ground` layer with the custom Tiled property `key_block = True`.
- During map initialization in [`src/GameLevel.py`](src/GameLevel.py) (`_hide_key_block_tiles`):
  - All tiles with `key_block: True` are located and their positions/GIDs are saved to `self.key_block_tiles`.
  - Their positions in the tilemap are set to `0` (empty/transparent).
  - Consequently, at the start of a level the block is completely invisible and non-collidable.

---

### 2. Spawning / Revealing the Key Block
- In [`src/states/game_states/PlayState.py`](src/states/game_states/PlayState.py), the game monitors the player's score each frame:
  ```python
  if (
      not self.game_level.key_block_revealed
      and self.player.score >= settings.SCORE_OBJECTIVE
  ):
      self.game_level.reveal_key_block()
  ```
- Once the player collects enough coins to reach `settings.SCORE_OBJECTIVE`:
  - `reveal_key_block()` is called.
  - The saved tile GID is restored back into the `ground` layer (`ground[row][col] = gid`), instantly making the block solid and visible in the world.
  - The `reveal_keyblock` sound effect plays to alert the player.

---

### 3. Hitting the Block & Key Emergence
- When the player jumps and hits the block from below, `player.block_hit_from_below` is flagged by the collision resolution.
- The player invokes `_check_key_block()`, which checks the tile above the player's head for the `key_block` property.
- If hit, `game_level.spawn_key(block_x, block_y)` is called:
  1. A `GameItem` instance representing the Key is created at the block's coordinates (`texture_id="items"`, `frame_index=0`).
  2. A tween animation moves the key 16 pixels upwards over 0.5 seconds (`Timer.tween(0.5, [(self.key, {"y": block_y - 16})])`), popping it out from the top of the block.
  3. The key becomes an active, collidable item hovering above the block.

---

### 4. Key Pickup & Level Transition
- When the player collides with the key:
  - The key's `on_consume` handler triggers `pickup_key` in [`src/definitions/items.py`](src/definitions/items.py):
    - Plays `settings.SOUNDS["key"]`.
    - Sets `player.key_picked = True`.
  - In `PlayState.update()`, detecting `player.key_picked`:
    - Halts and unloads background music.
    - Clears active level timers.
    - Tweens a screen fade-out to black (`fade_alpha: 255` over 0.5 seconds).
    - Once the fade-out completes, advances to the next stage:
      ```python
      next_level = (self.level % settings.NUM_LEVELS) + 1
      self.state_machine.change("play", level=next_level, fade_in=True)
      ```
