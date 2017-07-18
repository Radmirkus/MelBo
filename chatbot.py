import json
import random
import bottrainer
import botmemory
import commands
import vk_module
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.DEBUG, filename='bot.log')

# Подключение базы ответов
def openBaseToRead():
    with open('base.json', 'r') as baseRead:
        global base
        baseString = baseRead.read()
        base = json.loads(baseString)

# Список функций
def chatting():
    logging.info("Получение сообщения...")
    userMsg = vk_module.get_input_message()
    logging.info("Сообщение получено: "+userMsg)
    if userMsg.strip().find('/')==0:
        commands.do(userMsg.strip())
        return
    # дезинформация\ logging.info("Отправление ответа...")
    msg_result = vk_module.send_output_message(botmemory.name+botmemory.prefix+getResponse(userMsg))  # Результат отправления сообщения
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
    return 'Я тебя не совсем понимаю'

# Старт
def start():
    logging.info("!!!Бот запущен")
    vk_module.get_input_message()  # Получение последнего полученного сообщения, чтобы не ответить на старое сообщение
    vk_module.set_passive_mode()
    while True:
        openBaseToRead()
        chatting()
