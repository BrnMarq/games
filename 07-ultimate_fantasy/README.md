# Ultimate Fantasy — Turn-Based Cooldowns & Field Menus

This document details two core systems in Ultimate Fantasy: the **cooldown-based turn dispatch system** used during battles and the **out-of-combat field menu system** used during overworld exploration.

---

## Turn-Based Combat: The Cooldown Mechanic

Instead of a traditional rigid round-robin turn system, combat in Ultimate Fantasy utilizes an dynamic **cooldown turn system** driven by [`src/states/game/TakeTurnState.py`](src/states/game/TakeTurnState.py).

### 1. Entity Cooldown Properties
Every combatant (both playable `Character` party members and `Enemy` creatures) inherits from `BattleEntity` and defines:
- **`rest_turns`**: An integer stat representing the recovery time needed after taking an action. Faster characters have a lower `rest_turns` value; slower units have a higher value.
- **`cooldown`**: The integer counter tracking how many cycles remain before this entity can act again.
- **`cooldown_bar`**: A segmented `ProgressBar` rendered next to the combatant in [`src/states/game/BattleState.py`](src/states/game/BattleState.py) displaying current readiness (`value = rest_turns - cooldown`).

### 2. Battle Initialization (`_init_cooldowns`)
At the start of combat, initial cooldowns are randomized:
```python
for entity in self._all_alive_entities():
    entity.cooldown = random.randint(0, entity.rest_turns)
    if hasattr(entity, "cooldown_bar"):
        entity.cooldown_bar.value = entity.rest_turns - entity.cooldown
```
This random offset simulates staggered battle readiness, ensuring combat doesn't always start with the exact same turn order.

### 3. Turn Dispatch & Fast-Forwarding Time (`_next_turn`)
Rather than decrementing turns one by one through empty cycles, the game calculates the next actionable turn instantaneously:
1. **Find Next Combatant**: Finds the lowest remaining cooldown among all living participants:
   ```python
   min_cd = min(e.cooldown for e in alive)
   ```
2. **Fast-Forward Time**: Subtracts `min_cd` from every living entity's cooldown:
   ```python
   for e in alive:
       e.cooldown = max(0, e.cooldown - min_cd)
       if hasattr(e, "cooldown_bar"):
           e.cooldown_bar.value = e.rest_turns - e.cooldown
   ```
3. **Grant Turn**: The entity that reaches `cooldown == 0` is granted the immediate turn (`_give_turn`):
   - **Party Members**: Pushes `BattleMessageState` and `SelectActionState`, allowing the player to select Attack, Skill, Item, or Defend.
   - **Enemies**: Runs enemy AI decision logic to target the party.

### 4. Resetting the Cooldown
Once an entity finishes executing their action, their cooldown is reset:
```python
entity.reset_cooldown()  # sets entity.cooldown = entity.rest_turns
```
The entity's cooldown bar empties, and `_next_turn()` is called to advance to the next ready combatant.

---

## Out-of-Combat Menus

During overworld exploration in [`src/states/game/PlayState.py`](src/states/game/PlayState.py), the player has access to two distinct menus: the **Party Menu** and the **Pause Menu**.

---

### 1. The Party Menu (`PartyMenuState`)

- **Access**: Pressing the **`Tab`** key (`party_menu` binding) while exploring opens the party menu.
- **Overview Panel**: Displays a sleek bottom-of-screen panel ([`src/gui/Panel.py`](src/gui/Panel.py)) summarizing all living party members:
  - Character portrait sprite
  - Name and current Level
  - HP bar and exact current/maximum values (`HP: X/Y`)
  - Core combat attributes: **ATK** (Attack), **DEF** (Defense), and **MAG** (Magic)
- **Navigation**:
  - **Left / Right Arrows**: Cycles between party members with an audible blip and cursor highlight.
  - **Enter**: Opens the selected character's action sub-menu.
  - **Tab**: Closes the party menu and resumes gameplay.

#### Character Actions Sub-Menu (`PartyActionState`)
When pressing Enter on a character, a floating actions panel opens showing all abilities known by that character.
- **Combat vs Field Usability Filtering**:
  - Actions are filtered based on `target_type`.
  - **Healing / Support Skills** (`target_type == "character"`): Enabled and fully selectable outside of combat.
  - **Offensive Combat Skills** (`target_type == "enemy"`): Displayed in semi-transparent grey and cannot be activated.

#### Field Healing (`PartyHealTargetState`)
Selecting a field-usable healing ability transitions to the target selection state:
1. The player uses **Left / Right** to choose which party member should receive the heal.
2. Pressing **Enter** applies the healing formula, plays the recovery audio, updates the target's HP bar immediately, and returns to the menu.
3. This allows the player to sustain the party between dungeon skirmishes without entering combat.

---

### 2. The Pause Menu (`PauseMenuState`)

- **Access**: Pressing the **`Escape`** key while exploring pauses the game and pushes [`src/states/game/PauseMenuState.py`](src/states/game/PauseMenuState.py).
- **Available Options**:
  1. **Continue**: Closes the pause overlay and resumes the game.
  2. **Save Game**: Serializes the current party status, character progression, inventory, and overworld position to a JSON file in the `saves/` folder.
  3. **Quit**: Returns to the title screen.
