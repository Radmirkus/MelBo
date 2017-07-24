import json
import chatbot
import logging
import botmemory

with open('base.json', 'r') as baseRead:
    global base
    baseString = baseRead.read()
    base = json.loads(baseString)


def train(query):
    logging.info("Обучение бота")
    chatbot.send_output_message("Обучение: что ответить?")

    # msg_id_change = 1 if chatbot.channel_id==chatbot.my_id else 2
    if botmemory.testmode:
        chatbot.last_msg_id += 1  # Чтобы не принял свое сообщение за правильный ответ
        nowBotMsg = chatbot.nowBotMsg  # Чтобы не отправил ответ сам себе
        chatbot.nowBotMsg = False if nowBotMsg else True

    trueResponse = chatbot.get_input_message()
    base.append({'q': [query.lower()], 'a': [trueResponse]})

    baseToSave = json.dumps(base, ensure_ascii=False)
    baseToSave = baseToSave.replace('],', '],\n').replace('},', '},\n')  # Чтобы вся база ответов не записывалась в одну строку

    with open('base.json', 'w') as baseWrite:
        baseWrite.write(baseToSave)
    logging.info("Бот запомнил")
