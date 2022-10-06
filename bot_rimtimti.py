from controller import button_click
from game import *
from config import TOKEN

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler,)


def start(update, _):
    update.message.reply_text(
        'Привет, это бот, в котором есть калькулятор и игра с конфетами\n\n'
        'Для калькулятора введите через пробел:\n'
        'Рацион числа:\n'
        '/calculator ratio число знак число \n'
        'Компл числа:\n'
        '/calculator compl число знак число \n\n'
        'Команда /game, чтобы поиграть\n'
        'Режим: 1 - другой человек, 2 - бот,\n'
        '3 - умный бот\n'
        '/game [режим] [кол-во конфет] [можно брать за ход]\n'
        'Напрмер: /game 3 10 3\n\n'
        'Команда /cancel, чтобы прекратить.\n')


def calculator(update, _):
    text = update.message.text
    i = text.split()
    i.pop(0)
    a = str(i[0])
    x = str(i[1])
    y = str(i[2])
    z = str(i[3])
    update.message.reply_text(button_click(a, x, y, z))


def game(update, _):
    text = update.message.text
    i = text.split()
    i.pop(0)
    x = int(i[0])
    y = int(i[1])
    z = int(i[2])
    sweets(update, x, y, z)



def cancel(update, _):
    update.message.reply_text(
        'Не хочешь - как хочешь (( \n'
        ' Будет скучно - пиши /start.', 
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


start_handler = CommandHandler('start', start)
calcul = CommandHandler('calculator', calculator)
sweet = CommandHandler('game', game)
exit = MessageHandler(Filters.command, cancel)  # /game


dispatcher.add_handler(start_handler)
dispatcher.add_handler(calcul)
dispatcher.add_handler(sweet)
dispatcher.add_handler(exit)

print('server started')
updater.start_polling()
updater.idle()