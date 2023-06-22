from scipy import stats
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


# class training
class training:
    # Reading the train.csv by removing the
    # last column since it's an empty column
    DATA_PATH = "DataSet/Training.csv"
    data = pd.read_csv(DATA_PATH).dropna(axis=1)

    def __init__(self):
        # Encoding the target value into numerical
        # value using LabelEncoder
        self.Encoder = LabelEncoder()
        self.data["prognosis"] = self.Encoder.fit_transform(self.data["prognosis"])



        # Split the data set into 75:25, 75% for training the models and 25% for testing

        self.X = self.data.iloc[:, :-1]
        self.y = self.data.iloc[:, -1]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
        self.X, self.y, test_size=0.25, random_state=24)



        # Initializing Models
        self.Models = {
            "Gaussian NB": GaussianNB(),
            "Random Forest": RandomForestClassifier(random_state=18),
            "SVC": SVC()
        }



        # Testing of all classifiers together

        self.Final_GNB_Pred = GaussianNB()
        self.Final_SVC_Pred = SVC()
        self.Final_RFG_Pred = RandomForestClassifier(random_state=18)



        # Reading the test data
        test_data = pd.read_csv("./dataset/Testing.csv").dropna(axis=1)
        self.test_X = test_data.iloc[:, :-1]
        self.test_Y = self.Encoder.transform(test_data.iloc[:, -1])


    # calibrate function
    def calibrate(self):
         # Defining scoring metric for k-fold cross validation
        def cv_scoring(estimator, X, y):
            return accuracy_score(y, estimator.predict(X))



        # Checking whether the dataset is balanced or not
        disease_counts = self.data["prognosis"].value_counts()
        temp_df = pd.DataFrame({
            "Disease": disease_counts.index,
            "Counts": disease_counts.values
        })

        plt.figure(figsize=(18, 8))
        sns.barplot(x="Disease", y="Counts", data=temp_df)
        plt.xticks(rotation=90)
        plt.show()



        # Producing cross validation score for the models
        for Names_Models in self.Models:
            Model = self.Models[Names_Models]
            Scores = cross_val_score(Model, self.X, self.y, cv=8,
                                    n_jobs=-1,
                                    scoring=cv_scoring)
            print("==" * 20)
            print(Names_Models)
            print("Scores: ", numpy.array2string(Scores))
            print("Mean Score: ", np.mean(Scores))


        # Training and testing Guassian NB classifier

        dft = GaussianNB()
        dft.fit(self.X_train,self.y_train)
        dft_train_pred = dft.predict(self.X_train)
        dft_test_pred = dft.predict(self.X_test)
        dft_accuracy_training = accuracy_score(self.y_train, dft_train_pred)
        dft_accuracy_testing = accuracy_score(self.y_test, dft_test_pred)

        print("")
        print("")
        print("Accuracy on train data by Guassian NB Classifier: ", dft_accuracy_training*100, "%")
        print("Accuracy on test data by Guassian NB Classifier: ", dft_accuracy_testing*100, "%")

        cf_matrix = confusion_matrix(self.y_test, dft_test_pred)
        plt.figure(figsize=(12,8))
        sns.heatmap(cf_matrix, annot=True)
        plt.title("Confusion Matrix for Guassian NB Classifier on Test Data")
        plt.xlabel("Predicted Label")
        plt.ylabel("True Label")
        plt.show()



        # Training and Testing SVC Classifier
        clf = SVC()
        clf.fit(self.X_train, self.y_train)
        clf_train_pred = clf.predict(self.X_train)
        clf_test_pred = clf.predict(self.X_test)
        clf_accuracy_training = accuracy_score(self.y_train, clf_train_pred)
        clf_accuracy_testing = accuracy_score(self.y_test, clf_test_pred)

        print("")
        print("")
        print("Accuracy on train data by SVM Classifier: ", clf_accuracy_training*100, "%")
        print("Accuracy on test data by SVM Classifier: ", clf_accuracy_testing*100, "%")

        cf_matrix = confusion_matrix(self.y_test, clf_test_pred)
        plt.figure(figsize=(12,8))
        sns.heatmap(cf_matrix, annot=True)
        plt.title("Confusion Matrix for SVM Classifier on Test Data")
        plt.xlabel("Predicted Label")
        plt.ylabel("True Label")
        plt.show()



        # Training and Testing RandomForect Classifier
        hrf = RandomForestClassifier(random_state=18)
        hrf.fit(self.X_train, self.y_train)
        hrf_train_pred = hrf.predict(self.X_train)
        hrf_test_pred = hrf.predict(self.X_test)
        hrf_accuracy_training = accuracy_score(self.y_train, hrf_train_pred)
        hrf_accuracy_testing = accuracy_score(self.y_test, hrf_test_pred)

        print("")
        print("")
        print("Accuracy on train data by RandomForestClassifier: ", hrf_accuracy_training*100, "%")
        print("Accuracy on test data by RandomForestClassifier: ", hrf_accuracy_testing*100, "%")

        cf_matrix = confusion_matrix(self.y_test, hrf_test_pred)
        plt.figure(figsize=(12,8))
        sns.heatmap(cf_matrix, annot=True)
        plt.title("Confusion Matrix for RandomForestClassifier on Test Data")
        plt.xlabel("Predicted Label")
        plt.ylabel("True Label")
        plt.show()



        self.Final_GNB_Pred.fit(self.X, self.y)
        self.Final_SVC_Pred.fit(self.X, self.y)
        self.Final_RFG_Pred.fit(self.X, self.y)



        # Making prediction by take mode of predictions
        # made by all the classifiers
        nbc_pred = self.Final_GNB_Pred.predict(self.test_X)
        svm_pred = self.Final_SVC_Pred.predict(self.test_X)
        rfg_pred = self.Final_RFG_Pred.predict(self.test_X)

        arrays = [
            svm_pred,
            nbc_pred,
            rfg_pred]



        mode = stats.mode(np.stack(arrays), axis=0, keepdims=False)
        result = (mode[0])

        print(result)
        print("")
        print("")
        print("Accuracy on Test dataset by the combined model:", accuracy_score(self.test_Y, result)*100)

        cf_matrix = confusion_matrix(self.test_Y, result)
        plt.figure(figsize=(12, 8))
        sns.heatmap(cf_matrix, annot=True)
        plt.title("Confusion Matrix for Combined Model on Test Dataset")
        plt.xlabel("Predicted Label")
        plt.ylabel("True Label")
        plt.show()
