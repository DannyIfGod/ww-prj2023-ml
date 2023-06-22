# Importing libraries

import statistics
import scipy
from scipy import stats
from scipy.stats import mode
import numpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

# Reading the train.csv by removing the
# last column since it's an empty column
DATA_PATH = "DataSet/Training.csv"
data = pd.read_csv(DATA_PATH).dropna(axis=1)

# Encoding the target value into numerical
# value using LabelEncoder
Encoder = LabelEncoder()
data["prognosis"] = Encoder.fit_transform(data["prognosis"])

# Split the data set into 75:25, 75% for training the models and 25% for testing

X = data.iloc[:, :-1]
y = data.iloc[:, -1]


Final_GNB_Pred = GaussianNB()
Final_SVC_Pred = SVC()
Final_RFG_Pred = RandomForestClassifier(random_state=18)

Final_GNB_Pred.fit(X, y)
Final_SVC_Pred.fit(X, y)
Final_RFG_Pred.fit(X, y)


symptoms = X.columns.values

# Creating a symptom index dictionary to encode the
# input symptoms into numerical form
symptom_index = {}
for index, value in enumerate(symptoms):
    symptom = " ".join([i.capitalize() for i in value.split("_")])
    symptom_index[symptom] = index

data_dict = {
    "symptom_index": symptom_index,
    "predictions_classes": Encoder.classes_
}


# Defining the Function
# Input: string containing symptoms separated by commas
# Output: Generated predictions by models
def predictDisease(symptoms):
    symptoms = symptoms.split(",")

    # creating input data for the models
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in symptoms:
        index = data_dict["symptom_index"][symptom]
        input_data[index] = 1

    # reshaping the input data and converting it
    # into suitable format for model predictions
    input_data = np.array(input_data).reshape(1, -1)

    # generating individual outputs
    rf_prediction = data_dict["predictions_classes"][Final_RFG_Pred.predict(input_data)[0]]
    nb_prediction = data_dict["predictions_classes"][Final_GNB_Pred.predict(input_data)[0]]
    svm_prediction = data_dict["predictions_classes"][Final_SVC_Pred.predict(input_data)[0]]

    # making final prediction by taking mode of all predictions
    preds_array = pd.DataFrame([rf_prediction, nb_prediction, svm_prediction])
    final_prediction = preds_array.mode()
    predictions = {
        "rf_model_prediction": rf_prediction,
        "naive_bayes_prediction": nb_prediction,
        "svm_model_prediction": svm_prediction,
        "final_prediction": final_prediction
    }
    return predictions



Symptoms = "Itching,Skin Rash"


# Testing the function
print(predictDisease(Symptoms))