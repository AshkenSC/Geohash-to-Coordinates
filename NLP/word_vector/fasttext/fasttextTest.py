import fasttext


'''载入模型'''
model = fasttext.load_model('datamodel.model')

'''输出词向量'''
test_word = '中国'
print(test_word + ' 的词向量为：')
print(model.get_word_vector('中国'))
