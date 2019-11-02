'''
https://zhuanlan.zhihu.com/p/37850304
'''

# 用来做数据处理和生成训练数据
import codecs
import collections
import tensorflow as tf
import numpy as np
from operator import itemgetter

RAW_DATA = './simple-examples/data/ptb.train.txt' # 训练集数据
VOCAB_OUTPUT = 'ptb.vocab' # vocab文件路径
counter = collections.Counter()

with codecs.open(RAW_DATA, 'r', 'utf-8') as f:
    for line in f:
        for word in line.strip().split():
            counter[word] += 1

# 按照词频进行统计
sorted_word_to_cnt = sorted(counter.items(), key = itemgetter(1), reverse=True)
sorted_words = [x[0] for x in sorted_word_to_cnt]
sorted_words = ["<eos>"] + sorted_words

# 将10, 000所有单词按照词频顺序输出到vocab文件中
with codecs.open(VOCAB_OUTPUT, 'w', 'utf-8') as file_output:
    for word in sorted_words:
        file_output.write(word + '\n')

# 建立word2idx
word2idx={}
id = 0
with codecs.open(VOCAB_OUTPUT) as vocab_file:
    for line in vocab_file:
        word2idx[line.strip()] = id
        id += 1