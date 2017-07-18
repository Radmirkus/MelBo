# MelBo

## **MelBo** - автоответчик для Вконтакте.
---
## Проект находится на очень ранней стадии разработки
---
### Подготовка
Для предоставления доступа нужно перейти по [ссылке](https://oauth.vk.com/authorize?client_id=5468754&display=page&redirect_uri=https://vk.com&scope=messages+offline&response_type=token&v=5.64), *access_token* из адресной строки всавить в melbo.config в соответствующее поле.

Также потребуется ввести в поле my_id идентификатор своей страницы вконтакте (id).

В итоге последние строки melbo.config должны выглядеть примерно так:
```
my_id = 1
access_token = 077777764aaaf79e3331fff285cfd0f7cg8dddb93407e5f65c0a7ef49e0f87ce73ac16f233d285111116n
```

Данные неудобства предоставления доступа будут устранены в последующих обновлениях.
---
### Запуск MelBo

Для работы потребуется:
* python версии 3
* библиотеки python (скорее всего они уже установлены):
  * json
  * logging
  * http.client
  * configparser

Запуск через терминал:
```
python3 MelBo.py
```
