import tkinter as tk
from tkinter import filedialog
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = None
entry1 = None
canvas1 = None


def getKMeans ():
    global root
    global entry1
    global canvas1
    global df
    global numberOfClusters
    numberOfClusters = int(entry1.get())
    
    kmeans = KMeans(n_clusters=numberOfClusters).fit(df)
    centroids = kmeans.cluster_centers_
    
    label3 = tk.Label(root, text= centroids)
    canvas1.create_window(200, 250, window=label3)
    
    figure1 = plt.Figure(figsize=(4,3), dpi=100)
    ax1 = figure1.add_subplot(111)
    ax1.scatter(df['time interval'], df['login'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
    ax1.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
    scatter1 = FigureCanvasTkAgg(figure1, root) 
    scatter1.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)


def start(source_filename: str):
    global root
    global entry1
    global canvas1
    global df
    global numberOfClusters

    root = tk.Tk()
    canvas1 = tk.Canvas(root, width = 400, height = 300,  relief = 'raised')
    canvas1.pack()

    label1 = tk.Label(root, text='Класстеризация K-means')
    label1.config(font=('helvetica', 14))
    canvas1.create_window(200, 25, window=label1)

    label2 = tk.Label(root, text='Кол-во кластеров:')
    label2.config(font=('helvetica', 8))
    canvas1.create_window(200, 120, window=label2)

    entry1 = tk.Entry (root) 
    canvas1.create_window(200, 140, window=entry1)
    read_file = pd.read_csv (source_filename)
    df = DataFrame(read_file,columns=['time interval','login'])

    processButton = tk.Button(text=' Класстеризация ', command=getKMeans, bg='brown', fg='white', font=('helvetica', 10, 'bold'))
    canvas1.create_window(200, 170, window=processButton)

    root.mainloop()