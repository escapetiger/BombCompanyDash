import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import matplotlib.pylab as pylab
import time

# Configure visualisations
mpl.style.use('ggplot')
sns.set_style('white')
pylab.rcParams['figure.figsize'] = 12, 8


def plot_correlation_map(df):
    corr = df.corr()
    _, ax = plt.subplots(figsize=(12, 10))
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    _ = sns.heatmap(
        corr,
        cmap=cmap,
        square=True,
        cbar_kws={'shrink': .9},
        ax=ax,
        annot=False,
        # annot_kws = { 'fontsize' : 12 }
    )
    ax.set_title('Correlation map', fontsize=18)
    plt.tick_params(labelsize=14)
    # plt.savefig('correlation_map')


def plot_binary_scatter(ax, x1, x2, y, title):
    blue_patch = mpatches.Patch(color='#0A0AFF', label='Bomb')
    red_patch = mpatches.Patch(color='#AF0000', label='Unlabeled')
    ax.scatter(x1, x2, c=(y == 1), cmap='coolwarm', label='Bomb', marker='o', linewidths=0, s=30, alpha=0.5)
    ax.scatter(x1, x2, c=(y != 1), cmap='coolwarm', label='Unlabeled', marker='.', linewidths=0, s=5, alpha=0.5)

    ax.set_title(title, fontsize=24)
    ax.grid(True)
    ax.legend(handles=[blue_patch, red_patch])


def plot_scores_to_unlabeled_points(x1, x2, c, title, ax=None):
    plt.rcParams['figure.figsize'] = 12, 7
    plt.scatter(
        x1, x2,
        c=c, linewidth=0, s=50, alpha=0.5,
        cmap='jet_r'
    )
    plt.colorbar(label='Scores given to unlabeled points')
    plt.title(title, fontsize=28)
    plt.show()

def plot_confusion_matrix_heatmap(confusion_matrix, ax, title):
    sns.heatmap(confusion_matrix, ax=ax, annot=True, cmap=plt.cm.copper)
    ax.set_title(title, fontsize=24)
    ax.set_xticklabels(['', ''], fontsize=14, rotation=90)
    ax.set_yticklabels(['', ''], fontsize=14, rotation=360)