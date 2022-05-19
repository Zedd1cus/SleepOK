import matplotlib.pyplot as plt

def times_graph(rise_times_in:list, down_times_in:list, goal_times_in:list):

    # переводим значения в числовой вид
    rise_times = [time_translate(i) for i in rise_times_in]
    down_times = [time_translate(i) if time_translate(i) > 8 else time_translate(i)+24for i in down_times_in]
    goal_times = [time_translate(i) for i in goal_times_in]

    #создаем график
    figure, ax = plt.subplots()

    # создаем отметки на оси OX и подписываем их
    position = [i for i in range(7)]
    ax.set_xticks(position)
    ax.set_xticklabels(['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'])

    # создаем отметки на OY и подписываем их, ограничиваем ось до 25 отметок
    base_timestack = [i for i in range(24)]
    addit_timestack = [i for i in range(9)]
    base_timestack.extend(addit_timestack)
    ax.set_yticks([i for i in range(33)])
    ax.set_yticklabels([f'{i}:00' for i in base_timestack])
    plt.ylim(5, 25)

    # строим сами графики
    ax.plot(rise_times, label='Вставал', color='g', marker='o')
    ax.plot(down_times, label='Ложился', color='b', marker='o')
    ax.plot([goal_times[0]]*7, label='Нужно вставать', color='k')
    ax.plot([goal_times[1]]*7, label='Нужно ложиться', color='k')

    plt.show()

def time_translate(time):
    hours, minuts = tuple(int(i) for i in time.split(':'))
    fract = minuts/60
    result = float(hours) + fract
    return result

times_graph(['7:00', '7:30', '8:00', '8:30', '7:40', '7:50', '7:40'], ['23:00', '22:30', '23:30', '22:45', '22:50', '23:40', '23:40'], ['7:00', '22:30'])