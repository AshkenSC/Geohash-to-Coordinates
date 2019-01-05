# load news getter from sklearn.datasets
from sklearn.datasets import fetch_20newsgroups
# download data from Internet
news = fetch_20newsgroups(subset='all')