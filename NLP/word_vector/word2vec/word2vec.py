from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt

'''定义变量名'''
# 输出模型名
OUTPUT_MODEL = 'ptb.model'
OUTPUT_VECTOR = 'ptb.vetor'
# 源数据路径
DATA_PATH = 'D:\\Project\\Python\\PythonGadgets\\NLP\\NNLM\\simple-examples\\data\\ptb.train.txt'


'''训练模型'''
def train(data):
    inp=data
    outp1 = OUTPUT_MODEL
    outp2 = OUTPUT_VECTOR
    print('正在载入数据...\n')
    model = Word2Vec(LineSentence(inp), size=200, window=5, min_count=5, workers=4)
    print('数据载入完成。\n')
    model.save(outp1)
    print('模型已储存。\n')
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
#train('D:\\Project\\Python\\PythonGadgets\\word_vector\\headline_data\\million-headlines\\abcnews-date-text.csv')
#train('D:\\Project\\Python\\PythonGadgets\\word_vector\\headline_data\\million-headlines\\test.csv')
train(DATA_PATH)
# 载入模型
model = Word2Vec.load(OUTPUT_MODEL)
print('模型载入完成')
word1 = 'britain'
word2 = 'british'
word3 = 'market'

# 分布式词向量
print('“' + word1 + '”的词向量是:')
print(model.wv[word1])
# 测试单词的最近相似单词
print("与“" + word1 + "” 最相似的词为:")
print(model.wv.most_similar([word1], topn=100))
# 测试两个单词间的相似度
print('“' + word1 + '”与“' + word2 + '”的相似度为:')
print( (word1, word2))
print('“' + word1 + '”与“' + word3 + '”的相似度为:')
print(model.wv.similarity(word1, word3))


'''降维可视化'''
# 将词条和词向量存入列表
# 导入指定词的词向量
words = []
word_vector = []
load_similar_vectors('investor', 100, words, word_vector, model)
load_similar_vectors('britain', 100, words, word_vector, model)
load_similar_vectors('market', 100, words, word_vector, model)
load_similar_vectors('company', 100, words, word_vector, model)

word_vector = np.array(word_vector)
print('Vectors loading done.')
# 绘图
#plot_tSNE(word_vector, words, 'green')
#plt.show()
