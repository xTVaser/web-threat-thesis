print(__doc__)


# Code source: Gaël Varoquaux
# License: BSD 3 clause

import numpy as np
import matplotlib.font_manager
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn import datasets


# Our dataset and targets
# Create Numpy Array

iris = datasets.load_iris()

# figure number
fignum = 1

tuned_parameters = {'gamma': [0.00000000000000000000000000000001, 0.001, 0.0001, 0.01], 'C': [1000, 100, 1000, 1]}
scores = ['precision', 'recall', 'accuracy']

# fit the model
for kernel in ('linear', 'poly', 'rbf'):

    testSVM = GridSearchCV(svm.SVC(C=1, kernel="linear"), tuned_parameters)
    testSVM.fit(iris.data, iris.targets)

    print(testSVM.best_params_)

    # plot the line, the points, and the nearest vectors to the plane
    plt.figure(fignum, figsize=(10, 10))
    plt.clf()

    s = 80
    support_vectors = plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], c="yellow", zorder=20, s=s/2)
    training_vectors = plt.scatter(X[:, 0], X[:, 1], c="black", s=s, zorder=10, cmap=("Oranges"))

    plt.axis('tight')
    x_min = min(X[:, 0]) + min(X[:, 0]) * 0.125
    x_max = max(X[:, 0]) + max(X[:, 0]) * 0.125
    y_min = min(X[:, 1]) + min(X[:, 1]) * 0.125
    y_max = max(X[:, 1]) + max(X[:, 1]) * 0.500

    XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
    Z = clf.decision_function(np.c_[XX.ravel(), YY.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(XX.shape)
    plt.pcolormesh(XX, YY, Z > 0, cmap=("Pastel2"))
    c = plt.contour(XX, YY, Z, colors=['gray', 'black', 'gray'], linestyles=['--', '-', '--'], linewidths=2,
                    levels=[-.5, 0, .5])

    plt.legend([support_vectors, training_vectors],
               ["Support Vectors", "Training Vectors"],
               prop=matplotlib.font_manager.FontProperties(size=16))

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    plt.xticks(())
    plt.yticks(())
    plt.figure(fignum).savefig("test" + str(fignum) + ".png")
    fignum = fignum + 1

    # Testing a single value
    test = np.c_[(1, -1), (-1, 1)]
    result = clf.predict(test)

    print(result)
    print("")


