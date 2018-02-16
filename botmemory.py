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

token_path = "token.st"

try:
    prefix = config.get("optional", "prefix")
    chat_list = json.loads(config.get("optional", "chat_list"))
    ignore_users = json.loads(config.get("optional", "ignore_users"))
    testmode = config.getboolean("settings", "testmode")
    trainmode = config.getboolean("settings", "trainmode")
    msg_timeout = config.getint("settings", "msg_timeout")
    msg_wait = config.getint("settings", "msg_wait")
    active_mod_max_time = config.getint("settings", "active_mod_max_time")
    chatting = config.getboolean("settings", "chatting")
    reposting = config.getboolean("settings", "reposting")
    check_birthds = config.getboolean("settings", "check_birthds")
    birth_msg = config.get("settings", "birth_msg")
except ValueError:
    print('Не удалось найти melbo.config')

with open(token_path, "r") as token_file:
    access_token = token_file.read()
    ##my_id = config.get("private", "my_id")

def save_token(token):
    with open(token_path, 'w') as token_file:
        token_file.write(token)