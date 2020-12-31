""" This script is responsible for generating the machine learning model
that is going to be used to predict continuous blood pressure."""

# Libraries
from sklearn.model_selection import train_test_split
import sklearn.preprocessing
from sklearn import linear_model

# Package
import dataset
import model
import constants as consts

def main():
    print("##### Continuous Blood Pressure Estimation Framework #####")
    print("### Model generator script ###")

    features_and_labels_df = dataset.load(consts.ROOT_PATH + consts.OUTPUT_PATH)
    features_and_labels_df = dataset.handle(features_and_labels_df)

    features_array = dataset.get_features_as_array(features_and_labels_df)
    scaled_features_array = sklearn.preprocessing.scale(features_array)
    labels_array = dataset.get_labels_as_array(features_and_labels_df)

    X_train, X_test, y_train, y_test = train_test_split(scaled_features_array, labels_array, test_size=0.1, random_state=42)

    lr_model = linear_model.LinearRegression()
    parameters = {
                    'fit_intercept' : (True, False),
                    'normalize' : (True, False)
                }

    best_lr_model = model.train_regression("LiR", lr_model, parameters, X_train, y_train)

    model.save_estimator(best_lr_model, consts.ROOT_PATH + consts.LINEAR_REGRESSOR_OUTPUT_PATH)


if __name__ == "__main__":
    main()
