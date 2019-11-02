from glove import Glove

'''模型加载'''
gl = Glove.load('glove.model')


'''测试：求相似词'''
test_word = '中华人民共和国'
print("和 " + test_word + " 最接近的词语是：")
print(gl.most_similar(test_word, number=10))


'''测试：词向量矩阵'''
print(test_word + " 的词向量矩阵：")
print(gl.word_vectors[gl.dictionary[test_word]])


