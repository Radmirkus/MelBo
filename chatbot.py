import json
import random
import bottrainer
import botmemory
import commands
import simplevk
import logging
import time
import getpass

app_id = botmemory.app_id
my_id = botmemory.my_id
access_token = botmemory.access_token
user_id = ''
chat_id = ''
channel_id = ''
channel_type = ''
msg_id = '1'
last_msg_id = '1'  # Присвоено id, чтобы не выдавал ошибку при конвертации в int
active_mod_max_time = botmemory.active_mod_max_time
msg_waiting_break = botmemory.msg_wait  # пауза между запросом новых сообшений
active_mode_timer = active_mod_max_time / botmemory.msg_timeout
v = botmemory.api_version
mode = 'passive'
vk = ""

if botmemory.testmode:
    nowBotMsg = True

logging.basicConfig(format=u' %(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.DEBUG, filename='bot.log')

"""vk = simplevk.vk()
vk.access_token = access_token
vk.v = v
vk.app_id = app_id
while('vk'):
    if access_token!="":
        try:
            vk.user_id = vk.request('users.get')['response'][0]['id']
            print("Успешная авторизация")
            break
        except KeyError:
            print("Возникла ошибка, нужна авторизация")
    try:
        login = input('    Login: ')
        password = getpass.getpass('    Password: ')
        vk.authorize(botmemory.app_id, login, password, 'messages+offline', botmemory.api_version)
    except simplevk.AuthorizationError as autherr:
        print(autherr)
        continue
    if input('    Save password? [y/n]')=="y":
            botmemory.save_token(vk.access_token)
    print('Успешная авторизация')
    break"""

# Подключение базы ответов
def openBaseToRead():
    with open('base.json', 'r') as baseRead:
        global base
        baseString = baseRead.read()
        base = json.loads(baseString)

def chatting():
    logging.info("Получение сообщения...")
    userMsg = get_input_message()
    if userMsg:
        pass
    else:
        return

    logging.info("Сообщение получено: "+userMsg)
    if userMsg.strip().find('/')==0:
        commands.do(userMsg.strip())
        return
    msg_result = send_output_message(botmemory.prefix+getResponse(userMsg))  # Результат отправления сообщения
    logging.info("Ответ отправлен") if len(msg_result)==0 else logging.info("Ответ не отправлен - "+msg_result)
    print(msg_result)  # если сообщение не отправлено, выводит причину

def getResponse(userMsg):
    resVariantes = []  # Варианты ответа
    for pair in base:
        for question in pair['q']:
            if (userMsg.lower()).find(question)>=0:
                resVariantes.append(random.choice(pair['a']))
    if len(resVariantes) > 0:
        return random.choice(resVariantes)
    if botmemory.trainmode:
        bottrainer.train(userMsg)
        return 'Понял!'
    return '...'	

#####

def get_input_message():
    # Определение переменных
    global channel_id
    global msg_id
    global last_msg_id
    global active_mode_timer
    global channel_type

    result = vk.request("messages.get", "out=0&count=1")['response']
    input_message = result['items'][0]['body']
    msg_id = result['items'][0]['id']

    # Проверка новых сообщений
    if (int(msg_id) <= int(last_msg_id)):
        if mode == 'active':
            if active_mode_timer > 0:
                active_mode_timer-=1
            else:
                set_passive_mode()
            logging.info(mode+' '+str(active_mode_timer))
        time.sleep(msg_waiting_break)
        return #get_input_message()
    set_active_mode()
    last_msg_id = msg_id

    # Определение канала
    user_id = result['items'][0]['user_id']
    try:
        chat_id = result['items'][0]['chat_id']
        channel_id = chat_id
        channel_type = 'chat'
    except KeyError:
        channel_id = user_id
        channel_type = 'user'
    logging.info("Открыт канал "+str(channel_id))
    ##print('Сообщение из канала', str(channel_id))
    return input_message.center(len(input_message)+2)  # Вернуть сообщение с пробелами по краям (удобнее читать базу)


def send_output_message(output_message):
    global nowBotMsg
    if not botmemory.testmode:  # Если не тестовый режим
        if (int(channel_id) == int(my_id)):  # преобразуется в int, т.к. при сравнении одинаковых строк выдает False
            return "Нельзя отвечать на свои сообщения"
    if botmemory.testmode and int(channel_id) == int(my_id):
        nowBotMsg = False if nowBotMsg else True  # тернарный оператор (true if is_true else false)
    if botmemory.testmode and int(channel_id) == int(my_id):
        if nowBotMsg:  # Если очередь бота (в тестовом режиме)
            return "Сейчас не очередь бота"

    if channel_type == 'chat':  # Тип канала - чат, входит в список разрешенных
        if str(channel_id) not in botmemory.chat_list:
            return "Чат не входит в список разрешенных"
    if channel_type == 'user':  # Тип канала - пользователь, который не в списке запрещенных
        if str(channel_id) in botmemory.ignore_users:
            return "Пользователь входит в список игнорируемых"
    ##getter_id = "user_id" if channel_type=='user' else "chat_id"
    res = vk.request("messages.send", ("user_id" if channel_type=='user' else "chat_id")+"="+str(channel_id)+"&message="+output_message)['response']
    print('Отправлен ответ в канал '+str(channel_id))
    return ''


def encode_url(msg):
    return str(msg.encode("utf-8")).replace("\\x", "%")[2:-1]


def set_active_mode():
    global msg_waiting_break
    global active_mode_timer
    global mode
    active_mode_timer = active_mod_max_time / botmemory.msg_timeout
    msg_waiting_break = botmemory.msg_timeout
    mode = 'active'
    logging.info('Включен активный режим')  # режим частой проверки сообшений


def set_passive_mode():
    global msg_waiting_break
    global active_mode_timer
    global mode
    msg_waiting_break = botmemory.msg_wait
    mode = 'passive'
    logging.info('Включен пассивный режим')
#####

# Старт
def start(vk_s):
    global vk
    global my_id
    logging.info("!!!Бот запущен")
    vk = vk_s
    my_id = vk.user_id

    get_input_message()  # Получение последнего полученного сообщения, чтобы не ответить на старое сообщение
    set_active_mode()
    while True:
        openBaseToRead()
        chatting()
