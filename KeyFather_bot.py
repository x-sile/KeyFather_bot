
# coding: utf-8

# In[17]:


from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import logging
import time
import random
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(level=logging.INFO, 
                filename='KeyMater_bot.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

good_phrases = ['взял', 'взяла']
check_phrases = ['ключ']
answers_to_cheating = ['Кажется, я уже где-то это слышал...ах да, сегодня уже брали ключ!',
                       'Хм...похоже, что-то сломалось...сегодня уже брали ключ!',
                       'Кажется, у меня дежавю...кто-то уже брал у меня сегодня ключ!',
                       'Боюсь, что у меня нет ключа...видимо, я запамятовал, что уже отдал его сегодня.',
                       'А не ты ли уже брал сегодня ключ?!Если так, то хватит баловаться!!!',
                       'Ключ...ах да, сейчас посмотрю. К сожалению, я не могу его найти. Похоже, я уже отдал его сегодня.']

class TimeKeeper():
    
    def __init__(self):
        self.current_time = time.localtime()
        self.key_taken_time = 'Никогда'
        self.key_status = 0
        
    def reset_key_status(self):
        self.key_status = 0
        return self
                 
    def key_status_change(self, status='взял'):
        
        if status in ['взял', 'взяла'] and (self.key_status == 0):
            self.key_taken_time = self.current_time
            self.key_status = 1
            
        return self    
        

def echo(bot, update):
    sent = update.message.text.strip().lower()
    logging.info(update)
    
    if sent in good_phrases and (tk.key_status == 0):
        answer = 'Спасибо, что взяли ключ!!!' 
    elif sent in good_phrases and (tk.key_status == 1):
        answer = random.choice(answers_to_cheating)
        
    tk.key_status_change(sent)
       
    if sent in check_phrases:
        if tk.key_status == 1:
            answer = 'Вам повезло! Сегодня ключ уже взяли. Можете расслабиться и идти работать.'
        else:
            answer = 'К сожалению, еще никого нет. Придется взять ключ=(.'    
    elif sent not in (good_phrases + check_phrases):
        answer = 'Я Вас не понимаю. Если хотите проверить, взяли ли ключ за Вас, наберите "ключ". Если Вы взяли ключ, наберите "взял(а)", чтобы оповестить других.'
    
    bot.sendMessage(chat_id=update.message.chat_id, text=answer)


if __name__ == '__main__':
    tk = TimeKeeper()
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(tk.reset_key_status, 'cron', day_of_week='mon-sun', hour=0)
    scheduler.start()
    updater = Updater(token='338212089:AAHzQZVLPEWvqfcLuNAH30EpaViFvGdXRbA')
    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()

