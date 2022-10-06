import calculator as calcul

def button_click(name, first_r, sign, second_r):
    '''
    Функция запрашивает данные, решает и выводит
    '''
    if name == 'ratio':
        calcul.init_ratio(first_r, second_r)
    elif name == 'compl':
        calcul.init_compl(first_r, second_r)
    
    if sign == '+':
        result = calcul.sum()
    if sign == '-':
        result = calcul.sub()
    if sign == '*':
        result = calcul.mult()
    if sign == '/':
        result = calcul.div()
    if name == 'ratio':
        result = round(result, 15)
    if result == False:
        result = 'Деление на 0 невозможно!'
    return str(result)
