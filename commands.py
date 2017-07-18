import botmemory
import vk_module

def do(command):
    if command == '/train on':
        botmemory.trainmode = True
        vk_module.send_output_message('Режим обучения включен')
    elif command == '/train off':
        botmemory.trainmode = False
        vk_module.send_output_message('Режим обучения отключен')
    elif command == '/version':
        vk_module.send_output_message(botmemory.version)
    else:
        vk_module.send_output_message('Комманда не распознана')
