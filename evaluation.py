from sklearn import metrics
from sklearn.model_selection import cross_val_score, KFold
from scipy.stats import sem
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import numpy as np
import pandas as pd

# Create a confusion matrix
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title, fontsize=14)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def measure_performance(X, y, clf, show_accuracy=True, show_classification_report=False, show_confussion_matrix=False):
    y_pred = clf.predict(X)
    if show_accuracy:
        print('Accuracy: {0:3f}'.format(
            metrics.accuracy_score(y, y_pred)))

    if show_classification_report:
        print('Classification report:')
        print(metrics.classification_report(y, y_pred))

    if show_confussion_matrix:
        cm = metrics.confusion_matrix(y, y_pred)
        labels = ['No Bomb', 'Bomb']
        plot_confusion_matrix(cm, labels, title="Confusion Matrix", cmap=plt.cm.Reds)


def evaluate_cross_validation(clf, X, y, K, scoring='f1'):
    # create a k-fold cross validation iterator
    cv = KFold(K, shuffle=True, random_state=0)
    # by default the score used is the one returned
    #    by score method of the estimator (accuracy)
    scores = cross_val_score(clf, X, y, cv=cv, scoring=scoring)
    # print(scores)
    print("Mean score: {0:.3f} (+/-) {1:.3f})".format(np.mean(scores), sem(scores)))
