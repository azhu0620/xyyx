from evennia.objects.objects import DefaultRoom
from .objects import ObjectParent

class Room(ObjectParent, DefaultRoom):
    def return_appearance(self, looker):
        # 只获取房间的基本描述，不包含默认的 Characters 等内容
        desc = self.get_display_name(looker) + "\n"
        if self.db.desc:
            desc += self.db.desc

        # 获取房间内的所有物体
        contents = self.contents
        if not contents:
            return desc

        # 分离玩家（排除自己）、NPC和物品
        players = [obj for obj in contents if obj.has_account and obj != looker]  # 排除 looker
        npcs = [obj for obj in contents if obj.typeclass_path.endswith("NPC") and not obj.has_account]
        items = [obj for obj in contents if not obj.has_account and not obj.typeclass_path.endswith("NPC")]

        # 构建新的显示内容
        visible = []
        # 处理其他玩家
        for player in players:
            chinese_name = player.db.chinese_name or player.aliases.get("中文名") or "未知"
            english_id = player.key
            visible.append(f"Player {chinese_name}({english_id})")
        # 处理NPC
        for npc in npcs:
            chinese_name = npc.db.chinese_name or npc.aliases.get("中文名") or "未知"
            english_id = npc.key
            visible.append(f"Npc {chinese_name}({english_id})")
        # 处理物品
        for item in items:
            chinese_name = item.db.chinese_name or item.aliases.get("中文名") or "未知"
            english_id = item.key
            visible.append(f"{chinese_name}（{english_id}）")

        # 将新内容插入描述
        if visible:
            desc += "\n这里有：\n  " + "\n  ".join(visible)
        return desc
