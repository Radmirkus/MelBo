import http.client
import logging
import json
import time
import botmemory



# logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG, filename='vk_module.log')

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

if botmemory.testmode:
    nowWillBeBotMsg = True


def get_input_message():
    # Определение переменных
    global channel_id
    global msg_id
    global last_msg_id
    global active_mode_timer
    global channel_type

    result = send_request("messages.get", "out=0&count=1", True)
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
        return get_input_message()
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
    print('Сообщение из канала', str(channel_id))
    return input_message.center(len(input_message)+2)  # Вернуть сообщение с пробелами по краям (удобнее читать базу)


def send_output_message(output_message):
    global nowWillBeBotMsg
    if not botmemory.testmode:  # Если не тестовый режим
        if (int(channel_id) == int(my_id)):  # преобразуется в int, т.к. при сравнении одинаковых строк выдает False
            return "Нельзя отвечать на свои сообщения"
    if botmemory.testmode and int(channel_id) == int(my_id):
        nowWillBeBotMsg = False if nowWillBeBotMsg else True  # тернарный оператор (true if is_true else false)
    if botmemory.testmode and int(channel_id) == int(my_id):
        if nowWillBeBotMsg:  # Если очередь бота (в тестовом режиме)
            return "Сейчас не очередь бота"

    if channel_type == 'chat':  # Тип канала - чат, входит в список разрешенных
        if str(channel_id) not in botmemory.chat_list:
            return "Чат не входит в список разрешенных"
    if channel_type == 'user':  # Тип канала - пользователь, который не в списке запрещенных
        if str(channel_id) in botmemory.ignore_users:
            return "Пользователь входит в список запрещенных"
    getter_id = "user_id" if channel_type=='user' else "chat_id"
    res = send_request("messages.send", getter_id+"="+str(channel_id)+"&message="+encode_url(output_message), True)
    print('Ответ отправлен')  # при успешной отправке сообщения
    return ''

def send_request(method, params, need_return):
    vk_connection = http.client.HTTPSConnection("api.vk.com")
    """ Нужно заменять пробелы на '+' в URL
    """
    server_query = ("/method/"+method+"?"+params+"&access_token="+access_token+"&v="+v).replace(" ", "+")
    logging.debug("Запрос: https://api.vk.com"+server_query)
    vk_connection.request("GET", server_query)
    if need_return:
        response = vk_connection.getresponse()
        """ Оставить так, json.loads(response.read().decode("utf-8")) не работает - json.decoder.JSONDecodeError
        """
        decoded_response = response.read().decode("utf-8")
        logging.debug("Ответ сервера на запрос к api: "+decoded_response)
        try:
            json.loads(decoded_response)
        except json.decoder.JSONDecodeError:
            logging.warning("Ответ сервера не в json формате")
        result = json.loads(decoded_response)
        try:
            return result['response']
        except KeyError:
            logging.warning("Не найден ключ 'response' в ответе сервера")
            logging.warning(result['error']['error_msg'])
            time.sleep(msg_waiting_break)
            return send_request(method, params, need_return)


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
    logging.info('Включен пассивный режим')  # режим ожидания сообшений, время проверки новых увеличено
    # active_mode_timer = 600 / botmemory.msg_timeout  # минута
