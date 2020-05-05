import networkx as nx
import matplotlib.pyplot as plt
import csv

# DATA_PATH = "C:/Users/Aleksei-DIS/Downloads/res_all/res_all.csv"

def col(y): #Функция показывающая наличие инцидента в сети. Если значение x совпадает с y, то инцидента нет, и наоборот.
    c=(0,0,0)
    x='0' #1#
    if(x==y):
        c=(50/255,205/255,50/255)
    else:
        c=(1,0,0)
    return c


def start(filename: str):
    with open(filename, mode='r') as infile:
        next(infile) #пропуск заголовка
        reader = csv.reader(infile, delimiter=',')     
        count=1
        g=nx.Graph() #объявление графа соединений
        #plt.show()
        for row in reader: #построение графа соединений
            r=row
            g.add_node(r[4])
            g.add_node(r[6])
            g.add_edge(r[6], r[4], color=col(r[12])) #построение соединения. 1 в col стоит как заглушка. туда должен отправляться результат классификации для текущего узла
            if ((count%10)==0): #Обновление графика производится каждые 100 записей
                count+=1
                plt.ion()
                pos = nx.spring_layout(g,k=0.1,iterations=20)
                edges = g.edges()
                colors = [g[u][v]['color'] for u,v in edges]
                nx.draw(g, pos, node_size=25, node_color='limegreen', edges=edges, edge_color=colors)
                plt.pause (5) #Дополнительная задержка для теоретического оператора
                plt.ioff() ###
                plt.clf()
            else:
                count+=1
