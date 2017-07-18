import json
import vk_module
import logging
import botmemory

with open('base.json', 'r') as baseRead:
    global base
    baseString = baseRead.read()
    base = json.loads(baseString)


def train(query):
    logging.info("Обучение бота")
    vk_module.send_output_message("Обучение: что ответить?")

    # msg_id_change = 1 if vk_module.channel_id==vk_module.my_id else 2
    if botmemory.testmode:
        vk_module.last_msg_id += 1  # Чтобы не принял свое сообщение за правильный ответ
        nowWillBeBotMsg = vk_module.nowWillBeBotMsg  # Чтобы не отправил ответ сам себе
        vk_module.nowWillBeBotMsg = False if nowWillBeBotMsg else True

    trueResponse = vk_module.get_input_message()
    base.append({'q': [query.lower()], 'a': [trueResponse]})

    baseToSave = json.dumps(base, ensure_ascii=False)
    baseToSave = baseToSave.replace('],', '],\n').replace('},', '},\n')  # Чтобы вся база ответов не записывалась в одну строку

    with open('base.json', 'w') as baseWrite:
        baseWrite.write(baseToSave)
    logging.info("Бот запомнил")
