""" This is the package responsible for training the regression model."""

import joblib
import numpy as np
from sklearn.metrics import make_scorer
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV

def train_regression(model_name, estimator, parameters, X_train, y_train):
    rmse_scorer = make_scorer(_root_mean_squared_error, greater_is_better=False)

    k = 10 # Number of folds for cross validation
    grid_search_cv = GridSearchCV(estimator, parameters, cv=k, verbose=2, scoring=rmse_scorer, n_jobs=-1)
    grid_search_cv.fit(X_train, y_train)

    best_estimator = grid_search_cv.best_estimator_

    return best_estimator


def save_estimator(estimator, estimator_path):
    joblib.dump(estimator, estimator_path)
    print("Estimator properly saved.") # TO DO: Add a more descriptive message


def load_estimator(estimator_path):
    estimator = joblib.load(estimator_path)
    print("Estimator properly loaded.")

    return estimator


def _root_mean_squared_error(y_true, y_pred):
    ''' Root mean squared error regression loss

    Parameters
    ----------
    y_true : array-like of shape = (n_samples) or (n_samples, n_outputs)
    Ground truth (correct) target values.

    y_pred : array-like of shape = (n_samples) or (n_samples, n_outputs)
    Estimated target values.
    '''
    return np.sqrt(mean_squared_error(y_true, y_pred))
