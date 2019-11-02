from glove import Glove
import numpy as np
from gensim import matutils


'''计算两个词相似度'''
def similarity(w1, w2):
    return np.dot(matutils.unitvec(w1), matutils.unitvec(w2))


'''模型加载'''
gl = Glove.load('glove.model')


'''模型测试'''
word1 = '电影'
word2 = '电视剧'
word3 = '跑步'
vec1 = gl.word_vectors[gl.dictionary[word1]]
vec2 = gl.word_vectors[gl.dictionary[word2]]
vec3 = gl.word_vectors[gl.dictionary[word3]]

# 求词向量
print(word1 + " 的词向量：")
print(gl.word_vectors[gl.dictionary[word1]])
# 求最接近词语
print("和 " + word1 + " 最相似的词语是：")
print(gl.most_similar(word1, number=10))
print(len(vec1))
# 求相似度
print(word1 + ' 和 ' + word2  + ' 的相似度为：')
print(similarity(vec1, vec2))
print(word1 + ' 和 ' + word3  + ' 的相似度为：')
print(similarity(vec1, vec3))




