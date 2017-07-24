import botmemory
import chatbot

def do(command):
    if command == '/train on':
        botmemory.trainmode = True
        chatbot.send_output_message('Режим обучения включен')
    elif command == '/train off':
        botmemory.trainmode = False
        chatbot.send_output_message('Режим обучения отключен')
    elif command == '/version':
        chatbot.send_output_message(botmemory.version)
    else:
        #chatbot.send_output_message('Комманда не распознана')
        return
