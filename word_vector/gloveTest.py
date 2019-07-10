from __future__ import print_function
import argparse
import pprint
import gensim
from glove import Glove
from glove import Corpus

'''数据集导入'''
# 将文本行存入列表
i = 1
lines = []
for line in open("test.txt", encoding='utf-8'):
    lines.append(line)
    print("appending line " + str(i))
    i += 1

# 准备数据集
corpus_model = Corpus()
corpus_model.fit(lines, window=10)
#corpus_model.save('corpus.model')
print('Dictionary size: %s' % len(corpus_model.dictionary))
print('Collocations: %s' % corpus_model.matrix.nnz)


'''训练模型'''
gl = Glove(no_components=100, learning_rate=0.05)
gl.fit(corpus_model.matrix, epochs=10,
          no_threads=1, verbose=True)
gl.add_dictionary(corpus_model.dictionary)


'''模型保存与加载'''
gl.save('glove.model')
gl = Glove.load('glove.model')


'''测试：求相似词'''
print(gl.most_similar('中国', number=10))

