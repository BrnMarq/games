# Match-3 — Powerups & Design Documentation

This project extends the classic Match-3 mechanics with special powerup tiles, direct interactive detonation, cascading reactions, and an improved visual design.

---

## Powerups

Special powerup tiles are created by making larger tile combinations. Instead of destroying all matched tiles, the tile that the player moved transforms into an active powerup.

### 1. Line Clear Powerup (`line_clear`)

- **Creation**:
  - Formed when creating a match of **exactly 4 tiles** (`len(match) == 4`).
  - The tile dragged to create the match is preserved and upgraded to the `line_clear` powerup (rendered with `settings.LINE_CLEAR_TILE_FRAME`).
- **Activation Methods**:
  - **Direct Tap / Click**: Clicking or tapping directly on the powerup tile with minimal movement (< 5 pixels) instantly detonates it.
  - **Match Integration**: Combining the powerup tile into a standard 3+ tile match of its matching color.
- **Effect**:
  - Clears adjacent tiles in a **cross/plus pattern** (orthogonal directions: 1 tile up, down, left, and right via `get_line_clear_targets`).
  - Plays the `line_clear` sound effect.
- **Cascade Trigger**:
  - If any tile caught in the cross explosion is itself another powerup (`line_clear` or `bomb`), it automatically detonates in chain reaction via `collect_cascade_targets`.

---

### 2. Bomb Powerup (`bomb`)

- **Creation**:
  - Formed when creating a match of **5 or more tiles** (`len(match) >= 5`).
  - The moved tile upgrades to the `bomb` powerup (rendered with `settings.BOMB_TILE_FRAME`).
- **Activation Methods**:
  - **Direct Tap / Click**: Clicking or tapping directly on the bomb tile with minimal movement (< 5 pixels) instantly detonates it.
  - **Match Integration**: Matching the bomb with 2 or more tiles of the same color.
- **Effect**:
  - Clears all surrounding tiles in a **3×3 square area** (all 8 adjacent tiles via `get_bomb_targets`).
  - Plays the `bomb` sound effect.
- **Cascade Trigger**:
  - Any powerup caught within the 3×3 explosion radius is recursively detonated, potentially triggering massive chain reactions across the board.

---

## Scoring & Board Flow

- Each tile eliminated by matches or powerup explosions awards **50 points** (`len(tiles) * 50`).
- Once tiles are cleared, remaining tiles above drop smoothly using tween animations (`get_falling_tiles`), and replacement tiles drop in from the top.
- Falling tiles that settle into new matches automatically chain and resolve until no matches remain.
- The board validates available moves (`has_valid_move`); if no valid moves exist (including powerup taps), the board automatically regenerates to guarantee continuous playability.

---

## Design Choices

### Removal of Tile Variants

In the initial design, tiles of the same color included multiple pattern variants (different patterns or sub-varieties on the spritesheet). 

During development and playtesting, having multiple visual variants per color proved to be **too confusing for the player**:
1. Players frequently mistook different tile patterns as representing different colors or mechanics.
2. It added unnecessary visual noise to the board, making it hard to spot valid 3-in-a-row opportunities at a glance.
3. It competed with the special icons of actual powerup tiles (`line_clear` and `bomb`).

**Decision**: Tile variants were removed, standardizing all tiles to a single clean base frame (`settings.BASE_TILE_FRAME`). This ensures maximum visual clarity: color uniquely denotes matching sets, while special frame graphics are reserved exclusively for powerup tiles.
