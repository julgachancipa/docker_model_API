import os
import joblib
import pandas as pd

from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import AdaBoostClassifier
from sklearn import svm

from sklearn.model_selection import cross_val_score

DATA_PATH = 'orders.csv'
CLASSIFIERS = {
    'GaussianNB': GaussianNB(),
    'DecisionTreeClassifier': DecisionTreeClassifier(criterion='entropy', random_state=0),
    'KNeighborsRegressor': KNeighborsRegressor(n_neighbors=1),
    'AdaBoostClassifier': AdaBoostClassifier(n_estimators=100, random_state=0),
    'svm': svm.SVC(),
}


class Modeler:
    def __init__(self):
        self.df = pd.read_csv(DATA_PATH)
        if os.path.exists('trained_models/taken.model'):
            self.model = joblib.load('trained_models/taken.model')
        else:
            self.model = None

    def fit(self, clf='GaussianNB', scores=True):
        self.df['created_at'] = pd.to_datetime(self.df['created_at'])
        self.df['day_of_year'] = self.df['created_at'].dt.dayofyear
        self.df['day_of_week'] = self.df['created_at'].dt.dayofweek
        self.df['minutes'] = self.df['created_at'].dt.hour * 60 + self.df['created_at'].dt.minute

        X, y = self.df.drop(['taken', 'order_id', 'created_at'], axis=1), self.df['taken']

        self.model = CLASSIFIERS[clf].fit(X, y)
        joblib.dump(self.model, 'trained_models/taken.model')

        if scores:
            scores = cross_val_score(CLASSIFIERS[clf], X, y, cv=10, scoring='accuracy')
            print('CLASSIFIER -> ', clf)
            print('Mean: ', scores.mean(), ', STD: ', scores.std())

    def predict(self, orders):
        if not os.path.exists('trained_models/taken.model'):
            raise Exception('Model not trained yet. Call .fit() before making predictions')

        if len(orders) != 7:
            raise Exception(f'Expected store_id, to_user_distance, to_user_elevation, '
                            f'total_earning, day_of_year, day_of_week, minutes, but got {orders}')

        prediction = self.model.predict([orders])

        return int(prediction[0])
