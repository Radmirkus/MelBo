import configparser



config = configparser.ConfigParser()
config.read("melbo.config")

name = config.get("configuration", "name")
prefix = config.get("configuration", "prefix")
version = config.get("configuration", "version")
chat_list = list(config.get("configuration", "chat_list"))
ignore_users = list(config.get("configuration", "ignore_users"))
testmode = bool(config.get("configuration", "testmode"))
trainmode = bool(config.get("configuration", "trainmode"))
msg_timeout = int(config.get("configuration", "msg_timeout"))
msg_wait = int(config.get("configuration", "msg_wait"))
active_mod_max_time = int(config.get("configuration", "active_mod_max_time"))
access_token = config.get("configuration", "access_token")
app_id = config.get("configuration", "app_id")
my_id = config.get("configuration", "my_id")
api_version = config.get("configuration", "api_version")
