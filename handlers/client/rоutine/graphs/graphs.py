from handlers.client.rоutine.graphs.moodgraph import graph1
from handlers.client.rоutine.graphs.timesgraph import graph2
import matplotlib as plt

def get_graphs():
    # data1 = get_graph1_data()
    # data2 = get_hraph2_data()
    fig1, ax1 = graph1.states_graph()
    fig2, ax2 = graph1.states_graph()
    plt.show()

get_graphs()