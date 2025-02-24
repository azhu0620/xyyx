
r"""
Evennia settings file.
...
"""

from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

SERVERNAME = "夕阳又现"
TIME_ZONE = "Asia/Shanghai"
IN_GAME_ERRORS = True
DEFAULT_HOME = "#5"
START_LOCATION = "#5"
ACCOUNT_TYPECLASS = "typeclasses.accounts.Account"

# 只保留 Telnet 端口 4000
TELNET_PORTS = [4000]  # 确保是整数列表
TELNET_ENABLED = True

# 禁用所有其他服务
WEBSERVER_ENABLED = False
WEBSOCKET_CLIENT_ENABLED = False
SSH_ENABLED = False

# 清空其他端口配置
WEBSERVER_PORTS = []
WEBSOCKET_PORTS = []
SSH_PORTS = []

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
