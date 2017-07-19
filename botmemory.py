import configparser
import json



config_path = "melbo.config"
config = configparser.ConfigParser()
config.read(config_path)

name = config.get("optional", "name")
prefix = config.get("optional", "prefix")
version = config.get("optional", "version")
chat_list = json.loads(config.get("optional", "chat_list"))
ignore_users = json.loads(config.get("optional", "ignore_users"))
testmode = config.getboolean("settings", "testmode")
trainmode = config.getboolean("settings", "trainmode")
msg_timeout = config.getint("settings", "msg_timeout")
msg_wait = config.getint("settings", "msg_wait")
active_mod_max_time = config.getint("settings", "active_mod_max_time")
access_token = config.get("private", "access_token")
app_id = config.get("info", "app_id")
my_id = config.get("private", "my_id")
api_version = config.get("info", "api_version")
