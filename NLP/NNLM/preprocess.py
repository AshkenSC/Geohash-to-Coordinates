'''
https://zhuanlan.zhihu.com/p/37850304
'''

'''工具导入'''
import codecs
import collections
from operator import itemgetter

'''定义文件路径'''
RAW = './simple-examples/data/ptb.train.txt' # 训练集数据
VOCAB_OUTPUT = 'ptb.vocab' # vocab文件路径
TRAIN = './simple-examples/data/ptb.train.txt' # 训练集数据
TEST = './simple-examples/data/ptb.test.txt' # 测试集数据
VALID = './simple-examples/data/ptb.valid.txt' # 测试集数据
OUTPUT_TRAIN = 'ptb.train'
OUTPUT_TEST = 'ptb.test'
OUTPUT_VALID = 'ptb.valid'


'''按照词频进行统计并输出'''
counter = collections.Counter()
with codecs.open(RAW, 'r', 'utf-8') as f:
    for line in f:
        for word in line.strip().split():
            counter[word] += 1

sorted_word2cnt = sorted(counter.items(), key = itemgetter(1), reverse=True)
sorted_words = []
for i in sorted_word2cnt:
    sorted_words.append(i[0])
sorted_words = ["<eos>"] + sorted_words


'''按词频顺序，将所有单词输出到vocab文件中'''
with codecs.open(VOCAB_OUTPUT, 'w', 'utf-8') as file_output:
    for word in sorted_words:
        file_output.write(word + '\n')


'''构建词到序号映射的字典word2id'''
word2id={}
id = 0
with codecs.open(VOCAB_OUTPUT) as vocab_file:
    for line in vocab_file:
        word2id[line.strip()] = id
        id += 1


'''获取单词对应的序号'''
def get_id(word):
    if word in word2id:
        return word2id[word]
    else:
        return word2id['<unk>']


'''将源文本转化为单词序号的序列'''
def text_to_id(raw_data_path, output_data_path):
    fin = codecs.open(raw_data_path, 'r', 'utf-8')
    fout = codecs.open(output_data_path, 'w', 'utf-8')
    for line in fin:
        words = line.strip().split() + ["<eos>"]
        out_line = ' '.join([str(get_id(word)) for word in words]) + '\n'
        fout.write(out_line)
    fin.close()
    fout.close()

text_to_id(TRAIN, OUTPUT_TRAIN)
text_to_id(TEST, OUTPUT_TEST)
text_to_id(VALID, OUTPUT_VALID)