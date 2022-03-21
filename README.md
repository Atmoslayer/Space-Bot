# Космический Телеграм
Проект позволяет скачивать картинки, публикуемые NASA и SPACEX. 
Затем одна их скачанных картинок публикуется в указываемый телеграмм-канал с задаваемой частотой с помощью бота.
### Как установить
Необходимо получить API токен NASA по данной [ссылке](https://api.nasa.gov). Необходимо указать имя, фамилию, почту, и ссылку,
с которой будет использован токен. После этого будет получен ключ подобный этому: `AbcDhijklmNOPqrstuVWxyzhFlTyudngKrplAwr`.
Так же необходимо создать телеграм-бота с помощью отца ботов @BotFather, написав ему и выбрав имена для бота. 
После этого будет получен токен, подобный этому: `1234567890:ABCDEFGHIjklmnoPqrsStuvwxyzINet1234`.
Затем для бота нужно создать телеграмм-канал и получить его id, подобный этому: `-1234567926589`.
Для хранения токенов в проекте используются переменные окружения. После получения токены необходимо добавить в файл `.env`.
Помимо токенов файл содержит переменную для хренения времени задержки между отправкой картинок в секундах.
Пример заполненного файла:
```
NASA_TOKEN = AbcDhijklmNOPqrstuVWxyzhFlTyudngKrplAwr
TELEGRAM_TOKEN = 1234567890:ABCDEFGHIjklmnoPqrsStuvwxyzINet1234
CHAT_ID = -1234567926589
SLEEP_TIME = 86400
```
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
###Пример запуска
```
>>>C:/Users/atmoslayer/images
```
### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).