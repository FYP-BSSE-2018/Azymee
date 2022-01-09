# Importing the libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculati
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report , confusion_matrix
# Importing the dataset
data = pd.read_csv("Testing.csv")
df = pd.DataFrame(data)
cols = df.columns
cols = cols[:-1]
X = df[cols]
y = df['prognosis']
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
# Adjusting development threshold
tree = DecisionTreeClassifier()
X_train,X_test,y_train,y_test = train_test_split(X, y, random_state=42)
tree.fit(X_train, y_train)

# Predicting the Test set results
y_pred = tree.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# Making the Confusion Matrix



