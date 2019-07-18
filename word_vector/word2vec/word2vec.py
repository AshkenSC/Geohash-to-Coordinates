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

'''t-SNE降维可视化'''
def plot_tSNE(word_vector, wordlist):
    from sklearn.manifold import TSNE
    import numpy as np
    import matplotlib.pyplot as plt

    tsne = TSNE(n_components=2, random_state=0, n_iter=10000, perplexity=20)
    # 在控制台输出过程中，默认小数会以科学计数法的形式输出，若不需要加上下面这句
    np.set_printoptions(suppress=True)
    T = tsne.fit_transform(word_vector)
    labels = wordlist

    plt.figure(figsize=(14, 10))
    plt.scatter(T[:, 0], T[:, 1], c='blue', edgecolors='k')

    for label, x, y in zip(labels, T[:, 0], T[:, 1]):
        plt.annotate(label, xy=(x + 1, y + 1), xytext=(0, 0), textcoords='offset points')



'''模型测试'''
# 模型训练
#train('D:\\Project\\Python\\PythonGadgets\\word_vector\\fasttext\\clean_data.txt')
# 载入模型
model = Word2Vec.load('wiki.zh.text.model')
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