import configparser
import json



name = 'MelBo'
prefix = ''
version = '1.0.0'
chat_list = ['']
ignore_users = ['']
testmode = False
trainmode = False
msg_timeout = 2
msg_wait = 30
active_mod_max_time = 600
check_birthds = False
birth_msg = "С днем рождения!!!"

access_token = ''
app_id = '5468754'
my_id = ''
api_version = '5.64'

config_path = "melbo.config"
config = configparser.ConfigParser()
config.read(config_path)

try:
    prefix = config.get("optional", "prefix")
    chat_list = json.loads(config.get("optional", "chat_list"))
    ignore_users = json.loads(config.get("optional", "ignore_users"))
    testmode = config.getboolean("settings", "testmode")
    trainmode = config.getboolean("settings", "trainmode")
    msg_timeout = config.getint("settings", "msg_timeout")
    msg_wait = config.getint("settings", "msg_wait")
    active_mod_max_time = config.getint("settings", "active_mod_max_time")
    check_birthds = config.getboolean("settings", "check_birthds")
    birth_msg = config.get("settings", "birth_msg")
    ##access_token = config.get("private", "access_token")
    ##my_id = config.get("private", "my_id")
except ValueError:
    print('Не удалось найти melbo.config')

