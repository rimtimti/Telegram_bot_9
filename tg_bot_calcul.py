from config import TOKEN

import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler,)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

calc, number1, sign, number2 = 0, 0, 0, 0

CALC, NUM1, SIGN, NUM2 = range(4)

def get_float_number(text:str) -> float:
    '''
    Возвращает из строки значение float до первого знака, не являющегося числом или первой точкой
    '''
    result = []
    digit = ""
    count = 0
    for symbol in text+' ':
        if symbol.isdigit():
            digit += symbol
        elif symbol == '.' and count == 0:
            digit += symbol
            count += 1
        else:
            if digit:
                result.append(float(digit))
                digit = ""
            result.append(symbol)
    if result[0] == '-':
        result.remove(result[0])
        result = -1*result[0]
    else:
        result = result[0]
    return result

def get_complex_number(text:str) -> complex:
    '''
    Возвращает из строки значение complex до первого знака j
    '''
    result = []
    digit = ""
    count1, count2 = 0, 0
    for symbol in text+' ':
        if symbol.isdigit():
            digit += symbol
        elif symbol == '+' and count1 == 0:
            digit += symbol
            count1 += 1 
        elif symbol == 'j' and count2 == 0:
            digit += symbol
            count2 += 1
        else:
            if digit:
                result.append(complex(digit))
                digit = ""
            result.append(symbol)
    if result[0] == '-':
        result.remove(result[0])
        result = -1*result[0]
    else:
        result = result[0]
    return result


def start(update, _):
    reply_keyboard = [['Рациональные', 'Комплексные']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        'Привет, это бот-калькулятор\n\n'
        'Выбери, какие числа ты хочешь посчитать.\n\n'
        'Команда /cancel, чтобы прекратить.',
        reply_markup=markup_key,)
    return NUM1

def number_one(update, _):
    global calc
    user = update.message.from_user
    logger.info("%s выбрал калькулятор: %s числа.", user.first_name, update.message.text)
    calc = update.message.text
    update.message.reply_text('Введи первое число:\n Рациональные:\n дробные через одну точку (например, -7.45)\n Комплексные вида: 10+5j без пробелов', reply_markup=ReplyKeyboardRemove())
    return SIGN

def signal(update, _):
    global number1
    global calc
    text = update.message.text
    if calc == 'Рациональные':
        for symbol in text:
            if symbol.isalpha():
                update.message.reply_text('Неверный ввод числа! Попробуй ещё')
                return SIGN
        number1 = get_float_number(text)
        update.message.reply_text(f'Принято число: {number1}')
    else:
        for symbol in text:
            if symbol.isalpha() and symbol != 'j':
                update.message.reply_text('Неверный ввод числа! Попробуй ещё')
                return SIGN
        number1 = get_complex_number(text)
        update.message.reply_text(f'Принято число: {number1}')

    update.message.reply_text('Теперь введи знак действия: (+, -, *, /)')
    return NUM2

def number_two(update, _):
    global sign
    text = update.message.text
    if text == '+' or text == '-' or text == '*' or text == '/':
        sign = text
    else:
        update.message.reply_text('такого действия я не знаю! Попробуй ещё')
        return NUM2

    update.message.reply_text('Введи второе число', reply_markup=ReplyKeyboardRemove())
    return CALC

def calcul(update, _):
    global number1
    global calc
    global sign
    global number2
    text = update.message.text
    if calc == 'Рациональные':
        for symbol in text:
            if symbol.isalpha():
                update.message.reply_text('Неверный ввод числа! Попробуй ещё')
                return CALC
        number2 = get_float_number(text)
        update.message.reply_text(f'Принято число: {number2}')
    else:
        for symbol in text:
            if symbol.isalpha() and symbol != 'j':
                update.message.reply_text('Неверный ввод числа! Попробуй ещё')
                return CALC
        number2 = get_complex_number(text)
        update.message.reply_text(f'Принято число: {number2}')

    if sign == '+':
        result = number1 + number2
    if sign == '-':
        result = number1 - number2
    if sign == '*':
        result = number1 * number2
    if sign == '/':
        if number2 == 0:
            result = 'Деление на 0 невозможно!'
            update.message.reply_text(result)
            return ConversationHandler.END
        else:
            result = number1 / number2
    if calc == 'Рациональные':
        result = round(result, 15)
    log = f'{number1} {sign} {number2} = {result}'
    update.message.reply_text(log)
    user = update.message.from_user
    logger.info("%s решил пример: %s", user.first_name, log)
    return ConversationHandler.END

def cancel(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s отменил всё.", user.first_name)
    update.message.reply_text(
        'Не хочешь - как хочешь =(', 
        reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END


if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NUM1: [MessageHandler(Filters.regex('^(Рациональные|Комплексные)$'), number_one)],
            SIGN: [MessageHandler(Filters.text, signal)],
            NUM2: [MessageHandler(Filters.text, number_two)],
            CALC: [MessageHandler(Filters.text, calcul)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )


    dispatcher.add_handler(conv_handler)

    print('server started')
    updater.start_polling()
    updater.idle()
