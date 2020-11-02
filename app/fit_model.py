import os

from modeler.Modeler import Modeler

"""
Available classifiers:
    'GaussianNB'
    'DecisionTreeClassifier'
    'KNeighborsRegressor'
    'AdaBoostClassifier'
    'svm'
"""
clf = 'GaussianNB'


def fit_model():
    if os.path.exists('trained_models/taken.model'):
        os.remove('trained_models/taken.model')

    m = Modeler()
    m.fit(clf=clf, scores=True)


if __name__ == '__main__':
    fit_model()
