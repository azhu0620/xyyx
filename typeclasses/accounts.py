from evennia import DefaultAccount

class Account(DefaultAccount):
    def at_account_creation(self):
        print("DEBUG: at_account_creation called")
        self.cmdset.add_default("commands.default_cmdsets.UnloggedinCmdSet", permanent=True)

    def at_connect(self):
        print(f"DEBUG: at_connect called for session {self.session.address}")
        if not self.is_authenticated():
            welcome = (
                "----------------------------------------\n"
                "          欢迎来到《夕阳又现》          \n"
                "----------------------------------------\n"
                "夕阳斜照，江湖波澜再起。刀剑纵横，侠影凌空，\n"
                "只待豪杰仗义而行，谱写武林新篇。\n"
                f"你现在从 {self.session.address} 连线进入。\n"
                "目前共有零位神仙、零位江湖人士在江湖中，以及一位朋友正在步入途中。\n"
                "----------------------------------------\n"
                "请输入您的英文名字："
            )
            self.msg(welcome)
            self.cmdset.remove_default()
            self.cmdset.add("commands.default_cmdsets.EnterNameCmdSet")
        else:
            last = "您尚是第一次进入夕阳又现" if not self.db.last_login else self.db.last_login
            self.msg(f"您上次光临是从：{last}\n"
                     f"您上次连线的时间是：欢迎您成为我们的一员")
            super().at_connect()

    def at_login(self):
        self.db.last_login = self.session.get_connect_time()