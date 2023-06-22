import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from tkinter import *
import os 

# class diagnosor
class Diagnosor:
    DATA_PATH = "DataSet/Training.csv"

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        csv_path = f"{dir_path}/{Diagnosor.DATA_PATH}"
        print("CSV PATH: ", csv_path)

        self.data = pd.read_csv(csv_path).dropna(axis=1)

        # Encoding the target value into numerical
        # value using LabelEncoder
        Encoder = LabelEncoder()
        self.data["prognosis"] = Encoder.fit_transform(self.data["prognosis"])

        # Split the data set into 75:25, 75% for training the models and 25% for testing
        X = self.data.iloc[:, :-1]
        y = self.data.iloc[:, -1]

        # declaring the models
        self.Final_GNB_Pred = GaussianNB()
        self.Final_SVC_Pred = SVC()
        self.Final_RFG_Pred = RandomForestClassifier(random_state=18)

        #fitting the models
        self.Final_GNB_Pred.fit(X, y)
        self.Final_SVC_Pred.fit(X, y)
        self.Final_RFG_Pred.fit(X, y)

        symptoms = X.columns.values

        # Creating a symptom index dictionary to encode the
        # input symptoms into numerical form
        symptom_index = {}
        for index, value in enumerate(symptoms):
            symptom = " ".join([i.capitalize() for i in value.split("_")])
            symptom_index[symptom] = index

        self.data_dict = {
            "symptom_index": symptom_index,
            "predictions_classes": Encoder.classes_
        }


    # getSymptoms function that returns all the symptoms the user chose
    def getSymptoms(self):
        X = self.data.iloc[:, :-1]
        return list(map(lambda i: i.replace('_', ' ').title(), X.columns.values))


    # Defining the Function
    # Input: string containing symptoms separated by commas
    # Output: Generated predictions by models
    def generate(self, inputed_symptoms):

        # creating input data for the models
        input_data = [0] * len(self.data_dict["symptom_index"])
        print(input_data)
        for symptom in inputed_symptoms:
            index = self.data_dict["symptom_index"][symptom]
            print(index)
            input_data[index] = 1



        # reshaping the input data and converting it
        # into suitable format for model predictions
        input_data = np.array(input_data).reshape(1, -1)
        print("### input_data = ", input_data)

        # generating individual outputs
        rf_prediction = self.data_dict["predictions_classes"][self.Final_RFG_Pred.predict(input_data)[0]]
        nb_prediction = self.data_dict["predictions_classes"][self.Final_GNB_Pred.predict(input_data)[0]]
        svm_prediction = self.data_dict["predictions_classes"][self.Final_SVC_Pred.predict(input_data)[0]]


        # making final prediction by taking mode of all predictions
        preds_array = pd.DataFrame([rf_prediction, nb_prediction, svm_prediction])
        final_prediction = preds_array.mode()
        dn = list(map(lambda i: i[0].strip(), final_prediction.values.tolist()))

        predictions = {
            "rf_model_prediction": rf_prediction,
            "naive_bayes_prediction": nb_prediction,
            "svm_model_prediction": svm_prediction,
            "final_prediction": final_prediction.to_json(orient='records'),
            "diseases": dn
        }
        return predictions