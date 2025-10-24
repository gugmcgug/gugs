#!/usr/bin/env python3
"""
D&D 3.5 Treasure Generator
Based on DMG 3.5 treasure tables and Magic Item Compendium
"""

import random
import sys
from typing import Dict, List, Tuple, Optional


# ============================================================================
# TREASURE TABLES BY CR (DMG Table 3-3)
# ============================================================================

TREASURE_TABLES = {
    1: {'coins': (1, 'd6', 30, []), 'goods': 0, 'items': 0},
    2: {'coins': (1, 'd6', 60, []), 'goods': 0, 'items': 0},
    3: {'coins': (1, 'd6', 100, []), 'goods': 0, 'items': 0},
    4: {'coins': (1, 'd8', 150, []), 'goods': 0.15, 'items': 0},
    5: {'coins': (1, 'd10', 200, []), 'goods': 0.20, 'items': 0.05},
    6: {'coins': (1, 'd10', 300, []), 'goods': 0.30, 'items': 0.10},
    7: {'coins': (1, 'd12', 400, []), 'goods': 0.40, 'items': 0.15},
    8: {'coins': (2, 'd6', 500, []), 'goods': 0.45, 'items': 0.20},
    9: {'coins': (2, 'd8', 700, []), 'goods': 0.50, 'items': 0.25},
    10: {'coins': (2, 'd8', 1000, []), 'goods': 0.55, 'items': 0.30},
    11: {'coins': (3, 'd8', 1500, []), 'goods': 0.60, 'items': 0.35},
    12: {'coins': (3, 'd10', 2000, []), 'goods': 0.65, 'items': 0.40},
    13: {'coins': (3, 'd10', 3000, []), 'goods': 0.70, 'items': 0.50},
    14: {'coins': (4, 'd10', 4000, []), 'goods': 0.70, 'items': 0.55},
    15: {'coins': (4, 'd12', 5000, []), 'goods': 0.75, 'items': 0.60},
    16: {'coins': (5, 'd12', 7500, []), 'goods': 0.75, 'items': 0.65},
    17: {'coins': (5, 'd12', 10000, []), 'goods': 0.80, 'items': 0.70},
    18: {'coins': (6, 'd12', 15000, []), 'goods': 0.80, 'items': 0.75},
    19: {'coins': (6, 'd12', 20000, []), 'goods': 0.85, 'items': 0.80},
    20: {'coins': (6, 'd12', 30000, []), 'goods': 0.85, 'items': 0.85},
}


# ============================================================================
# COIN TYPES AND DISTRIBUTION
# ============================================================================

def roll_dice(num: int, sides: int, multiplier: int = 1) -> int:
    """Roll dice and return result."""
    return sum(random.randint(1, sides) for _ in range(num)) * multiplier


def generate_coins(cr: int) -> Dict[str, int]:
    """Generate coins based on CR."""
    if cr not in TREASURE_TABLES:
        cr = min(20, max(1, cr))

    table = TREASURE_TABLES[cr]
    num_dice, die_type, base_gp, _ = table['coins']
    die_size = int(die_type[1:])  # Extract number from 'd6', 'd8', etc.

    total_gp = roll_dice(num_dice, die_size) * base_gp

    # Distribute among coin types (weighted toward GP at higher CR)
    coins = {'cp': 0, 'sp': 0, 'gp': 0, 'pp': 0}

    if cr <= 3:
        # Low level: mostly copper and silver
        coins['cp'] = roll_dice(3, 6) * 10
        coins['sp'] = roll_dice(2, 6) * 10
        coins['gp'] = total_gp // 10
    elif cr <= 6:
        # Low-mid: silver and gold
        coins['sp'] = roll_dice(2, 8) * 10
        coins['gp'] = total_gp // 5
    elif cr <= 10:
        # Mid: mostly gold
        coins['gp'] = total_gp
    else:
        # High: gold and platinum
        pp_amount = total_gp // 20
        coins['pp'] = pp_amount
        coins['gp'] = total_gp - (pp_amount * 10)

    return {k: v for k, v in coins.items() if v > 0}


# ============================================================================
# GEMS AND ART OBJECTS (DMG Table 3-5)
# ============================================================================

GEMS = {
    4: ['irregular freshwater pearl', 'hematite', 'azurite', 'blue quartz', 'malachite', 'obsidian', 'turquoise'],
    10: ['bloodstone', 'carnelian', 'chalcedony', 'chrysoprase', 'citrine', 'jasper', 'moonstone', 'onyx', 'rock crystal'],
    50: ['agate', 'alexandrite', 'amber', 'amethyst', 'chrysoberyl', 'coral', 'garnet', 'jade', 'jet', 'pearl', 'spinel', 'tourmaline'],
    100: ['deep blue spinel', 'golden yellow topaz', 'emerald', 'white opal', 'black pearl'],
    500: ['alexandrite', 'aquamarine', 'violet garnet', 'black pearl', 'deep blue sapphire', 'emerald', 'fire opal', 'star ruby'],
    1000: ['emerald', 'white sapphire', 'black sapphire', 'fire opal', 'star ruby', 'star sapphire', 'jacinth'],
    5000: ['black sapphire', 'diamond', 'jacinth', 'ruby'],
}

ART_OBJECTS = {
    10: ['brass mug', 'carved bone statuette', 'small woven rug', 'embroidered silk handkerchief'],
    25: ['silver ring', 'carved ivory scroll case', 'decorated copper stein', 'silver-trimmed small mirror'],
    75: ['silver chalice', 'carved jade figurine', 'crystal vial', 'gold-trimmed spellbook'],
    250: ['gold ring with gems', 'silver necklace with pendant', 'electrum statuette', 'gold-trimmed silk robe'],
    750: ['silver coronet with gems', 'gold bracelet with gems', 'electrum censer with silver filigree', 'gold statuette'],
    2500: ['platinum crown with gems', 'gold and ruby ring', 'gold scepter with diamonds', 'jeweled gold anklet'],
    7500: ['platinum and sapphire crown', 'jeweled golden collar', 'gold and ruby scepter', 'diamond-studded platinum idol'],
}


def generate_goods(cr: int) -> List[Tuple[str, int]]:
    """Generate gems and art objects."""
    goods = []

    if cr not in TREASURE_TABLES:
        cr = min(20, max(1, cr))

    chance = TREASURE_TABLES[cr]['goods']
    if random.random() > chance:
        return goods

    # Number of items based on CR
    num_items = roll_dice(1, 4) if cr <= 10 else roll_dice(2, 4)

    for _ in range(num_items):
        # Choose gem or art
        is_gem = random.random() < 0.7

        # Select value based on CR
        if cr <= 4:
            values = [4, 10]
        elif cr <= 7:
            values = [10, 50, 100]
        elif cr <= 10:
            values = [50, 100, 500]
        elif cr <= 14:
            values = [100, 500, 1000]
        elif cr <= 17:
            values = [500, 1000, 5000]
        else:
            values = [1000, 5000]

        value = random.choice(values)

        if is_gem and value in GEMS:
            item_desc = random.choice(GEMS[value])
            goods.append((f"Gem ({value} gp): {item_desc}", value))
        elif not is_gem and value in ART_OBJECTS:
            item_desc = random.choice(ART_OBJECTS[value])
            goods.append((f"Art ({value} gp): {item_desc}", value))

    return goods


# ============================================================================
# MAGIC ITEMS - WEAPONS
# ============================================================================

WEAPON_TYPES = [
    'longsword', 'greatsword', 'bastard sword', 'rapier', 'scimitar', 'shortsword', 'dagger',
    'battleaxe', 'greataxe', 'handaxe', 'warhammer', 'light hammer', 'heavy mace', 'light mace',
    'morningstar', 'heavy flail', 'light flail', 'spear', 'longspear', 'shortspear',
    'composite longbow', 'longbow', 'composite shortbow', 'shortbow', 'light crossbow', 'heavy crossbow'
]

WEAPON_BRANDS = {
    'flaming': (1, 8000),
    'frost': (1, 8000),
    'shock': (1, 8000),
    'keen': (1, 8000),
    'thundering': (1, 8000),
    'anarchic': (2, 18000),
    'axiomatic': (2, 18000),
    'holy': (2, 18000),
    'unholy': (2, 18000),
    'flaming burst': (2, 18000),
    'icy burst': (2, 18000),
    'shocking burst': (2, 18000),
    'wounding': (2, 18000),
    'vorpal': (5, 50000),
}


def get_weapon_price(enhancement: int, brands: List[str] = None) -> int:
    """Calculate weapon price based on enhancement and brands."""
    base_weapon_price = 350  # Average martial weapon

    if brands is None:
        brands = []

    # Calculate total enhancement equivalent
    total_enhancement = enhancement
    brand_cost = 0

    for brand in brands:
        if brand in WEAPON_BRANDS:
            equiv, flat_cost = WEAPON_BRANDS[brand]
            total_enhancement += equiv
            brand_cost += flat_cost

    # Price formula: base + (enhancement^2 * 2000) + flat brand costs
    bonus_price = (total_enhancement ** 2) * 2000
    return base_weapon_price + bonus_price + brand_cost


def generate_magic_weapon(cr: int) -> Tuple[str, int]:
    """Generate a magic weapon."""
    # Enhancement bonus based on CR
    if cr <= 5:
        enhancement = 1
        brands = []
    elif cr <= 8:
        enhancement = random.choice([1, 1, 1, 2])
        brands = [random.choice(list(WEAPON_BRANDS.keys()))] if random.random() < 0.3 else []
    elif cr <= 12:
        enhancement = random.choice([1, 2, 2, 2])
        brands = [random.choice(list(WEAPON_BRANDS.keys()))] if random.random() < 0.5 else []
    elif cr <= 16:
        enhancement = random.choice([2, 2, 3, 3])
        brands = [random.choice([k for k, v in WEAPON_BRANDS.items() if v[0] <= 2])]
    else:
        enhancement = random.choice([3, 3, 4, 4, 5])
        brands = random.sample([k for k, v in WEAPON_BRANDS.items() if v[0] <= 2],
                              random.choice([1, 1, 2]))

    weapon_type = random.choice(WEAPON_TYPES)

    # Build description
    desc = f"+{enhancement}"
    if brands:
        desc += " " + " ".join(brands)
    desc += f" {weapon_type}"

    price = get_weapon_price(enhancement, brands)

    return (desc, price)


# ============================================================================
# MAGIC ITEMS - ARMOR
# ============================================================================

ARMOR_TYPES = [
    'chain shirt', 'chainmail', 'breastplate', 'scale mail', 'half-plate', 'full plate',
    'leather armor', 'studded leather', 'hide armor',
    'light steel shield', 'heavy steel shield', 'tower shield'
]


def generate_magic_armor(cr: int) -> Tuple[str, int]:
    """Generate magic armor."""
    if cr <= 6:
        enhancement = 1
    elif cr <= 10:
        enhancement = random.choice([1, 1, 2])
    elif cr <= 14:
        enhancement = random.choice([2, 2, 3])
    else:
        enhancement = random.choice([3, 4, 5])

    armor_type = random.choice(ARMOR_TYPES)
    base_armor_price = 150  # Average
    price = base_armor_price + (enhancement ** 2) * 1000

    return (f"+{enhancement} {armor_type}", price)


# ============================================================================
# MAGIC ITEMS - POTIONS, SCROLLS, WANDS
# ============================================================================

POTION_TYPES = [
    ('cure light wounds', 50),
    ('cure moderate wounds', 300),
    ('cure serious wounds', 750),
    ('cure critical wounds', 1000),
    ('invisibility', 300),
    ('fly', 750),
    ('haste', 750),
    ('heroism', 750),
    ('neutralize poison', 1000),
    ('resist energy', 300),
    ('lesser restoration', 300),
    ('protection from arrows', 300),
    ('bull\'s strength', 300),
    ('cat\'s grace', 300),
    ('bear\'s endurance', 300),
]


def generate_potion(cr: int) -> Tuple[str, int]:
    """Generate a potion."""
    # Filter by CR
    if cr <= 5:
        valid = [p for p in POTION_TYPES if p[1] <= 300]
    elif cr <= 10:
        valid = [p for p in POTION_TYPES if p[1] <= 750]
    else:
        valid = POTION_TYPES

    name, price = random.choice(valid)
    return (f"Potion of {name}", price)


SCROLL_SPELLS = [
    ('magic missile', 25, 1),
    ('shield', 25, 1),
    ('mage armor', 25, 1),
    ('identify', 25, 1),
    ('cure light wounds', 25, 1),
    ('bless', 25, 1),
    ('invisibility', 150, 2),
    ('knock', 150, 2),
    ('levitate', 150, 2),
    ('cure moderate wounds', 150, 2),
    ('fireball', 375, 3),
    ('haste', 375, 3),
    ('fly', 375, 3),
    ('cure serious wounds', 375, 3),
    ('greater invisibility', 700, 4),
    ('dimension door', 700, 4),
]


def generate_scroll(cr: int) -> Tuple[str, int]:
    """Generate a scroll."""
    if cr <= 4:
        max_level = 1
    elif cr <= 8:
        max_level = 2
    elif cr <= 12:
        max_level = 3
    else:
        max_level = 4

    valid = [s for s in SCROLL_SPELLS if s[2] <= max_level]
    spell, price, level = random.choice(valid)

    return (f"Scroll of {spell}", price)


WAND_SPELLS = [
    ('magic missile', 750),
    ('cure light wounds', 750),
    ('shield', 750),
    ('burning hands', 750),
    ('cure moderate wounds', 4500),
    ('fireball', 11250),
]


def generate_wand(cr: int) -> Tuple[str, int]:
    """Generate a wand with 50 charges."""
    if cr <= 8:
        valid = [w for w in WAND_SPELLS if w[1] <= 750]
    elif cr <= 12:
        valid = [w for w in WAND_SPELLS if w[1] <= 4500]
    else:
        valid = WAND_SPELLS

    spell, price = random.choice(valid)
    charges = 50  # Standard new wand

    return (f"Wand of {spell} ({charges} charges)", price)


# ============================================================================
# MAGIC ITEMS - RINGS AND WONDROUS ITEMS
# ============================================================================

RINGS = [
    ('ring of protection +1', 2000),
    ('ring of protection +2', 8000),
    ('ring of protection +3', 18000),
    ('ring of feather falling', 2200),
    ('ring of swimming', 2500),
    ('ring of climbing', 2500),
    ('ring of jumping', 2500),
    ('ring of sustenance', 2500),
    ('ring of counterspells', 4000),
    ('ring of mind shielding', 8000),
    ('ring of invisibility', 20000),
]

WONDROUS_ITEMS = [
    ('bag of holding (type I)', 2500),
    ('bag of holding (type II)', 5000),
    ('cloak of resistance +1', 1000),
    ('cloak of resistance +2', 4000),
    ('cloak of resistance +3', 9000),
    ('cloak of elvenkind', 2500),
    ('cloak of the bat', 26000),
    ('boots of elvenkind', 2500),
    ('boots of speed', 12000),
    ('boots of teleportation', 49000),
    ('bracers of armor +1', 1000),
    ('bracers of armor +2', 4000),
    ('bracers of armor +3', 9000),
    ('amulet of natural armor +1', 2000),
    ('amulet of natural armor +2', 8000),
    ('amulet of natural armor +3', 18000),
    ('gloves of dexterity +2', 4000),
    ('gauntlets of ogre power', 4000),
    ('headband of intellect +2', 4000),
    ('periapt of wisdom +2', 4000),
    ('belt of giant strength +2', 4000),
    ('robe of the archmagi', 75000),
    ('robe of stars', 58000),
    ('portable hole', 20000),
    ('rope of climbing', 3000),
    ('rope of entanglement', 21000),
    ('handy haversack', 2000),
    ('everburning torch', 110),
]


def generate_ring(cr: int) -> Tuple[str, int]:
    """Generate a magic ring."""
    if cr <= 8:
        valid = [r for r in RINGS if r[1] <= 4000]
    elif cr <= 14:
        valid = [r for r in RINGS if r[1] <= 10000]
    else:
        valid = RINGS

    return random.choice(valid)


def generate_wondrous_item(cr: int) -> Tuple[str, int]:
    """Generate a wondrous item."""
    if cr <= 6:
        valid = [w for w in WONDROUS_ITEMS if w[1] <= 2500]
    elif cr <= 10:
        valid = [w for w in WONDROUS_ITEMS if w[1] <= 5000]
    elif cr <= 14:
        valid = [w for w in WONDROUS_ITEMS if w[1] <= 15000]
    else:
        valid = WONDROUS_ITEMS

    return random.choice(valid)


# ============================================================================
# ITEM GENERATION
# ============================================================================

def generate_magic_items(cr: int) -> List[Tuple[str, int]]:
    """Generate magic items based on CR."""
    items = []

    if cr not in TREASURE_TABLES:
        cr = min(20, max(1, cr))

    chance = TREASURE_TABLES[cr]['items']
    if random.random() > chance:
        return items

    # Number of items
    if cr <= 5:
        num_items = 1
    elif cr <= 10:
        num_items = random.choice([1, 1, 2])
    elif cr <= 15:
        num_items = random.choice([1, 2, 2, 3])
    else:
        num_items = random.choice([2, 2, 3, 3, 4])

    for _ in range(num_items):
        # Choose item type
        roll = random.random()

        if cr <= 4:
            # Low level: mostly potions and scrolls
            if roll < 0.4:
                items.append(generate_potion(cr))
            elif roll < 0.8:
                items.append(generate_scroll(cr))
            else:
                items.append(generate_wondrous_item(cr))
        elif cr <= 8:
            # Mid-low: varied with some weapons/armor
            if roll < 0.2:
                items.append(generate_magic_weapon(cr))
            elif roll < 0.35:
                items.append(generate_magic_armor(cr))
            elif roll < 0.55:
                items.append(generate_potion(cr))
            elif roll < 0.70:
                items.append(generate_scroll(cr))
            elif roll < 0.85:
                items.append(generate_wondrous_item(cr))
            else:
                items.append(generate_ring(cr))
        elif cr <= 12:
            # Mid: more weapons/armor, add wands
            if roll < 0.25:
                items.append(generate_magic_weapon(cr))
            elif roll < 0.45:
                items.append(generate_magic_armor(cr))
            elif roll < 0.55:
                items.append(generate_potion(cr))
            elif roll < 0.65:
                items.append(generate_scroll(cr))
            elif roll < 0.75:
                items.append(generate_wand(cr))
            elif roll < 0.87:
                items.append(generate_wondrous_item(cr))
            else:
                items.append(generate_ring(cr))
        else:
            # High: emphasis on permanent items
            if roll < 0.30:
                items.append(generate_magic_weapon(cr))
            elif roll < 0.50:
                items.append(generate_magic_armor(cr))
            elif roll < 0.55:
                items.append(generate_potion(cr))
            elif roll < 0.60:
                items.append(generate_scroll(cr))
            elif roll < 0.70:
                items.append(generate_wand(cr))
            elif roll < 0.85:
                items.append(generate_wondrous_item(cr))
            else:
                items.append(generate_ring(cr))

    return items


# ============================================================================
# MAIN GENERATION AND OUTPUT
# ============================================================================

class TreasureHoard:
    """Represents a complete treasure hoard."""

    def __init__(self, cr: int):
        self.cr = cr
        self.coins = generate_coins(cr)
        self.goods = generate_goods(cr)
        self.items = generate_magic_items(cr)

    def total_value(self) -> int:
        """Calculate total treasure value in GP."""
        total = 0

        # Coins
        total += self.coins.get('cp', 0) / 100
        total += self.coins.get('sp', 0) / 10
        total += self.coins.get('gp', 0)
        total += self.coins.get('pp', 0) * 10

        # Goods
        total += sum(value for _, value in self.goods)

        # Items
        total += sum(price for _, price in self.items)

        return int(total)

    def format_output(self) -> str:
        """Format the treasure hoard for display."""
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"TREASURE HOARD - CR {self.cr}")
        lines.append(f"{'='*60}\n")

        # Coins
        if self.coins:
            lines.append("COINS:")
            for coin_type in ['pp', 'gp', 'sp', 'cp']:
                if coin_type in self.coins:
                    lines.append(f"  {self.coins[coin_type]:,} {coin_type}")
            lines.append("")

        # Goods
        if self.goods:
            lines.append("GOODS:")
            for item_desc, _ in self.goods:
                lines.append(f"  {item_desc}")
            lines.append("")

        # Magic Items
        if self.items:
            lines.append("MAGIC ITEMS:")
            for item_desc, price in self.items:
                lines.append(f"  {item_desc} ({price:,} gp)")
            lines.append("")

        if not self.coins and not self.goods and not self.items:
            lines.append("No treasure found!\n")

        # Total
        lines.append(f"{'='*60}")
        lines.append(f"TOTAL VALUE: {self.total_value():,} gp")
        lines.append(f"{'='*60}\n")

        return '\n'.join(lines)


def generate_treasure(cr: int) -> TreasureHoard:
    """Generate a treasure hoard for the given CR."""
    return TreasureHoard(cr)


def print_usage():
    """Print usage information."""
    print("""
D&D 3.5 Treasure Generator
===========================

Usage:
  python treasure_generator.py [CR]

Arguments:
  CR    Challenge Rating (1-20+) for treasure generation

Examples:
  python treasure_generator.py 5    - Generate treasure for CR 5
  python treasure_generator.py 12   - Generate treasure for CR 12
  python treasure_generator.py      - Interactive mode

Interactive mode: Run without arguments for interactive treasure generation
""")


def interactive_mode():
    """Run in interactive mode."""
    print("D&D 3.5 Treasure Generator - Interactive Mode")
    print("Enter CR (1-20+) or 'quit' to exit")

    while True:
        try:
            user_input = input("\nCR> ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Happy adventuring!")
                break

            if user_input.lower() in ['help', 'h', '?']:
                print_usage()
                continue

            if not user_input:
                continue

            try:
                cr = int(user_input)
                if cr < 1:
                    print("CR must be at least 1")
                    continue

                hoard = generate_treasure(cr)
                print(hoard.format_output())

            except ValueError:
                print("Please enter a valid number for CR")

        except KeyboardInterrupt:
            print("\nHappy adventuring!")
            break
        except EOFError:
            print("\nHappy adventuring!")
            break


def main():
    """Main entry point."""
    if len(sys.argv) == 1:
        interactive_mode()
    elif len(sys.argv) == 2:
        if sys.argv[1] in ['-h', '--help', 'help']:
            print_usage()
        else:
            try:
                cr = int(sys.argv[1])
                if cr < 1:
                    print("Error: CR must be at least 1")
                    sys.exit(1)

                hoard = generate_treasure(cr)
                print(hoard.format_output())
            except ValueError:
                print("Error: CR must be a number")
                print_usage()
                sys.exit(1)
    else:
        print("Error: Too many arguments")
        print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
