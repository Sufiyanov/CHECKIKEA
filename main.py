from urllib.request import Request, urlopen
from threading import Thread
import time
import telebot


TOKEN = '5597549677:AAGUpfXnvhrJ_HllAQqZ8U8zKvII5YndNOE'
TRACKED_PAGE = 'http://192.168.56.102/index.html'

bot = telebot.TeleBot(TOKEN)

#Преводит страницу в списочный тип 
def get_current_html(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    data = webpage.decode("utf8").split()
    return data    

#Отправка уведомлений
def sending_notifications(text, file):
    f = open(file, 'r')
    datafile = f.readlines()
    for i in datafile:
        bot.send_message(i, text)
    f.close()
    return 'Рассылка выполнена'

#Проверка страницы на изменение 
def check_page():
    original_page = get_current_html(TRACKED_PAGE)

    while True:
        actual_page = get_current_html(TRACKED_PAGE)
        if original_page != actual_page:
            print('Страница поменялась')
            print(sending_notifications('Страница поменялась', 'users.txt'))
            break
        else:
            time.sleep(100) 

#Добавление пользователей в базу (текстовый файл)
@bot.message_handler(commands=['start'])
def start_message(message):
    print('вошел', message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    bot.send_message(message.chat.id, f'начал отслеживание, если страница изменится сообщу {TRACKED_PAGE}')
    f = open('users.txt', 'a')
    f.write(str(message.chat.id) + '\n')
    f.close()

#Включение в поток проверки страницы
t1 = Thread(target = check_page, args =())
t1.start()


bot.infinity_polling()           


