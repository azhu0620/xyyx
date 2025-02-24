import random
from evennia import create_object, utils, CmdSet
from evennia.commands.default.unloggedin import CmdUnconnectedQuit, CmdUnconnectedLook, CmdUnconnectedConnect, CmdUnconnectedCreate
from evennia.commands.default.muxcommand import MuxCommand

# 随机中文名生成器
def generate_random_name():
    surnames = ["张", "李", "王", "赵", "萧", "段", "慕容", "令狐"]
    given_names = ["无忌", "三丰", "翠山", "峰", "冲", "云", "风", "雪"]
    return random.choice(surnames) + random.choice(given_names)

def disconnect_with_timeout(caller, timeout, message):
    """延迟断开连接"""
    def disconnect():
        if not caller.is_authenticated():
            caller.msg(message)
            caller.session.disconnect()
    utils.delay(timeout, disconnect)

class CmdEnterName(MuxCommand):
    """输入英文名字"""
    key = "name"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("请输入您的英文名字：")
            disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")
            return
        name = self.args.strip()
        account = caller.search_account(name)
        if account:
            caller.ndb.login_account = account
            caller.msg("请输入密码：")
            caller.cmdset.add("commands.default_cmdsets.LoginPasswordCmdSet")
            caller.cmdset.remove("commands.default_cmdsets.EnterNameCmdSet")
            disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")
        else:
            caller.ndb.new_account_name = name
            caller.msg(f"使用 {name} 这个名字将会创造一个新的人物，您确定吗(y/n)？")
            caller.cmdset.add("commands.default_cmdsets.CreateConfirmCmdSet")
            caller.cmdset.remove("commands.default_cmdsets.EnterNameCmdSet")
            disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")

class CmdLoginPassword(MuxCommand):
    """输入登录密码"""
    key = "password"

    def func(self):
        caller = self.caller
        if not self.args:
            caller.msg("请输入密码：")
            disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")
            return
        password = self.args.strip()
        account = caller.ndb.login_account
        if account.check_password(password):
            caller.login(account)
            caller.msg("登录成功！欢迎回到江湖！")
            caller.cmdset.remove("commands.default_cmdsets.LoginPasswordCmdSet")
        else:
            caller.msg("密码错误，请重新输入您的英文名字：")
            caller.cmdset.add("commands.default_cmdsets.EnterNameCmdSet")
            caller.cmdset.remove("commands.default_cmdsets.LoginPasswordCmdSet")
            disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")

class CmdCreateConfirm(MuxCommand):
    """确认创建账号"""
    key = "y"

    def func(self):
        caller = self.caller
        caller.msg("现在请您给自己取一个有气质，有个性的名字。\n"
                   "如果您有困难输入中文名字，请直接敲回车键。\n"
                   "请给自己取一个中文名字：")
        caller.cmdset.add("commands.default_cmdsets.CreateNameCmdSet")
        caller.cmdset.remove("commands.default_cmdsets.CreateConfirmCmdSet")
        disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")

class CmdCreateDeny(MuxCommand):
    """拒绝创建账号"""
    key = "n"

    def func(self):
        caller = self.caller
        caller.msg("请输入您的英文名字：")
        caller.cmdset.add("commands.default_cmdsets.EnterNameCmdSet")
        caller.cmdset.remove("commands.default_cmdsets.CreateConfirmCmdSet")
        disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")

class CmdSetName(MuxCommand):
    """设置中文名"""
    key = "name"

    def func(self):
        caller = self.caller
        if not self.args.strip():
            random_name = generate_random_name()
            caller.ndb.temp_name = random_name
            caller.msg(f"看来您要个随机产生的中文名字．．\n"
                       f"请问您是否满意这个中文名字(y/n)？ ──〖 {random_name} 〗：")
            caller.cmdset.add("commands.default_cmdsets.ConfirmNameCmdSet")
            disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")
        else:
            caller.ndb.temp_name = self.args.strip()
            caller.msg("请设定您的密码：")
            caller.cmdset.add("commands.default_cmdsets.SetPasswordCmdSet")
            caller.cmdset.remove("commands.default_cmdsets.CreateNameCmdSet")
            disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")

class CmdConfirmName(MuxCommand):
    """确认随机姓名"""
    key = "y"

    def func(self):
        caller = self.caller
        caller.msg("请设定您的密码：")
        caller.cmdset.add("commands.default_cmdsets.SetPasswordCmdSet")
        caller.cmdset.remove("commands.default_cmdsets.ConfirmNameCmdSet")
        disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")

class CmdDenyName(MuxCommand):
    """拒绝随机姓名"""
    key = "n"

    def func(self):
        caller = self.caller
        caller.msg("请给自己取一个中文名字：")
        caller.cmdset.remove("commands.default_cmdsets.ConfirmNameCmdSet")
        disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")

class CmdSetPassword(MuxCommand):
    """设置密码"""
    key = "password"

    def func(self):
        caller = self.caller
        password = self.args.strip()
        if len(password) < 5:
            caller.msg("密码的长度至少要五个字符，请重设您的密码：")
            return
        caller.ndb.temp_password = password
        caller.msg("请再输入一次您的密码，以确认您没记错：")
        caller.cmdset.add("commands.default_cmdsets.ConfirmPasswordCmdSet")
        caller.cmdset.remove("commands.default_cmdsets.SetPasswordCmdSet")
        disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")

class CmdConfirmPassword(MuxCommand):
    """确认密码"""
    key = "password"

    def func(self):
        caller = self.caller
        if self.args != caller.ndb.temp_password:
            caller.msg("两次密码不一致，请重设您的密码：")
            caller.cmdset.add("commands.default_cmdsets.SetPasswordCmdSet")
            caller.cmdset.remove("commands.default_cmdsets.ConfirmPasswordCmdSet")
            disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")
        else:
            caller.msg("请设定您的身份标识，该标识在您自杀，以及取回密码时使用。不可修改，请谨慎保管：")
            caller.cmdset.add("commands.default_cmdsets.SetIdentifierCmdSet")
            caller.cmdset.remove("commands.default_cmdsets.ConfirmPasswordCmdSet")
            disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")

class CmdSetIdentifier(MuxCommand):
    """设置身份标识"""
    key = "identifier"

    def func(self):
        caller = self.caller
        identifier = self.args.strip()
        if len(identifier) < 9:
            caller.msg("身份标识的长度至少要九个字符，请重设您的身份标识：")
            return
        caller.ndb.temp_identifier = identifier
        caller.msg("请再输入一次您的身份标识，以确认您没记错：")
        caller.cmdset.add("commands.default_cmdsets.ConfirmIdentifierCmdSet")
        caller.cmdset.remove("commands.default_cmdsets.SetIdentifierCmdSet")
        disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")

class CmdConfirmIdentifier(MuxCommand):
    """确认身份标识"""
    key = "identifier"

    def func(self):
        caller = self.caller
        if self.args != caller.ndb.temp_identifier:
            caller.msg("两次身份标识不一致，请重设您的身份标识：")
            caller.cmdset.add("commands.default_cmdsets.SetIdentifierCmdSet")
            caller.cmdset.remove("commands.default_cmdsets.ConfirmIdentifierCmdSet")
            disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")
        else:
            caller.msg(
                """一个人物的天赋对于他或她所修习的武艺息息相关。
人物大多具有以下六项天赋,其中福缘与容貌是隐藏属性：
　　㈠　臂力：影响攻击能力及负荷量的大小。
　　㈡　悟性：影响学习武功秘籍的速度及理解师傅的能力。
　　㈢　根骨：影响体力恢复的速度及升级后所增加的体力。
　　㈣　身法：影响防御及躲避的能力。
　　㈤　福缘：影响解迷、奇遇，拜师等运气方面。
　　㈥  容貌：影响解密，拜师的条件以及玩家和NPC对你的印象。
您可以输入 (1-4) 指定其中的一项值，或者输入 0 由系统随机选择。
您的选择是 (0-4)："""
            )
            caller.cmdset.add("commands.default_cmdsets.SetAttributeCmdSet")
            caller.cmdset.remove("commands.default_cmdsets.ConfirmIdentifierCmdSet")
            disconnect_with_timeout(caller, 300, "您用的时间太久了！")

class CmdSetAttribute(MuxCommand):
    """选择属性分配方式"""
    key = "attribute"

    def func(self):
        caller = self.caller
        choice = self.args.strip()
        if choice not in {"0", "1", "2", "3", "4"}:
            caller.msg("请输入 0-4：")
            disconnect_with_timeout(caller, 300, "您用的时间太久了！")
            return
        caller.ndb.attr_choice = int(choice)
        if choice == "0":
            self.try_attributes(caller)
        else:
            caller.msg("请输入您想要的数值(10-30)：")
            caller.cmdset.add("commands.default_cmdsets.SetAttributeValueCmdSet")
            caller.cmdset.remove("commands.default_cmdsets.SetAttributeCmdSet")
            disconnect_with_timeout(caller, 300, "您用的时间太久了！")

    def try_attributes(self, caller):
        char = caller.ndb.temp_character or create_object("typeclasses.characters.Character", key=caller.ndb.new_account_name)
        caller.ndb.temp_character = char
        attr_map = {1: "先天臂力", 2: "先天悟性", 3: "先天根骨", 4: "先天身法"}
        fixed_attr = attr_map.get(caller.ndb.attr_choice)
        fixed_value = caller.ndb.attr_value if fixed_attr else None
        char.set_innate_attributes(fixed_attr, fixed_value)
        char.db.innate_attributes["先天福缘"] = random.randint(10, 30)
        char.db.innate_attributes["先天容貌"] = random.randint(10, 30)
        attrs = char.db.innate_attributes
        caller.msg(
            f"膂力[{attrs['先天臂力']}]，悟性[{attrs['先天悟性']}]，"
            f"根骨[{attrs['先天根骨']}]，身法[{attrs['先天身法']}]\n"
            "您同意这一组天赋吗(y/n)？"
        )
        caller.cmdset.add("commands.default_cmdsets.ConfirmAttributesCmdSet")

class CmdSetAttributeValue(MuxCommand):
    """设置指定属性值"""
    key = "value"

    def func(self):
        caller = self.caller
        try:
            value = int(self.args.strip())
            if not 10 <= value <= 30:
                caller.msg("数值需在 10-30 之间：")
                disconnect_with_timeout(caller, 300, "您用的时间太久了！")
                return
            caller.ndb.attr_value = value
            CmdSetAttribute().try_attributes(caller)
            caller.cmdset.remove("commands.default_cmdsets.SetAttributeValueCmdSet")
            disconnect_with_timeout(caller, 300, "您用的时间太久了！")
        except ValueError:
            caller.msg("请输入有效数字(10-30)：")
            disconnect_with_timeout(caller, 300, "您用的时间太久了！")

class CmdConfirmAttributes(MuxCommand):
    """确认属性"""
    key = "y"

    def func(self):
        caller = self.caller
        caller.msg("您要扮演男性(m)的角色或女性(f)的角色？")
        caller.cmdset.add("commands.default_cmdsets.SetGenderCmdSet")
        caller.cmdset.remove("commands.default_cmdsets.ConfirmAttributesCmdSet")
        disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")

class CmdDenyAttributes(MuxCommand):
    """拒绝属性"""
    key = "n"

    def func(self):
        caller = self.caller
        CmdSetAttribute().try_attributes(caller)
        caller.cmdset.remove("commands.default_cmdsets.ConfirmAttributesCmdSet")
        disconnect_with_timeout(caller, 300, "您用的时间太久了！")

class CmdSetGender(MuxCommand):
    """设置性别"""
    key = "gender"

    def func(self):
        caller = self.caller
        gender = self.args.strip().lower()
        if gender not in {"m", "f"}:
            caller.msg("请输入 m（男性）或 f（女性）：")
            disconnect_with_timeout(caller, 180, "您三分钟未输入，已断开连接！")
            return
        caller.ndb.gender = "男性" if gender == "m" else "女性"

        # 创建并登录
        account_name = caller.ndb.new_account_name
        password = caller.ndb.temp_password
        identifier = caller.ndb.temp_identifier
        chinese_name = caller.ndb.temp_name
        char = caller.ndb.temp_character

        account = create_object("typeclasses.accounts.Account", key=account_name)
        account.set_password(password)
        account.db.identifier = identifier
        char.db.chinese_name = chinese_name
        char.db.gender = caller.ndb.gender
        char.location = "#5"
        account.characters.add(char)
        caller.login(account)
        caller.msg("角色创建成功！欢迎踏入《夕阳又现》的江湖！")
        caller.cmdset.remove("commands.default_cmdsets.SetGenderCmdSet")

# 定义命令集
class EnterNameCmdSet(CmdSet):
    key = "EnterNameCmdSet"
    def at_cmdset_creation(self):
        self.add(CmdEnterName())

class LoginPasswordCmdSet(CmdSet):
    key = "LoginPasswordCmdSet"
    def at_cmdset_creation(self):
        self.add(CmdLoginPassword())

class CreateConfirmCmdSet(CmdSet):
    key = "CreateConfirmCmdSet"
    def at_cmdset_creation(self):
        self.add(CmdCreateConfirm())
        self.add(CmdCreateDeny())

class CreateNameCmdSet(CmdSet):
    key = "CreateNameCmdSet"
    def at_cmdset_creation(self):
        self.add(CmdSetName())

class ConfirmNameCmdSet(CmdSet):
    key = "ConfirmNameCmdSet"
    def at_cmdset_creation(self):
        self.add(CmdConfirmName())
        self.add(CmdDenyName())

class SetPasswordCmdSet(CmdSet):
    key = "SetPasswordCmdSet"
    def at_cmdset_creation(self):
        self.add(CmdSetPassword())

class ConfirmPasswordCmdSet(CmdSet):
    key = "ConfirmPasswordCmdSet"
    def at_cmdset_creation(self):
        self.add(CmdConfirmPassword())

class SetIdentifierCmdSet(CmdSet):
    key = "SetIdentifierCmdSet"
    def at_cmdset_creation(self):
        self.add(CmdSetIdentifier())

class ConfirmIdentifierCmdSet(CmdSet):
    key = "ConfirmIdentifierCmdSet"
    def at_cmdset_creation(self):
        self.add(CmdConfirmIdentifier())

class SetAttributeCmdSet(CmdSet):
    key = "SetAttributeCmdSet"
    def at_cmdset_creation(self):
        self.add(CmdSetAttribute())

class SetAttributeValueCmdSet(CmdSet):
    key = "SetAttributeValueCmdSet"
    def at_cmdset_creation(self):
        self.add(CmdSetAttributeValue())

class ConfirmAttributesCmdSet(CmdSet):
    key = "ConfirmAttributesCmdSet"
    def at_cmdset_creation(self):
        self.add(CmdConfirmAttributes())
        self.add(CmdDenyAttributes())

class SetGenderCmdSet(CmdSet):
    key = "SetGenderCmdSet"
    def at_cmdset_creation(self):
        self.add(CmdSetGender())

class UnloggedinCmdSet(CmdSet):
    key = "UnloggedinCmdSet"
    def at_cmdset_creation(self):
        self.add(CmdUnconnectedQuit())
        self.add(CmdUnconnectedLook())
        self.add(CmdUnconnectedConnect())
        self.add(CmdUnconnectedCreate())
        self.add(CmdEnterName())
