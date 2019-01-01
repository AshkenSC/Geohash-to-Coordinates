import pandas as pd
import numpy as np

# create characteristic list
column_names = ['Sample code number', 'Clump Thickness', 'Uniformity of Cell Size',
                'Uniformity of Cell Shape', 'Marginal Adhesion', 'Single Epithelial Cell Size',
                'Bare Nuclei', 'Bland Chromatin', 'Normal Nucleoli', 'Mitoses', 'Class']

# load designated data from Internet
data = pd.read_csv(
        'https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data',
        names=column_names)


# replace '?' with standard missing value
data = data.replace(to_replace='? ', value=np.nan)
# abandon data with missing value (as long as there is one dimension missing)
data = data.dropna(how='any')
# output the amount and dimension of 'data'
data.shape

# get ready for the training and testing data
# use train_test_split module in sklearn.cross_validation to divide data
from sklearn.cross_validation import train_test_split
# use 25% of data to test, the rest is for training set
X_train, X_test, y_train, y_test = train_test_split(data[column_names[1:10]], data[column_names[10]],
                                                    test_size=0.25, random_state=33)
# sample check
'''
# check distribution of training samples
y_train.value_counts()
# check distribution of testing samples
y_test.value_counts()
'''

# use linear classification model to predict
# load StandardScaler from sklearn.preprocessing
from sklearn.preprocessing import StandardScaler
# load Logistic Regression and SGD classifier from sklearn.linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier

# standardize data to ensure each charateristic is DX = 1, EX = 0.
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)
