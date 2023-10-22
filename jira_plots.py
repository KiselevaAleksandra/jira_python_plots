from my_plot import plots

print(
    'Виды графиков для построения:\n1 - Время, которая задача провела в открытом состоянии\n2 - Распределение времени по заданному состоянию\n3 - Количество заведенных и закрытых задач в день за выбранный период\n4 - Общее количество задач для пользователей, указанных как репортер и исполнитель\n5 - Время, потраченное пользователем на выполнение задач\n6 - Количество задач по степени серьезности\n\n0 - Выход\n')

print('Введите номер графика:')
par = input()

while 1:
    if (par == '1'):
        plots.time_open_plot()
        print('Введите номер графика:')
        par = input()
    elif (par == '2'):
        plots.cond_time_plot()
        print('Введите номер графика:')
        par = input()
    elif (par == '3'):
        plots.count_open_close_plot()
        print('Введите номер графика:')
        par = input()
    elif (par == '4'):
        plots.count_ass_rep_plot()
        print('Введите номер графика:')
        par = input()
    elif (par == '5'):
        plots.time_user_plot()
        print('Введите номер графика:')
        par = input()
    elif (par == '6'):
        plots.count_prior_plot()
        print('Введите номер графика:')
        par = input()
    elif (par == '0'):
        print('Спасибо за использование!')
        exit()
    else:
        print('Введено неверное значение')
        print('Введите номер графика:')
        par = input()
