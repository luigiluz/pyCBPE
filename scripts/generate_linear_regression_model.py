""" This script is responsible for generating the machine learning model
that is going to be used to predict continuous blood pressure."""

# Libraries
from sklearn.model_selection import train_test_split
import sklearn.preprocessing
from sklearn import linear_model
import os

# Package
import pyCBPE.dataset
import pyCBPE.model
import pyCBPE.constants as consts
import pyCBPE.metrics

def main():
    print("##### Continuous Blood Pressure Estimation Framework #####")
    print("### Model generator script ###")

    features_and_labels_df = pyCBPE.dataset.load()

    features_and_labels_df = pyCBPE.dataset.handle(features_and_labels_df)
    features_and_labels_df = pyCBPE.dataset.remove_outliers(features_and_labels_df)

    features_array = pyCBPE.dataset.get_features_as_array(features_and_labels_df)
    scaled_features_array = sklearn.preprocessing.scale(features_array)
    labels_array = pyCBPE.dataset.get_labels_as_array(features_and_labels_df)

    X_train, X_test, y_train, y_test = train_test_split(scaled_features_array, labels_array, test_size=0.2, random_state=42)

    MODEL_NAME = "LiR"
    model = linear_model.LinearRegression()
    parameters = {}

    best_model = pyCBPE.model.train_regression(MODEL_NAME, model, parameters, X_train, y_train)
    y_pred = best_model.predict(X_test)

    all_metrics, stats_metrics, bhs_metrics, aami_metrics = pyCBPE.metrics.evaluate(MODEL_NAME, y_test, y_pred)

    # Export the best estimator
    MODEL_FOLDER_OUTPUT_PATH = consts.ROOT_PATH + "/files/estimators/" + MODEL_NAME + "/"
    MODEL_JOBLIB_FILENAME = MODEL_NAME + ".joblib"

    os.mkdir(MODEL_FOLDER_OUTPUT_PATH)

    pyCBPE.model.save_estimator(best_model, MODEL_FOLDER_OUTPUT_PATH + MODEL_JOBLIB_FILENAME)
    # Export the generated metrics
    all_metrics.to_csv(MODEL_FOLDER_OUTPUT_PATH + consts.ALL_METRICS_FILENAME, index=False)
    stats_metrics.to_csv(MODEL_FOLDER_OUTPUT_PATH + consts.STATS_METRICS_FILENAME, index=False)
    bhs_metrics.to_csv(MODEL_FOLDER_OUTPUT_PATH + consts.BHS_METRICS_FILENAME, index=False)
    aami_metrics.to_csv(MODEL_FOLDER_OUTPUT_PATH + consts.AAMI_METRICS_FILENAME, index=False)


if __name__ == "__main__":
    main()
