# Imported Libraries
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
#import tensorflow as tf

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA, TruncatedSVD
import time
from plots import *
import warnings
warnings.filterwarnings("ignore")

def tsne(X,y):
    # T-SNE Implementation
    t0 = time.time()
    X_reduced_tsne = TSNE(n_components=2, random_state=42).fit_transform(X.values)
    t1 = time.time()
    print("T-SNE took {:.2} s".format(t1 - t0))
    plot_scores_to_unlabeled_points(X_reduced_tsne[y==0][:, 0], X_reduced_tsne[y==0][:,1])
def pca(X,y):
    # PCA Implementation
    t0 = time.time()
    X_reduced_pca = PCA(n_components=2, random_state=42).fit_transform(X.values)
    t1 = time.time()
    print("PCA took {:.2} s".format(t1 - t0))
    plot_scores_to_unlabeled_points(X_reduced_pca[y == 0][:, 0], X_reduced_pca[y == 0][:, 1])

def svd():
    # TruncatedSVD
    t0 = time.time()
    X_reduced_svd = TruncatedSVD(n_components=2, algorithm='randomized', random_state=42).fit_transform(X.values)
    t1 = time.time()
    print("Truncated SVD took {:.2} s".format(t1 - t0))
    plot_scores_to_unlabeled_points(X_reduced_svd[y == 0][:, 0], X_reduced_svd[y == 0][:, 1])