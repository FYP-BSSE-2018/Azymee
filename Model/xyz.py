from sklearn.tree import DecisionTreeClassifier
import  warnings
warnings.filterwarnings('ignore')
import os
from sklearn import datasets, linear_model, metrics
from sklearn.svm import SVC # "Support vector classifier

import numpy as np

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

from sklearn.naive_bayes import GaussianNB

##Reading data set and seperating independent and dependent variables
data = pd.read_csv("Testing.csv")
df = pd.DataFrame(data)
cols = df.columns
cols = cols[:-1]
x = df[cols]
y = df['prognosis']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)


#Decision Tree ....Calling Classifier and Fitting data for training
dt = DecisionTreeClassifier()
dt.fit(x_train, y_train)



## SVM
classifier = SVC(kernel='linear', random_state=0)
classifier.fit(x_train, y_train)
#Random Forest
rf = RandomForestClassifier(n_estimators=100, criterion = 'gini', max_depth = 6,
                            max_features = 'auto', random_state=0)
rf.fit(x_train, y_train)


#knn
knnclf = KNeighborsClassifier()


# Fitting K-NN to the Training set
knnClassifier = KNeighborsClassifier(n_neighbors = 2)
knnClassifier.fit(x_train, y_train)

#Naive Bayes
gnb = GaussianNB()
gnb.fit(x_train, y_train)



#To create a dictionary from two sequences, use the dict() and zip() so it creates dictionary of symptoms and indices
indices = [i for i in range(132)]
symptoms = df.columns.values[:-1]

dictionary = dict(zip(symptoms,indices))




# Functions

def dosomething(symptom):
    # Getting values from user input
    user_input_symptoms = symptom
    user_input_label = [0 for i in range(132)]
    for i in user_input_symptoms:
        idx = dictionary[i]
        user_input_label[idx] = 1
    # Creating np array
    user_input_label = np.array(user_input_label)
    # Changing 1D array to 2D array
    user_input_label = user_input_label.reshape((-1,1)).transpose()


    # Predicting values
    DecisionTree=dt.predict(user_input_label)


    RandomForest=rf.predict(user_input_label)


    y_pred = knnClassifier.predict(user_input_label)


    Naive = gnb.predict(user_input_label)

    SVM = classifier.predict(user_input_label)
    return(DecisionTree,RandomForest,y_pred,Naive,SVM)




### Predicting Diseases
prediction=(dosomething(['headache','nausea','puffy_face_and_eyes','constipation','skin_rash']))
print("DecisionTree : " ,prediction[0])
print("Random Forest : " ,prediction[1])
print("KNN : " ,prediction[2])
print("Naive: " ,prediction[3])
print("SVM: " ,prediction[4])



