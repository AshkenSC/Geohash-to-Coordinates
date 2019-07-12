import codecs
import re
from gensim.models import FastText

'''数据集去除多余字符'''
def remove_char(write_file, read_file):
    f=codecs.open(write_file, "a+",'utf-8')

    i = 0
    for line in open(read_file, encoding='utf-8'):
        newline = re.sub('[·a-zA-Z0-9_,]','',line)
        f.write(newline)
        # 输出显示工作进度
        print('removing redundant characters, processing: ' + str(i))
        i += 1

    f.close()


'''数据集导入与训练'''
def train(open_file):
    # 将文本行存入列表
    i = 1
    lines = []
    for line in open(open_file, encoding='utf-8'):
        lines.append(line.split(' '))
        print("appending line " + str(i))
        i += 1
    print('Data input complete.')
    # 训练数据
    model = FastText(lines, size=50, min_count=2, iter=5)
    model.save('testModel.model')   # 保存为model格式
    model.wv.save_word2vec_format('testModelVec.vector', binary=False) # 保存为vector


remove_char(write_file='clean_data.txt', read_file='test.txt')
train('clean_data.txt')