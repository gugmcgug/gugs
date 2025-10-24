# Claude Code Skills

This directory contains custom skills for Claude Code.

## Available Skills

### dice

A DnD dice roller skill that uses the `dice_roller.py` script.

**Usage:**
- Invoke with: "use the dice skill" or "roll some dice"
- Claude will use the dice_roller.py script to roll dice
- Supports all standard DnD dice notation

**Examples:**
- "Roll a d20"
- "Roll 2d6+3 for damage"
- "Roll with advantage" (will roll 2d20)

### treasure

A D&D 3.5 treasure generator skill that uses the `treasure_generator.py` script.

**Usage:**
- Invoke with: "use the treasure skill" or "generate treasure"
- Claude will use the treasure_generator.py script to generate treasure based on CR
- Supports CR 1-20+ with coins, gems, art objects, and magic items
- Magic items include weapons with brands (flaming, keen, etc.), armor, potions, scrolls, wands, rings, and wondrous items

**Examples:**
- "Generate treasure for CR 7"
- "What treasure would a CR 15 dragon have?"
- "Roll treasure for a goblin camp (CR 3)"

## How Skills Work

Skills are markdown files that define specialized behaviors for Claude. When invoked, Claude will follow the instructions in the skill file to complete tasks.

To use a skill, simply mention it in conversation or ask Claude to use it by name.
