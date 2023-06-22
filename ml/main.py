# Importing libraries

from scipy import stats
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
import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
import calibrate
import diagnose

# NOTE: main.py is practically useless at this time since all the actual fronend code is in app.js
# mainy.py was mainly used when I was still using TKinter and also allows for the classifiers to be retrained

# calibrated = calibrate.training()
# calibrated.calibrate()
diagnostic = diagnose.Diagnosor()


# Creating a window for the GUI's
GUI = tk.Tk()
options = diagnostic.getSymptoms()
font = tkFont.Font(family='Times', size=24)
global num_symptoms
num_symptoms = 1


# Creating a function that prints the generated diagnostic when user clicks "generate"
def print_input():
    global inputed_symptoms
    inputed_symptoms = []
    for i in range(num_symptoms):
        inputed_symptoms.append(symptomClicked[i].get())
    print(inputed_symptoms)
    print(diagnostic.generate(inputed_symptoms))


# Creating a function that adds a drop-down menu when the user clicks "add" button
def add_symptom():
    global num_symptoms
    if num_symptoms < 8:
        num_symptoms += 1

        symptomClicked.append(0)
        symptomMenus.append(0)

        symptomClicked[(num_symptoms - 1)] = StringVar()
        symptomClicked[(num_symptoms - 1)].set("symptom")

        symptomMenus[(num_symptoms - 1)] = ttk.Combobox(GUI, width = 25, textvariable = symptomClicked[(num_symptoms - 1)], font=('Times', 24))
        symptomMenus[(num_symptoms - 1)]["values"] = options

        if (num_symptoms) < 5:
            symptomMenus[(num_symptoms - 1)].grid(row=(num_symptoms - 1), column = 0, padx = 10, pady = 10)
        else:
            symptomMenus[(num_symptoms - 1)].grid(row=(num_symptoms - 5), column = 1, padx = 10, pady = 10)

    else:
        print("Max numer of symptoms have been reached.")


# Creating a function that deletes a drop-down menu when the user clicks "remove" button
def remove_symptom():
    global num_symptoms
    if num_symptoms > 1:
        num_symptoms = (num_symptoms - 1)

        symptomClicked.remove(symptomClicked[num_symptoms])
        symptomMenus[num_symptoms].destroy()
        symptomMenus.remove(symptomMenus[num_symptoms])



GUI.columnconfigure(1, weight=1, minsize=75)
GUI.columnconfigure(2, weight=1, minsize=75)
GUI.rowconfigure(1, weight=1, minsize=50)
GUI.rowconfigure(2, weight=1, minsize=50)
GUI.rowconfigure(3, weight=1, minsize=50)
GUI.rowconfigure(4, weight=1, minsize=50)


# Initializing arrows for the drop-down menu
symptomClicked = [0]

symptomClicked[0] = StringVar()
symptomClicked[0].set("symptom")



symptomMenus = [0]

symptomMenus[0] = ttk.Combobox(GUI, width = 25, textvariable = symptomClicked[0], font=('Times', 24))

symptomMenus[0]["values"] = options

symptomMenus[0].grid(row = 0, column = 0, padx = 10, pady = 10)

symptomMenus[0].current()


# Initializing frames for the drop-down menus and buttons to be in
generate_button_frame = tk.Frame(
        master = GUI,
        relief = tk.RAISED,
        borderwidth = 5
    )

generate_button_frame.grid(row = 3, column = 2, padx = 10, pady = 10)

generate_button = tk.Button(master = generate_button_frame, text = "Generate", font=('Times', 24), command = print_input)

generate_button.pack()



add_button_frame = tk.Frame(
        master = GUI,
        relief = tk.RAISED,
        borderwidth = 5
    )

add_button_frame.grid(row = 1, column = 2, padx = 10, pady = 10)

add_button = tk.Button(master = add_button_frame, text = "Add", font=('Times', 24), command = add_symptom)

add_button.pack()



remove_button_frame = tk.Frame(
        master = GUI,
        relief = tk.RAISED,
        borderwidth = 10,
    )

remove_button_frame.grid(row = 2, column = 2, padx = 10, pady = 10)

remove_button = tk.Button(master = remove_button_frame, text = "remove", font=('Times', 24), command = remove_symptom)

remove_button.pack()



GUI.mainloop()