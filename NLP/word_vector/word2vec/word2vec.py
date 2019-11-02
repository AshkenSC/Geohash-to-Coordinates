from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt


'''训练模型'''
def train(data):
    inp=data
    outp1 = 'abc_news200.model'
    outp2 = 'abc_data200.vector'
    print('Loading data...\n')
    model = Word2Vec(LineSentence(inp), size=200, window=5, min_count=5, workers=4)
    print('Finished data loading.\n')
    model.save(outp1)
    print('The model has been saved.\n')
    model.wv.save_word2vec_format(outp2, binary=False)

'''导入指定词及其相似词的词向量'''
def load_similar_vectors(keyword, topnumber, wordlist, vectorlist, model):
    i = 1
    for member in model.wv.most_similar(keyword, topn=topnumber):
        # most_similar返回一个列表，列表元素为二元组
        # 二元组第一个元素为最相近词条，第二个元素为相似度
        wordlist.append(member[0])
        vectorlist.append(model.wv[member[0]])
        print('The word vector of ' + str(i) + ' has been appended.')
        i += 1
    print('Similar words of ' + keyword + ' have been loaded.')

'''t-SNE降维可视化'''
def plot_tSNE(word_vector, wordlist, dot_color):
    # 支持中文
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    tsne = TSNE(n_components=2, random_state=0, n_iter=300, perplexity=20)
    # 在控制台输出过程中，默认小数会以科学计数法的形式输出，若不需要，可加上下面这句
    np.set_printoptions(suppress=True)
    T = tsne.fit_transform(word_vector)
    labels = wordlist

    print('Data loading complete. Plotting...')

    plt.figure(figsize=(14, 10))
    plt.scatter(T[:, 0], T[:, 1], color=dot_color)

    # 为数据点添加标签
    for label, x, y in zip(labels, T[:, 0], T[:, 1]):
        plt.annotate(label, xy=(x + 1, y + 1), xytext=(0, 0), textcoords='offset points')
    #    plt.annotate(label, xy=(x + 1, y + 1), xytext=(0, 0))


'''模型测试'''
# 模型训练
#train('D:\\Project\\Python\\PythonGadgets\\word_vector\\fasttext\\clean_data.txt')
train('D:\\Project\\Python\\PythonGadgets\\word_vector\\headline_data\\million-headlines\\abcnews-date-text.csv')
#train('D:\\Project\\Python\\PythonGadgets\\word_vector\\headline_data\\million-headlines\\test.csv')
# 载入模型
model = Word2Vec.load('abc_news200.model')
print('Model loading done.')
word1 = 'uk'
word2 = 'british'
word3 = 'qantas'


# 分布式词向量
print('The word vector of “' + word1 + '” is:')
print(model.wv[word1])
# 测试单词的最近相似单词
print("Words similar to “" + word1 + "” are:")
print(model.wv.most_similar([word1], topn=100))
# 测试两个单词间的相似度
print('The similarity between ' + word1 + ' and ' + word2 + ' is:')
print(model.wv.similarity(word1, word2))
print('The similarity between ' + word1 + ' and ' + word3 + ' is:')
print(model.wv.similarity(word1, word3))


'''降维可视化'''
# 将词条和词向量存入列表
# 导入指定词的词向量
words = []
word_vector = []
load_similar_vectors('uk', 100, words, word_vector, model)
load_similar_vectors('qantas', 100, words, word_vector, model)
load_similar_vectors('rain', 100, words, word_vector, model)
load_similar_vectors('obama', 100, words, word_vector, model)

word_vector = np.array(word_vector)
print('Vectors loading done.')
# 绘图
plot_tSNE(word_vector, words, 'green')
plt.show()
