"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.
"""

import random
from evennia.objects.objects import DefaultCharacter

class Character(DefaultCharacter):
    """
    The Character class represents a player-controlled entity in-game.
    It includes methods for setting innate attributes and retrieving stats.
    """
    start_location = "#5"

    def at_object_creation(self):
        """Initialize character attributes at creation."""
        self.db.chinese_name = self.key
        self.db.innate_attributes = {}

    def set_innate_attributes(self, fixed_attr=None, fixed_value=None):
        """Set innate attributes with a total of 80 points across 4 main stats."""
        total_points = 80
        attrs = ["先天臂力", "先天悟性", "先天根骨", "先天身法"]
        if fixed_attr and fixed_value:
            if fixed_attr not in attrs or not (10 <= fixed_value <= 30):
                self.msg("Invalid fixed attribute or value. Using random distribution.")
                fixed_attr = None
                fixed_value = None
            else:
                self.db.innate_attributes[fixed_attr] = fixed_value
                remaining_points = total_points - fixed_value
                remaining_attrs = [attr for attr in attrs if attr != fixed_attr]
                for attr in remaining_attrs[:-1]:
                    max_allowed = min(remaining_points - 20, 30)  # Ensure last attr has at least 10
                    value = random.randint(10, max_allowed)
                    self.db.innate_attributes[attr] = value
                    remaining_points -= value
                self.db.innate_attributes[remaining_attrs[-1]] = remaining_points
        if not fixed_attr:  # Random distribution
            for attr in attrs[:-1]:
                max_allowed = min(total_points - 30, 30)  # Ensure last attr has at least 10
                value = random.randint(10, max_allowed)
                self.db.innate_attributes[attr] = value
                total_points -= value
            self.db.innate_attributes[attrs[-1]] = total_points
        
        # Add hidden attributes
        self.db.innate_attributes["先天福缘"] = random.randint(10, 30)
        self.db.innate_attributes["先天容貌"] = random.randint(10, 30)

    def get_stats(self):
        """Return formatted string of character stats."""
        attrs = self.db.innate_attributes
        return (f"先天臂力: {attrs.get('先天臂力', 0)}\n"
                f"先天悟性: {attrs.get('先天悟性', 0)}\n"
                f"先天根骨: {attrs.get('先天根骨', 0)}\n"
                f"先天身法: {attrs.get('先天身法', 0)}\n"
                f"先天福缘: {attrs.get('先天福缘', 0)}\n"
                f"先天容貌: {attrs.get('先天容貌', 0)}")

class NPC(DefaultCharacter):
    """
    自定义NPC类（需继承自DefaultCharacter）
    """
    def at_object_creation(self):
        """Initialize NPC description."""
        self.db.desc = "一位沉默的NPC"