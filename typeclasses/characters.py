"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia.objects.objects import DefaultCharacter

from .objects import ObjectParent


class Character(ObjectParent, DefaultCharacter):
    start_location = "#5"
    """
    The Character just re-implements some of the Object's methods and hooks
    to represent a Character entity in-game.

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Object child classes like this.

    """

    pass
class NPC(DefaultCharacter):
    """
    自定义NPC类（需继承自DefaultCharacter）
    """
    def at_object_creation(self):
        self.db.desc = "一位沉默的NPC"  # 初始化描述
import random

class Character(DefaultCharacter):
    def at_object_creation(self):
        self.db.chinese_name = self.key
        self.db.innate_attributes = {}

    def set_innate_attributes(self, fixed_attr=None, fixed_value=None):
        total_points = 80
        attrs = ["先天臂力", "先天悟性", "先天根骨", "先天身法"]
        if fixed_attr and fixed_value:
            if fixed_attr not in attrs or not (10 <= fixed_value <= 30):
                return
            self.db.innate_attributes[fixed_attr] = fixed_value
            remaining_points = total_points - fixed_value
            remaining_attrs = [attr for attr in attrs if attr != fixed_attr]
            for attr in remaining_attrs[:-1]:
                max_allowed = min(remaining_points - 20, 40)
                value = random.randint(10, max_allowed)
                self.db.innate_attributes[attr] = value
                remaining_points -= value
            self.db.innate_attributes[remaining_attrs[-1]] = remaining_points
        else:
            for attr in attrs[:-1]:
                max_allowed = min(total_points - 30, 40)
                value = random.randint(10, max_allowed)
                self.db.innate_attributes[attr] = value
                total_points -= value
            self.db.innate_attributes[attrs[-1]] = total_points

    def get_stats(self):
        attrs = self.db.innate_attributes
        return (f"先天臂力: {attrs.get('先天臂力', 0)}\n"
                f"先天悟性: {attrs.get('先天悟性', 0)}\n"
                f"先天根骨: {attrs.get('先天根骨', 0)}\n"
                f"先天身法: {attrs.get('先天身法', 0)}\n"
                f"先天福缘: {attrs.get('先天福缘', 0)}\n"
                f"先天容貌: {attrs.get('先天容貌', 0)}")