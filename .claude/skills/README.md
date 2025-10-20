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

## How Skills Work

Skills are markdown files that define specialized behaviors for Claude. When invoked, Claude will follow the instructions in the skill file to complete tasks.

To use a skill, simply mention it in conversation or ask Claude to use it by name.
