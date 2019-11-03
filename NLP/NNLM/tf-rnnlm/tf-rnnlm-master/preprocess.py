#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
import os
import numpy as np


'''读取原文本并转换为单词列表'''
def get_word_list(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().replace('\n', '<eos>').split()


'''构建单词与序号相互转换的映射表'''
def build_vocab(path):
    data = get_word_list(path)

    counter = Counter(data)
    count_pairs = sorted(counter.items(), key=lambda x: -x[1])

    word_list, _ = list(zip(*count_pairs))
    word_to_id = dict(zip(word_list, range(len(word_list))))

    return word_list, word_to_id


'''将一个文本文件转换为词序号列表'''
def text_to_id(path, word_to_id):
    data = get_word_list(path)
    return [word_to_id[x] for x in data if x in word_to_id]


'''将句子从词序号列表转换回单词'''
def id_to_sentence(sentence, word_list):
    return list(map(lambda x: word_list[x], sentence))


'''调用上述函数，处理原始数据'''
def get_ptb_data(path=None):
    train_path = os.path.join(path, 'ptb.train.txt')
    valid_path = os.path.join(path, 'ptb.valid.txt')
    test_path = os.path.join(path, 'ptb.test.txt')

    word_list, word_to_id = build_vocab(train_path)
    train_data = text_to_id(train_path, word_to_id)
    valid_data = text_to_id(valid_path, word_to_id)
    test_data = text_to_id(test_path, word_to_id)

    return train_data, valid_data, test_data, word_list, word_to_id


'''将原始数据列表转换为多个批次'''
def ptb_batching(raw_data, batch_size=64, num_steps=20, stride=3):
    '''
    参数：
        raw_data: 函数get_ptb_data()产生的数据
        batch_size: 数据分批输出，每次的数据量
        num_steps: 单句长度
        stride: 取数据的步长
    '''

    data_len = len(raw_data)
    sentences = []
    next_words = []

    for i in range(0, data_len - num_steps, stride):
        sentences.append(raw_data[i:(i + num_steps)])
        next_words.append(raw_data[i + num_steps])

    sentences = np.array(sentences)
    next_words = np.array(next_words)

    batch_len = len(sentences) // batch_size
    x = np.reshape(sentences[:(batch_len * batch_size)], [batch_len, batch_size, -1])
    y = np.reshape(next_words[:(batch_len * batch_size)], [batch_len, batch_size])

    return x, y


'''执行预处理'''
train_data, valid_data, test_data, word_list, word_to_id = get_ptb_data('simple-examples/data')
x_train, y_train = ptb_batching(train_data)

# 输出显示数据批次数及每次的训练集维度
print(x_train.shape)
print(y_train.shape)

# 示例：输出第64个批次的第3句话，及其下一个词
print(id_to_sentence(x_train[64, 3], word_list))
print(word_list[np.argmax(x_train[64, 3])])

