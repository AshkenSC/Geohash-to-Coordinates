from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence


'''训练模型'''
def train(data):
    inp=data
    outp1 = 'word2vec.model'
    outp2 = 'word2vec.vector'
    model = Word2Vec(LineSentence(inp), size=200, window=5, min_count=3, workers=4)
    model.save(outp1)
    model.wv.save_word2vec_format(outp2, binary=False)


'''模型测试'''
# 模型训练
#train('D:\\Project\\Python\\PythonGadgets\\word_vector\\fasttext\\clean_data.txt')
# 载入模型
model = Word2Vec.load('word2vec.model')
word1 = '电影'
word2 = '电视剧'
word3 = '跑步'

# 分布式词向量
print(word1 + " 的词向量：")
print(model.wv[word1])
# 测试单词的最近相似单词
print("和 " + word1 + " 最相似的词语是：")
print(model.wv.most_similar([word1]))
# 测试两个单词间的相似度
print(word1 + ' 和 ' + word2 + ' 的相似度为：')
print(model.wv.similarity(word1, word2))
print(word1 + ' 和 ' + word3 + ' 的相似度为：')
print(model.wv.similarity(word1, word3))