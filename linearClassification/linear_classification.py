import pandas as pd
import numpy as np

# 创建特征列表
# create characteristic list
column_names = ['Sample code number', 'Clump Thickness', 'Uniformity of Cell Size',
                'Uniformity of Cell Shape', 'Marginal Adhesion', 'Single Epithelial Cell Size',
                'Bare Nuclei', 'Bland Chromatin', 'Normal Nucleoli', 'Mitoses', 'Class']

# 从指定URL导入数据
# load designated data from Internet
data = pd.read_csv(
        'https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data',
        names=column_names)

# 替换原始数据中缺失数据'?'，使用标准缺失值NaN替换
# replace '?' with standard missing value
data = data.replace(to_replace='?', value=np.nan)
# abandon data with missing value (as long as there is one dimension missing)
data = data.dropna(how='any')
# output the amount and dimension of 'data'
data.shape

# 准备训练集和测试集。75%用作训练集，25%用作测试集
# get ready for the training and testing data
# use train_test_split module in sklearn.cross_validation to divide data
from sklearn.cross_validation import train_test_split
# use 25% of data to test, the rest is for training set
X_train, X_test, y_train, y_test = train_test_split(data[column_names[1:10]], data[column_names[10]],
                                                 test_size=0.25, random_state=33)
# 样本集合检查
# sample check
'''
# check distribution of training samples
y_train.value_counts()
# check distribution of testing samples
y_test.value_counts()
'''

# 使用线性回归模型进行预测。导包
# use linear classification model to predict
# load StandardScaler from sklearn.pre-processing
from sklearn.preprocessing import StandardScaler
# load Logistic Regression and SGD classifier from sklearn.linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier

# 将数据标准化
# standardize data to ensure each characteristic is DX = 1, EX = 0.
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)

# 初始化Logistic回归和SGDClassifier
# initialize Logistic Regression and SGDClassifier
lr = LogisticRegression()
sgdc = SGDClassifier()

# 调用Logistic回归中的fit函数以训练模型
# call fit function in LogisticRegression to train model parameter
lr.fit(X_train, y_train)
# use trained model lr to predict X_test
# the result is stored in lr_y_predict
lr_y_predict = lr.predict(X_test)

# 使用Logistic回归内置的score对模型准确性进行评分
from sklearn.metrics import classification_report
# use 'score' in the Logistic Regression model to get accuracy result
# of the model on the test set
print ('Accuracy of LR Classifier:', lr.score(X_test, y_test))
# use classification_report model to get the other 3 results
print(classification_report(y_test, lr_y_predict, target_names=['Benign', 'Malignant']))

# 使用随机梯度下降模型自带的评分函数score获得模型在测试集上的准确性
print('Accuracy of SGD Classifier:', sgdc.score(X_test, y_test))
# 利用classification_report模块活的SGDClassifier其他三个指标的结果
print(classification_report(y_test, sgdc_y_predict, target_names=['Benign', 'Malignant']))

