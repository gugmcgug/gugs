#!/usr/bin/env python3
"""
DnD Dice Roller
Supports standard dice notation: XdY+Z
where X = number of dice, Y = sides per die, Z = modifier
"""

import random
import re
import sys


class DiceRoller:
    """Handles rolling dice using standard DnD notation."""

    # Standard DnD dice types
    VALID_DICE = [4, 6, 8, 10, 12, 20, 100]

    def __init__(self):
        self.pattern = re.compile(r'^(\d+)?d(\d+)([+-]\d+)?$', re.IGNORECASE)

    def roll(self, notation):
        """
        Roll dice based on standard notation.

        Args:
            notation: String like "2d6", "1d20+5", "3d8-2"

        Returns:
            Dictionary with roll details
        """
        notation = notation.strip().lower().replace(' ', '')
        match = self.pattern.match(notation)

        if not match:
            raise ValueError(f"Invalid dice notation: {notation}")

        num_dice = int(match.group(1)) if match.group(1) else 1
        die_type = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0

        if die_type not in self.VALID_DICE:
            print(f"Warning: d{die_type} is not a standard DnD die, but rolling anyway...")

        if num_dice < 1 or num_dice > 100:
            raise ValueError("Number of dice must be between 1 and 100")

        # Roll the dice
        rolls = [random.randint(1, die_type) for _ in range(num_dice)]
        total = sum(rolls) + modifier

        return {
            'notation': notation,
            'num_dice': num_dice,
            'die_type': die_type,
            'modifier': modifier,
            'rolls': rolls,
            'sum_before_modifier': sum(rolls),
            'total': total
        }

    def format_result(self, result):
        """Format roll result for display."""
        rolls_str = ', '.join(str(r) for r in result['rolls'])

        output = [
            f"\nRolling {result['notation']}:",
            f"  Rolls: [{rolls_str}]",
            f"  Sum: {result['sum_before_modifier']}"
        ]

        if result['modifier'] != 0:
            modifier_str = f"{result['modifier']:+d}"
            output.append(f"  Modifier: {modifier_str}")
            output.append(f"  Total: {result['total']}")
        else:
            output.append(f"  Total: {result['total']}")

        return '\n'.join(output)


def print_usage():
    """Print usage information."""
    print("""
DnD Dice Roller
===============

Usage:
  python dice_roller.py [dice notation]

Dice Notation:
  XdY     - Roll X dice with Y sides each
  XdY+Z   - Roll X dice with Y sides, add modifier Z
  XdY-Z   - Roll X dice with Y sides, subtract modifier Z

Examples:
  d20         - Roll one 20-sided die
  2d6         - Roll two 6-sided dice
  1d20+5      - Roll one 20-sided die and add 5
  4d6-2       - Roll four 6-sided dice and subtract 2

Standard DnD Dice: d4, d6, d8, d10, d12, d20, d100

Interactive mode: Run without arguments to enter interactive mode
""")


def interactive_mode():
    """Run in interactive mode."""
    roller = DiceRoller()
    print("DnD Dice Roller - Interactive Mode")
    print("Enter dice notation (e.g., '2d6', '1d20+5') or 'quit' to exit")
    print(f"Standard dice: {', '.join(f'd{d}' for d in roller.VALID_DICE)}")

    while True:
        try:
            notation = input("\n> ").strip()

            if notation.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if notation.lower() in ['help', 'h', '?']:
                print_usage()
                continue

            if not notation:
                continue

            result = roller.roll(notation)
            print(roller.format_result(result))

        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


def main():
    """Main entry point."""
    roller = DiceRoller()

    if len(sys.argv) == 1:
        # No arguments - enter interactive mode
        interactive_mode()
    elif len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help', 'help']:
        print_usage()
    else:
        # Roll each dice notation provided as argument
        for notation in sys.argv[1:]:
            try:
                result = roller.roll(notation)
                print(roller.format_result(result))
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)


if __name__ == '__main__':
    main()
