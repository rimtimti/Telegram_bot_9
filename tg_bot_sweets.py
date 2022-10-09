from config import TOKEN
import logging
import random

from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

number_of_sweets = 0
take_sweets_in_one_move = 0
players = []

NUM_OF_SWEETS, SWEET_IN_MOVE, BOT, GAME = range(4)

def start(update, _):
    global players
    user = update.message.from_user
    players.append(user.first_name)
    update.message.reply_text(
        f'Привет, {user.first_name}!\n'
        'Это игра: на столе лежит заданное в начале игры число конфет больше 2.\n'
        'Играешь ты и бот делая ход друг после друга.\n'
        'Есть умный и не очень бот.\n'
        'Первый ход определяется жеребьёвкой.\n'
        'За один ход можно забрать от 1 и не более чем также заданное вами в начале игры число конфет, но более 1.\n'
        'Тот, кто берет последнюю конфету - проиграл.\n\n'
        'Команда /cancel, чтобы прекратить игру.\n\n'
        'Введите начальное количество конфет больше 2 (целое, положительное): ')
    return NUM_OF_SWEETS

def all_sweets(update, _):
    global number_of_sweets
    text = update.message.text
    if text.isdigit():
        if int(text) <= 2:
            update.message.reply_text('Вы ввели число меньше 3! Попробуй ещё')
            return NUM_OF_SWEETS
        else:
            number_of_sweets = int(text)
    else:
        update.message.reply_text('Неверный ввод числа! Попробуй ещё')
        return NUM_OF_SWEETS

    logger.info("Начальное количество конфет: %s", number_of_sweets)
    update.message.reply_text('Введите число конфет, которое можно брать за один ход, более 1 (целое, положительное): ')
    return SWEET_IN_MOVE

def check_positive_number_less_x_or_y(number: int, num1: int, num2: int)-> int:
    '''
    Проверяет, чтобы начальное число было меньше первого и второго числа
    '''
    if number > num1 or number > num2:
        return False
    else:
        return True

def take_sweets_one_move(update, _):
    global take_sweets_in_one_move
    global number_of_sweets
    text = update.message.text
    if text.isdigit():
        if int(text) <= 1:
            update.message.reply_text('Вы ввели число меньше 2! Попробуй ещё')
            return SWEET_IN_MOVE
        elif check_positive_number_less_x_or_y(int(text), number_of_sweets, number_of_sweets) == False:
            update.message.reply_text('Вы ввели число больше, чем всего есть конфет на столе! Попробуй ещё')
            return SWEET_IN_MOVE
        else:
            take_sweets_in_one_move = int(text)
    else:
        update.message.reply_text('Неверный ввод числа! Попробуй ещё')
        return SWEET_IN_MOVE
    
    logger.info('Количество конфет, которое можно брать за один раз: %s', take_sweets_in_one_move)
    reply_keyboard = [['Простой_бот', 'Умный']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = True)
    update.message.reply_text('Выбери, с кем ты будешь играть.\n\n', reply_markup = markup_key)
    return BOT

def bot(update, _):
    global players
    global take_sweets_in_one_move
    global number_of_sweets

    text = update.message.text
    players.append(text)

    logger.info("Выбран %s.", text)
    i = random.randint(0, 1)
    update.message.reply_text(f'В результате жеребьевки первый ход достается игроку {players [i]}',reply_markup=ReplyKeyboardRemove())
    if players [i] == 'Простой_бот':
        move = random.randint(1, take_sweets_in_one_move)
        update.message.reply_text(f'Игрок {players [1]} забирает {move} конфет.')
        number_of_sweets -= move
        update.message.reply_text(f'Ход достается игроку {players [0]}, осталось {number_of_sweets} конфет.')
    elif players [i] == 'Умный':
        if number_of_sweets % (take_sweets_in_one_move + 1) == 1:
            move = random.randint(1, take_sweets_in_one_move)
        else:
            move = (number_of_sweets - 1) % (take_sweets_in_one_move + 1)
        update.message.reply_text(f'Игрок {players [1]} забирает {move} конфет.')
        number_of_sweets -= move
        update.message.reply_text(f'Ход достается игроку {players [0]}, осталось {number_of_sweets} конфет.')
    
    update.message.reply_text(f'Игрок {players [0]}, сколько конфет вы забираете?: ')
    return GAME

def game(update, _):
    global players
    global take_sweets_in_one_move
    global number_of_sweets

    text = update.message.text
    if text.isdigit():
        if int(text) <= 0:
            update.message.reply_text('Вы ввели число меньше 1! Попробуй ещё')
            return GAME
        elif check_positive_number_less_x_or_y(int(text), take_sweets_in_one_move, number_of_sweets) == False:
            update.message.reply_text('Вы ввели число больше, чем возможно взять! Попробуй ещё')
            return GAME
        else:
            move = int(text)
    else:
        update.message.reply_text('Неверный ввод числа! Попробуй ещё')
        return GAME

    update.message.reply_text(f'Игрок {players [0]} забирает {move} конфет.')
    number_of_sweets -= move
    if number_of_sweets <= 0:
        update.message.reply_text(f'Игрок {players [0]} проиграл.... печалька (\nЧтобы сыграть еще, нажми /start')
        logger.info(f'Игрок {players [0]} проиграл')
        return ConversationHandler.END
    else:
        update.message.reply_text(f'Ход достается игроку {players [1]}, осталось {number_of_sweets} конфет.')
        if players [1] == 'Простой_бот':
            move = random.randint(1, take_sweets_in_one_move)
            update.message.reply_text(f'Игрок {players [1]} забирает {move} конфет.')
            number_of_sweets -= move
            if number_of_sweets <= 0:
                update.message.reply_text(f'Игрок {players [1]} проиграл.... печалька (\nЧтобы сыграть еще, нажми /start')
                logger.info(f'Игрок {players [1]} проиграл')
                return ConversationHandler.END
            else:
                update.message.reply_text(f'Ход достается игроку {players [0]}, осталось {number_of_sweets} конфет.')
        elif players [1] == 'Умный':
            if number_of_sweets % (take_sweets_in_one_move + 1) == 1:
                if number_of_sweets >= take_sweets_in_one_move:
                    move = random.randint(1, take_sweets_in_one_move)
                else:
                    move = random.randint(1, number_of_sweets)
            else:
                move = (number_of_sweets - 1) % (take_sweets_in_one_move + 1)
                update.message.reply_text(f'Игрок {players [1]} забирает {move} конфет.')
                number_of_sweets -= move
                if number_of_sweets <= 0:
                    update.message.reply_text(f'Игрок {players [1]} проиграл.... печалька (\nЧтобы сыграть еще, нажми /start')
                    logger.info(f'Игрок {players [1]} проиграл')
                    return ConversationHandler.END
                else:
                    update.message.reply_text(f'Ход достается игроку {players [0]}, осталось {number_of_sweets} конфет.')
            
        update.message.reply_text(f'Игрок {players [0]}, сколько конфет вы забираете?: ')
        return GAME

def cancel(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s отменил игру.", user.first_name)
    update.message.reply_text('Не хочешь, как хочешь (((' ' Будет скучно - пиши )))', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NUM_OF_SWEETS: [MessageHandler(Filters.text, all_sweets)],
            SWEET_IN_MOVE: [MessageHandler(Filters.text, take_sweets_one_move)], 
            BOT: [MessageHandler(Filters.regex('^(Простой_бот|Умный)$'), bot)],
            GAME: [MessageHandler(Filters.text, game),],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    print('server started')
    updater.start_polling()
    updater.idle()