'''
https://blog.csdn.net/aaalswaaa1/article/details/84778725
'''

import math


def dis(a, b):
    s = 0
    for i in range(len(a)):
        t = a[i] - b[i]
        t = t * t
        s += t
    return math.sqrt(s)


import pickle

inputt = open('./data/myw2v.pkl', 'rb')
wd = pickle.load(inputt)
a = wd['����']
b = wd['��˾']
c = wd['��ҵ']
d = wd['����']
e = wd['֧��']
print(dis(a, b))
print(dis(b, c))
print(dis(e, d))
print(dis(a, e))