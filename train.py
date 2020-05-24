import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import time
import joblib
# Classifier Libraries
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV

from preprocessing import preprocessing


def log_reg_train(X_train, y_train):
    y_train[PU_results.truth != 1] = np.where(PU_results.output_ave > 0.2, 1, 0)

    sampleweights = np.where(PU_results.truth == 1, 1, 0.01)
    t0 = time.time()
    log_reg_params = {'C': range(50, 150, 20)}

    grid_log_reg = GridSearchCV(LogisticRegression(class_weight=sampleweights), log_reg_params)
    grid_log_reg.fit(X_train, y_train)
    # We automatically get the logistic regression with the best parameters.
    log_reg = grid_log_reg.best_estimator_
    t1 = time.time()
    print('Logistic Regression takes {:2f} s for best paramter'.format(t1 - t0))
    return log_reg


def gbc_train(X_train, y_train):
    t0 = time.time()
    sampleweights = np.where(PU_results.truth == 1, 1, 0.55)
    gbc = GradientBoostingClassifier(max_depth=15, min_samples_leaf=5, min_samples_split=9, n_estimators=150,
                                     max_features=11, min_impurity_decrease=0.01)
    gbc.fit(X_train, y_train, sample_weight=sampleweights)
    t1 = time.time()
    print('GradientBoostingClaissifer takes {:2f} s for fitting'.format(t1 - t0))
    return gbc


def svc_train(X_train, y_train):
    # SVM
    y_train[PU_results.truth != 1] = np.where(PU_results.output_bag > 0.9, 1, 0)
    t0 = time.time()
    svc = SVC(kernel='rbf', C=100, )
    svc.fit(X_train, y_train)
    t1 = time.time()
    print('SVM takes {:2f} s for best paramter'.format(t1 - t0))


def plot_correlation_map(df, annot=False):
    corr = df.corr()
    _, ax = plt.subplots(figsize=(12, 10))
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    _ = sns.heatmap(
        corr,
        cmap=cmap,
        square=True,
        cbar=True,
        cbar_kws={'shrink': .9},
        ax=ax,
        annot=annot,
        annot_kws={'fontsize': 12}
    )
    ax.set_title('Correlation map', fontsize=18)
    plt.tick_params(labelsize=14)
    plt.savefig('correlation_map.png')
    plt.show()


def plot_label_dist(y):
    sns.countplot(y)
    plt.title('Class Distributions \n (0: No Bomb || 1: Bomb)', fontsize=14);
    plt.show()


def set_new_pos_samples(res, y):
    new_Pnum = sum(res[res.truth != 1].output_bag > 0.9)
    y[res.truth != 1] = np.where(res.out_bag > 0.9, 1, 0)
    print('origin positive samples: %d \nnew positive samples: %d' % (len(res[res.truth == 1]), new_Pnum))
    return y


if __name__ == '__main__':
    try:
        train = pd.read_csv('./data/processed_train.csv')
        test = pd.read_csv('./data/processed_test.csv')
    except Exception:
        train = preprocessing(train=True, test=False)
        test = preprocessing(train=False, test=True)

    if test.flag.isnull().sum() > 0:
        test.flag.fillna(0, inplace=True)
    PU_results = pd.read_csv('./data/PU_learning_results.csv', index_col=0)

    X_train, y_train = train.drop('flag', axis=1), train['flag']
    X_test, y_test = test.drop('flag', axis=1), test['flag']

    # gbc = joblib.load('./models/gbc.m')
    # svc = joblib.load('./models/svc.m')
    # log_reg = joblib.load('./models/log_reg.m')




