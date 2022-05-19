import matplotlib.pyplot as plt

def states_graph(mean_values:list = None):
    fig, ax = plt.subplots(figsize=(12,6))
    position = [i for i in range(7)]
    ax.plot(position, mean_values, marker='o', markersize=15, linewidth=5)

    # именуем
    ax.set_title('График состояний за неделю')

    # устанавливаем позиции "тиков" на OY и именуем, ограничиваем ось OY
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.set_yticklabels([None, 'Просто ужасно', 'Плохо', 'Пойдет', 'Хорошо', 'Всё отлично'])
    plt.ylim(None, 5.5)

    # то же самое на OX
    ax.set_xticks(position)
    ax.set_xticklabels(['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']) # Даты вмсто дней

    # добавляем сетку
    ax.grid()
    plt.show()

states_graph([2, 3, 4, 5, 2, 3, 5])