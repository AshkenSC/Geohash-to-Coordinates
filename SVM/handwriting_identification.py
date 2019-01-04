# load digit loader from sklearn datasets
from sklearn.datasets import load_digits
# store digits image data in variable 'digits'
digits = load_digits()
# inspect data size and dimension
print(digits.data.shape)

# handwriting data division
from sklearn.cross_validation import train_test_split
# randomly select 75% of the dataset as training set, the rest as test set
X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target,
                                                    test_size=0.25, random_state=33)

# inspect training and test set respectively
print(y_train.shape)
print(y_test.shape)
