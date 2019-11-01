'''
https://blog.csdn.net/Yellow_python/article/details/89088854
'''

'''1. 工具导入'''
from collections import Counter
import numpy as np
import pandas as pd
pdf = lambda data, index=None, columns=None: pd.DataFrame(data, index, columns)


'''2. 语料预处理'''

'''语料'''
corpus = '''她的菜很好 她的菜很香 她的他很好 他的菜很香 他的她很好
很香的菜 很好的她 很菜的他 她的好 菜的香 他的菜 她很好 他很菜 菜很好'''.split()

'''预处理'''
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
print("预处理：")
print(pdf(counter, None, ['word', 'freq']))


'''3. unigram'''
unigram = np.array([entry[1] for entry in counter])
unigram = unigram / sum(unigram)

# 输出unigram 字-概率 表
print('unigram:')
print(pdf(unigram.reshape(1, char_count), ['概率'], char_list))
print('\n')

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
for i in range(char_count):
    bigram[i] = bigram[i] / bigram[i].sum()

# 输出bigram 字-概率 表
pd.DataFrame(bigram, char_list, char_list, int)
# 频数 --> 概率
for i in range(char_count):
    bigram[i] = bigram[i] / bigram[i].sum()
print('bigram:')
print(pdf(bigram, char_list, char_list))
print('\n')


'''5. 概率计算'''
def prob(sentence):
    # 将句子字符转为对应编号后存储于列表id_sentence
    id_sentence = []
    for char in sentence:
        id_sentence.append(char_to_id[char])
    sentence_len = len(id_sentence)    # 句子包含字符数

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

print(prob('菜很香'), 1 / 6 / 6)

print('很好的菜', prob('很好的菜'))
print('菜很好的', prob('菜很好的'))
print('菜好的很', prob('菜好的很'))


"""排列组合"""
def permutation_and_combination(ls_ori, ls_all=None):
    ls_all = ls_all or [[]]
    le = len(ls_ori)
    if le == 1:
        ls_all[-1].append(ls_ori[0])
        ls_all.append(ls_all[-1][: -2])
        return ls_all
    for i in range(le):
        ls, lsi = ls_ori[:i] + ls_ori[i + 1:], ls_ori[i]
        ls_all[-1].append(lsi)
        ls_all = permutation_and_combination(ls, ls_all)
    if ls_all[-1]:
        ls_all[-1].pop()
    else:
        ls_all.pop()
    return ls_all

print('123排列组合', permutation_and_combination([1, 2, 3]))


"""给定词组，返回最大概率组合的句子"""
def max_prob(char_list):
    pc = permutation_and_combination(char_list)  # 生成排列组合
    p, w = max((prob(s), s) for s in pc)
    return p, ''.join(w)

print(*max_prob(list('香很的菜')))
print(*max_prob(list('好很的他菜')))
print(*max_prob(list('好很的的她菜')))

