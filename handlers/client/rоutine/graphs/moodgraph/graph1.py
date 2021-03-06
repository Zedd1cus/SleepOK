import matplotlib.pyplot as plt
import os

async def states_graph(mean_values:list = None):
    fig, ax = plt.subplots(figsize=(12,6))
    position = [i for i in range(7)]
    ax.plot(position, mean_values, marker='o', markersize=15, linewidth=5)

    # именуем

    # устанавливаем позиции "тиков" на OY и именуем, ограничиваем ось OY
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.set_yticklabels([None, 'Плохо', 'Ниже среднего', 'Средне', 'Выше среднего', 'Отлично'])
    plt.ylim(None, 5.5)

    # то же самое на OX
    ax.set_xticks(position)
    ax.set_xticklabels(['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']) # Даты вмсто дней

    # добавляем сетку
    ax.grid()

    return fig, ax
