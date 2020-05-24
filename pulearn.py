# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in

# Imported Libraries

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
# import tensorflow as tf
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA, TruncatedSVD
import matplotlib.patches as mpatches
import matplotlib.pylab as pylab
import time

# Classifier Libraries
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import collections

import preprocessing as pp
# from baggingPU import BaggingClassifierPU
from tqdm import trange

# Configure visualisations
mpl.style.use('ggplot')
sns.set_style('white')
pylab.rcParams['figure.figsize'] = 8, 6


def tsne(X):
    """
    T-SNE implementation
    :param X: pandas.DataFrame object
    :return:
    """
    t0 = time.time()
    X_reduced_tsne = TSNE(n_components=2, random_state=42).fit_transform(X.values)
    t1 = time.time()
    print("T-SNE took {:.2} s".format(t1 - t0))

    return X_reduced_tsne


def pca(X):
    """
    PCA implementation
    :param X: pandas.DataFrame object
    :return:
    """
    t0 = time.time()
    X_reduced_pca = PCA(n_components=2, random_state=42).fit_transform(X.values)
    t1 = time.time()
    print("PCA took {:.2} s".format(t1 - t0))
    return X_reduced_pca


def tsvd(X):
    """
    Truncated SVD implementation
    :param X: pandas.DataFrame object
    :return:
    """
    t0 = time.time()
    X_reduced_svd = TruncatedSVD(n_components=2, random_state=42).fit_transform(X.values)
    t1 = time.time()
    print("Truncated SVD took {:.2} s".format(t1 - t0))
    return X_reduced_svd


def plot_binary_scatter(y, X_reduced_pca, X_reduced_svd, X_reduced_tsne):
    """
    Plot binary scatter of binary-class data
    :param y:
    :param X_reduced_pca:
    :param X_reduced_svd:
    :param X_reduced_tsne:
    :return:
    """

    def plotHelper(ax, x1, x2, y, title):
        ax.scatter(x1, x2, c=(y == 1), cmap='coolwarm', label='Bomb', marker='o', linewidths=0, s=30, alpha=0.5)
        ax.scatter(x1, x2, c=(y != 1), cmap='coolwarm', label='Unlabeled', marker='.', linewidths=0, s=5, alpha=0.5)

        ax.set_title(title, fontsize=24)
        ax.grid(True)
        ax.legend(handles=[blue_patch, red_patch])

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(36, 12))
    fig.suptitle('Clusters using Dimensionality Reduction', fontsize=24)
    blue_patch = mpatches.Patch(color='#0A0AFF', label='Bomb')
    red_patch = mpatches.Patch(color='#AF0000', label='Unlabeled')

    # PCA scatter plot
    plotHelper(ax1, X_reduced_pca[:, 0], X_reduced_pca[:, 1], y, 'PCA')

    # Truncated SVD scatter plot
    plotHelper(ax2, X_reduced_svd[:, 0], X_reduced_svd[:, 1], y, 'Truncated SVD')

    # t-SNE scatter plot
    plotHelper(ax3, X_reduced_tsne[:, 0], X_reduced_tsne[:, 1], y, 't-SNE')
    plt.show()


def plot_scores_to_unlabeled_points(ax, x1, x2, c, title):
    plt.rcParams['figure.figsize'] = 12, 7
    ax.scatter(
        x1, x2,
        c=c, linewidth=0, s=50, alpha=0.5,
        cmap='jet_r'
    )
    ax.set_title(title, fontsize=28)


def std_clf(X, y):
    """
    Standard Classifier Method
    """
    y = y.fillna(0)
    #  We'll use a generic random forest
    rf = RandomForestClassifier(
        n_estimators=1000,  # Use 1000 trees
        n_jobs=-1  # Use all CPU cores
    )
    t0 = time.time()
    rf.fit(X, y)
    t1 = time.time()
    print("RandomForestClassifier took {:.2} s".format(t1 - t0))

    scores = rf.predict_proba(X)[:, 1]
    return scores


def PUbagging(X, y):
    """
    PU bagging Method
    """
    y = y.fillna(0)
    # Use 1000 trees
    from sklearn.tree import DecisionTreeClassifier
    from tqdm import trange
    n_estimators = 1000
    estimator = DecisionTreeClassifier()

    # Keep track of the indices of positive and unlabeled data points
    iP = y[y == 1].index
    iU = y[y != 1].index

    # For each data point, keep track of how many times it has been OOB...
    num_oob = pd.DataFrame(np.zeros(shape=y.shape), index=y.index)

    # ...and the sum of its OOB scores
    sum_oob = pd.DataFrame(np.zeros(shape=y.shape), index=y.index)

    for _ in trange(n_estimators):
        # Get a bootstrap sample of unlabeled points for this round
        ib = np.random.choice(iU, replace=True, size=len(iP))

        # Find the OOB data points for this round
        i_oob = list(set(iU) - set(ib))

        # Get the training data (ALL positives and the bootstrap
        # sample of unlabeled points) and build the tree
        Xb = X[y == 1].append(X.loc[ib])
        yb = y[y == 1].append(y.loc[ib])
        estimator.fit(Xb, yb)

        # Record the OOB scores from this round
        sum_oob.loc[i_oob, 0] += estimator.predict_proba(X.loc[i_oob])[:, 1]
        num_oob.loc[i_oob, 0] += 1

    scores = sum_oob / num_oob
    return scores


def two_step(X, y):
    """
    Two-step Method
    """
    y = y.fillna(0)
    ys = 2 * y - 1
    # initialize the classifier
    rf = RandomForestClassifier(
        n_estimators=1000,  # Use 1000 trees
        n_jobs=-1  # Use all CPU cores
    )
    rf.fit(X, y)

    # Get the scores from before
    pred = rf.predict_proba(X)[:, 1]

    # Find the range of scores given to positive data points
    range_P = [min(pred * (ys == 1)), max(pred * (ys == 1))]

    # STEP1
    # If any unlabeled point has a score above or below all known positives, label it accordingly
    iP_new = ys[(ys == -1) & (pred >= range_P[1])].index
    iN_new = ys[(ys == -1) & (pred <= range_P[0])].index
    ys.loc[iP_new] = 1
    ys.loc[iN_new] = 0

    # Classifier to be used for step2
    rf2 = RandomForestClassifier(n_estimators=1000, n_jobs=-1)

    # Limit to 10 iterations(this is arbitrary, but otherwise this approach can take a very long time)
    for i in trange(10):
        # If step 1 didn't find new labels, we're done
        if len(iP_new) + len(iN_new) == 0 and i > 0:
            break
        print('Step 1 labeled %d new positives and %d new negatives.' % (len(iP_new), len(iN_new)))
        print('Doing step 2... ', end='')

        # STEP 2
        rf2.fit(X, ys)
        pred = rf2.predict_proba(X)[:, -1]

        # Find the range of scores given to positive data points
        range_P = [min(pred * (ys > 0)), max(pred * (ys > 0))]

        # Repeat step 1
        iP_new = ys[(ys < 0) & (pred >= range_P[1])].index
        iN_new = ys[(ys < 0) & (pred <= range_P[0])].index
        ys.loc[iP_new] = 1
        ys.loc[iN_new] = 0

    scores = pred

    return scores


def save_reducedX(X_reduced_pca, X_reduced_svd, X_reduced_tsne, filename='reduced_X_train'):
    reduced_X = {
        'tsne': X_reduced_tsne,
        'pca': X_reduced_pca,
        'svd': X_reduced_svd
    }
    try:
        np.save('./data/' + filename + '.npy', reduced_X)
        print('Save reduced X values successfully')
    except Exception:
        print('Fail!')


def read_reduced_data():
    X = np.load('./data/reduced_X_test.npy', allow_pickle=True).item()
    return X


def reduction(X, y):
    X_reduced_tsne = tsne(X)
    X_reduced_pca = pca(X)
    X_reduced_svd = tsvd(X)
    plot_binary_scatter(y, X_reduced_pca, X_reduced_svd, X_reduced_tsne)
    return X_reduced_tsne, X_reduced_pca, X_reduced_svd


def pu_learn(X, y):
    results = pd.DataFrame({
        # The true labels
        'truth': y,
        # The labels to be shown to models in experiment
        'label': y.fillna(0),
    }, columns=['truth', 'label', 'output_std'])

    results['output_std'] = std_clf(X, y)
    results['output_bag'] = PUbagging(X, y)
    results['output_stp'] = two_step(X, y)
    results['output_ave'] = results[[
        'output_std', 'output_bag', 'output_stp'
    ]].mean(axis=1)

    return results


def main(train, test):
    X_train, y_train = train.drop('flag', axis=1), train['flag']
    X_test, y_test = test.drop('flag', axis=1), test['flag']

    # X_reduced_tsne, X_reduced_pca, X_reduced_svd = reduction(X_train, y_train)
    # results = pu_learn(X_train,y_train)
    # results.to_csv('./data/PU_learning_results.csv', encoding='utf_8_sig')


# if __name__ == '__main__':
#     train = pp.preprocessing(train=True, test=False)
#     test = pp.preprocessing(train=False, test=True)
#     # train.to_csv('processed_train.csv', encoding='utf_8_sig')
#     # test.to_csv('processed_test.csv', encoding='utf_8_sig')
#     main(train, test)
