# load digit loader from sklearn datasets
from sklearn.datasets import load_digits
# store digits image data in variable 'digits'
digits = load_digits()
# inspect data size and dimension
print(digits.data.shape)

# handwriting data division
from sklearn.cross_validation import train_test_split
# randomly select 75% of the dataset as training set, the rest as test set
# random_state: the random seed
X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target,
                                                    test_size=0.25, random_state=33)
# inspect training and test set respectively
print(y_train.shape)
print(y_test.shape)

# use SVM to train classifier and identificate
from sklearn.preprocessing import StandardScaler
# load SVM classifier based on linear hypothesis
from sklearn.svm import LinearSVC

# normalize training and test data
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)

# initialize LinearSVC classifier based on SVM
lsvc = LinearSVC()
# train model
lsvc.fit(X_train, y_train)
# predict using trained model
y_predict = lsvc.predict(X_test)