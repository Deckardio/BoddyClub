"k-means"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


import seaborn as sns
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.cluster import AgglomerativeClustering


def start(filename: str):
    if isinstance(filename, str) is False:
        raise Exception("fock u!")
    df = pd.read_csv(filename, 
        dtype={
            "begin": int, 
            "end": int,
            "time interval": int,
            "login": int,
            "mac ab": str,
            "ULSK1": str,
            "BRAS ip": str,
            "start count": int,
            "alive count": int,
            "stop count": int,
            "incoming": int,
            "outcoming": int,
            "error_count": int,
            "code 0": int,
            "code 1011": int,
            "code 1100": int,
            "code -3": int,
            "code -52": int,
            "code -42": int,
            "code -21": int,
            "code -40": int,
            "code -44": int,
            "code -46": int,
            "code -38": int
            })
    df.head()

    sample_df = df
    sample_df.shape

    df1 = sample_df.drop(columns =[
        "code 0",
        "code 1011",
        "code 1100",
        "code -3",
        "code -52",
        "code -42",
        "code -21",
        "code -40",
        "code -44",
        "code -46",
        "code -38",
        "mac ab",
        "ULSK1",
        "BRAS ip"
    ])
    print(df1.columns)
    cols_of_interest = [
        'begin',
        'end',
        'time interval',
        'incoming',
        'outcoming'
        ]

    data = df1[cols_of_interest]

    X = StandardScaler().fit_transform(data)
    print(X)

    n_clusters= 12
    #Set number of clusters at initialisation time
    k_means = KMeans(n_clusters=12)
    #Run the clustering algorithm
    model = k_means.fit(X)
    #Generate cluster predictions and store in y_hat
    y_hat = k_means.predict(X)

    from sklearn import metrics
    labels = k_means.labels_
    metrics.silhouette_score(X, labels, metric = 'euclidean')

    metrics.calinski_harabasz_score(X, labels)
    """
    k_means_8 = KMeans(n_clusters=8)
    model = k_means_8.fit(X)
    y_hat_8 = k_means_8.predict(X)

    labels_8 = k_means_8.labels_
    metrics.silhouette_score(X, labels_8, metric = 'euclidean')

    metrics.calinski_harabasz_score(X, labels_8)
    """
    #for each value of k, we can initialise k_means and use inertia to identify the sum of squared distances of samples to the nearest cluster centre
    sum_of_squared_distances = []
    K = range(1,15)
    for k in K:
        k_means = KMeans(n_clusters=k)
        model = k_means.fit(X)
        sum_of_squared_distances.append(k_means.inertia_)

    plt.plot(K, sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('sum_of_squared_distances')
    plt.title('elbow method for optimal k')
    plt.show()