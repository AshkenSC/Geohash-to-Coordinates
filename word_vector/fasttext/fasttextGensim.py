import codecs
import re
from gensim.models import FastText

'''数据集去除多余字符'''
def remove_char(write_file, read_file):
    f=codecs.open(write_file, "w",'utf-8')

    i = 0
    for line in open(read_file, encoding='utf-8'):
        newline = re.sub('[·a-zA-Z0-9_,]','',line)
        f.write(newline)
        # 输出显示工作进度
        print('removing redundant characters, processing: ' + str(i))
        i += 1

    f.close()


'''数据集导入与训练'''
def train(open_file, dim):
    # 将文本行存入列表
    i = 1
    lines = []
    for line in open(open_file, encoding='utf-8'):
        lines.append(line.split(' '))
        print("appending line " + str(i))
        i += 1
    print('Data input complete.')
    # 训练数据
    model = FastText(lines, size=dim, min_count=3, iter=5)
    model.save('testModel.model')   # 保存为model格式
    model.wv.save_word2vec_format('testModelVec.vector', binary=False) # 保存为vector


'''训练模型（如模型已存在请勿重复加载训练）'''
#remove_char(write_file='clean_data.txt', read_file='data_train.txt')
#train('clean_data.txt', 200)

'''模型加载与测试'''
# 载入模型
model = FastText.load('testModel.model')

word1 = '劲舞团'
word2 = '石油'
word3 = '原油'
# 获取词向量
print(word1 + ' 的词向量为：')
print(model.wv[word1])
# 求相似度
print(word1 + ' 和 ' + word2  + ' 的相似度为：')
print(model.wv.similarity(word1, word2))
print(word3 + ' 和 ' + word2 + ' 的相似度为：')
print(model.wv.similarity(word3, word2))
# 求最相似词语
print('和' + word1 + ' 最相似的词语为：')
print(model.most_similar(word1))