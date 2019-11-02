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
# vectorize text
from sklearn.feature_extraction.text import CountVectorizer
vec = CountVectorizer()
X_train = vec.fit_transform(X_train)
X_test = vec.transform(X_test)

# load Bayes model from sklearn
from sklearn.naive_bayes import MultinomialNB
# load default settings
mnb = MultinomialNB()
# estimate parameter using trained data
mnb.fit(X_train, y_train)
# make prediction on test set
y_predict = mnb.predict(X_test)

# assess performance of naive bayes on news texts
from sklearn.metrics import classification_report
print('The accuracy of Naive Bayes Classifier is', mnb.score(X_test, y_test))
print(classification_report(y_test, y_predict, target_names=news.target_names))
