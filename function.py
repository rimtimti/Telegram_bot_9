def get_number_natural_int(input_string: str)-> int:
    '''
    Просит у пользователя ввести целое положительное число и проверяет его
    '''
    try:
        number_int = int(input(input_string))
        if number_int <= 0:
            print('Вы ввели отрицательное число или ноль!!!')
            return get_number_natural_int(input_string)
        else:
            return number_int
    except ValueError:
        print('Неверный ввод числа!!!')
        return get_number_natural_int(input_string)