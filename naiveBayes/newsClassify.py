# load news getter from sklearn.datasets
from sklearn.datasets import fetch_20newsgroups
# download data from Internet
news = fetch_20newsgroups(subset='all')
# inspect data scale and details
print(len(news.data))
print(news.data[0])

# load train_test_split from sklearn
from sklearn.cross_validation import train_test_split
# get test set
X_train, X_test, y_train, y_test = train_test_split(news.data, news.target,
                                                    test_size=0.25, random_state=33)
