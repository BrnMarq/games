# The Legend of the Princess — Bow & Boss Mechanics

This document details the implementation of the Bow combat mechanic, the technical challenges faced when rotating projectile sprites, and the design and AI of the dungeon Boss encounter.

---

## The Bow Implementation

The bow offers a ranged combat alternative to the sword, enabling long-distance projectile attacks and playing an essential role in defeating armored enemies and bosses.

### 1. Acquisition & Controls
- **Dungeon Spawns**: Before the bow is acquired, each newly generated dungeon room has a 1-in-5 chance to spawn a bow item in a chest or on the floor ([`src/world/Room.py`](src/world/Room.py)).
- **Collection**: Picking it up flags `player.has_bow = True`.
- **Controls**: Pressing the **`B`** key triggers `BowCommand` ([`src/commands.py`](src/commands.py)), setting `player.bow_requested = True`.

### 2. Attack State (`PlayerBowAttackState`)
- From either `PlayerIdleState` or `PlayerWalkState`, requesting a bow attack transitions the player into [`src/states/entity/player/PlayerBowAttackState.py`](src/states/entity/player/PlayerBowAttackState.py).
- **Audio & Animation**: Plays the weapon swoosh sound effect and starts the four-directional bow animation (`bow-left`, `bow-right`, `bow-up`, `bow-down`).
- **Arrow Instantiation**: Creates an arrow `GameObject` centered on the player's collision box and registers a new `Projectile` traveling in the player's facing direction:
  ```python
  arrow = GameObject(
      GAME_OBJECT_DEFS["arrow"],
      self.entity.x + self.entity.width / 2 - 4,
      self.entity.y + self.entity.height / 2 - 4,
  )
  self.dungeon.current_room.projectiles.append(
      Projectile(arrow, direction, max_tiles=8)
  )
  ```
- **Travel Limits**: Arrows travel at 150 px/s for up to 8 tiles or until colliding with room walls, obstacles, or enemies.

---

## The Boss Encounter

The dungeon culminates in a dedicated boss battle room designed to test both ranged and melee combat skills.

### 1. Boss Arena (`BossRoom.py`)
- **Isolation**: The boss room contains only the entry doorway; the other three walls are solid.
- **Lockdown**: Upon the player entering, the doorway locks shut. It cannot be reopened until the boss is defeated (`boss_defeated = True`).
- **Clean Arena**: No pots, switches, or obstacles spawn in the room, creating an open duel environment.

### 2. Boss Stats & States
- **Stats**: 10 HP (`health = 10`), deals 2 hearts on contact damage (`contact_damage = 2`).
- **HUD**: Displays a prominent health counter at the top center of the screen (`Boss HP: X/10`).
- **State Machine**:
  - `BossIdleState`: Periodically pauses and evaluates next action.
  - `BossWalkState`: Relentlessly tracks and pursues the player across the arena, re-evaluating trajectory every 0.5–1.5 seconds or upon bumping walls.
  - `BossAttackState`: Pauses movement to play a 32×32 swing animation and launches a homing `Fireball` projectile aimed directly at the player. Fireballs inflict lethal full-health damage if unshielded.
  - `BossStunnedState`: Entered when the boss's shield is broken. Disables all boss movement and attacks for a temporary duration.

### 3. Combat Puzzle: The Shield & Stun Loop
Directly attacking the boss with a sword is ineffective due to the boss's innate shield:

1. **Sword Invulnerability**:
   - The boss starts with `sword_invulnerable = True`.
   - Striking the boss with a sword while shielded deals **0 damage** and deflects.
2. **Breaking the Shield with Arrows**:
   - Arrows cannot defeat the boss directly, but hitting the boss with an arrow breaks its shield:
     - Sets `sword_invulnerable = False`.
     - Places the boss into `BossStunnedState`.
     - Starts a **2.0-second vulnerability window** (`BOSS_VULNERABLE_DURATION = 2.0`).
3. **Visual Vulnerability Indicator**:
   - While vulnerable, the Boss HP counter in the UI changes from **white to red**, signaling the player to rush in and strike.
4. **Melee Damage Window**:
   - Sword strikes during this stunned window deal 1 damage per hit.
5. **Recovery & Stun Cooldown**:
   - Once the 2-second timer expires, the boss recovers, reactivates its sword shield, and enters a **3.0-second stun cooldown** (`BOSS_STUN_COOLDOWN = 3.0`). During this cooldown, arrows cannot re-stun the boss, preventing stun-locking.
6. **Victory**:
   - Upon depleting all 10 HP, the boss is destroyed, the locked door unlocks, and the dungeon victory condition is fulfilled.
