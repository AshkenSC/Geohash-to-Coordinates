'''
https://blog.csdn.net/Yellow_python/article/details/89088854
'''

'''-----------------'''
'''1. 模块导入'''
from collections import Counter
import numpy as np
import pandas as pd
pdf = lambda data, index=None, columns=None: pd.DataFrame(data, index, columns)


'''-----------------'''
'''2. 语料预处理'''
# 语料
corpus = '她很香 她很菜 她很好 他很菜 他很好 菜很好'
corpus = corpus.split()     # 将句子分割并存入列表中

# 预处理
# 词频统计：统计语料中的各个字出现次数，并存入counter对象中
counter = Counter()
for sentence in corpus:
    for char in sentence:
        counter[char] += 1

# 将所有出现过的字存入列表char_list中
char_list = []
for char in counter:
    char_list.append(char)
counter = counter.most_common()     # 将counter转化为（字，出现次数）的二元组列表
char_count = len(counter)           # 语料中共出现了多少个不同的字
# 构建从字到字编号的映射
char_to_id = {}
for i in range(char_count):
    char_to_id[counter[i][0]] = i
# 构建从字编号的字的映射
id_to_char = {}
for char, i in char_to_id.items():
    id_to_char[i] = char

# 输出预处理结果
print("字频：")
print(pdf(counter, None, ['word', 'freq']))
print('\n')


'''-----------------'''
'''3. unigram'''
unigram = np.array([entry[1] for entry in counter])
unigram = unigram / sum(unigram)

# 输出unigram 字-概率 表
print('unigram:')
print(pdf(unigram.reshape(1, char_count), ['概率'], char_list))
print('\n')


'''-----------------'''
'''4. bigram'''
# 初始化bigram数组，并进行平滑
bigram = np.zeros((char_count, char_count))
bigram = bigram  + 1e-8     # 平滑

for sentence in corpus:
    # 将句子中的字转为对应的字编号，并存储在列表sentence中
    sentence = [char_to_id[w] for w in sentence]
    # 对句子中每个字前一个字进行统计（注：原理不太懂，需要进一步解释）
    for i in range(1, len(sentence)):
       bigram[sentence[i - 1], sentence[i]] += 1
# 频数 --> 概率
for i in range(char_count):
    bigram[i] = bigram[i] / bigram[i].sum()

# 输出bigram 字-概率 表
pd.DataFrame(bigram, char_list, char_list, int)
pd.set_option('display.max_columns',100)    # 设置DataFrame可显示的最大列数，避免显示省略号
print('bigram:')
print(pdf(bigram, char_list, char_list))
print('\n')


'''-----------------'''
'''5. 概率计算'''
def sentence_prob(sentence):
    # 将句子字符转为对应编号后存储于列表id_sentence
    id_sentence = []
    for char in sentence:
        id_sentence.append(char_to_id[char])
    sentence_len = len(id_sentence)    # 句子包含的字符数

    # 计算概率
    # (此处可能需要补充注释)
    if sentence_len < 1:
        return 0
    probability = unigram[id_sentence[0]]
    if sentence_len < 2:
        return probability
    for i in range(1, sentence_len):
        probability = probability * bigram[id_sentence[i - 1], id_sentence[i]]
    return probability


print('菜很香', sentence_prob('菜很香'))


