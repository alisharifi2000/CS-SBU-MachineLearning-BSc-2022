from enum import Enum, auto
from typing import List
from sklearn import metrics
from sklearn.base import BaseEstimator
from sklearn.model_selection import train_test_split
import pandas as pd


class SelectorType(Enum):
    forward = auto()
    backward = auto()


def sequential_feature_selector(estimator: BaseEstimator,
                                n_features_to_select: int,
                                X: pd.DataFrame,
                                y: pd.Series,
                                direction: SelectorType,
                                scoring: str = "auc") -> List[str]:
    '''
    Adds (forward selection) or removes (backward selection) features to form a feature subset
    in a greedy fashion. At each stage, this estimator chooses the best feature to add or remove
    based on achieved score of an estimator with a particular scoring metric.
    
    Arguments:
    estimator -- an (sklearn) unfitted model. 
    n_features_to_select -- The number of features to select.
    X -- Training vectors.
    y -- Target values.
    direction -- Whether to perform forward selection or backward selection.
    scoring -- A single str which specifies a metric to evaluate the predictions on the test set.

    Returns: 
    selected_features -- a list with the name of the input features.
    '''

    features = X.columns.to_list()
    if direction == SelectorType.forward:
        selected_features = []
        n_iter = n_features_to_select
    elif direction == SelectorType.backward:
        selected_features = X.columns.to_list()
        n_iter = len(X.columns) - n_features_to_select

    for _ in range(n_iter):
        best_score = -1
        best_feature = None
        for feature in features:
            if direction == SelectorType.forward:
                selected_features.append(feature)
            elif direction == SelectorType.backward:
                selected_features.remove(feature)

            X_train, X_test, y_train, y_test = train_test_split(X[selected_features], y, test_size=0.2,
                                                                random_state=42)

            estimator.fit(X_train, y_train)
            predictions = estimator.predict_proba(X_test)[::, 1]
            if scoring == "auc":
                score = metrics.roc_auc_score(y_test, predictions)
            if score > best_score:
                best_feature = feature
                best_score = score

            if direction == SelectorType.forward:
                selected_features.remove(feature)
            elif direction == SelectorType.backward:
                selected_features.append(feature)

        if direction == SelectorType.forward:
            selected_features.append(best_feature)
        elif direction == SelectorType.backward:
            selected_features.remove(best_feature)
        features.remove(best_feature)
        
    return selected_features

