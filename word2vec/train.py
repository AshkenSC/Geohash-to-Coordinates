# 训练模型

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence


inp='processed.txt'
outp1 = 'wiki.zh.text.model'
outp2 = 'wiki.zh.text.vector'
model = Word2Vec(LineSentence(inp), size=200, window=5, min_count=3, workers=4)
model.save(outp1)
model.wv.save_word2vec_format(outp2, binary=False)


# 模型测试

model = Word2Vec.load('wiki.zh.text.model')
# 分布式词向量
print(model.wv['哲学'])
# 测试单词的最近相似单词
print(model.wv.most_similar(['中国']))
# 测试两个单词间的相似度
print(model.wv.similarity('中国', '中华人民共和国'))
print(model.wv.similarity('方针', '民族'))