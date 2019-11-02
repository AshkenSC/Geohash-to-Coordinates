'''
https://zhuanlan.zhihu.com/p/37865648
'''

import numpy as np

TRAIN_BATCH_SIZE = 20 # 训练数据batch大小
TRAIN_NUM_STEP = 35 # 训练数据阶段长度

TRAIN_DATA = 'ptb.train'
TEST_DATA = 'ptb.test'
EVAL_DATA = 'ptb.valid'

def read_data(file_path):
    '''
    读取数据，返回包含单词编号的数组，一整个文本的内容作为一个数组返回，每行句子拼接起来
    '''
    with open(file_path, 'r') as fin:
        id_string = ' '.join([line.strip() for line in fin.readlines()])
    id_list = [int(w) for w in id_string.split()]
    return id_list

def make_batches(id_list, batch_size, num_step):
    '''
    获取到batch
    Args:
        id_list: 一整个文本组成的数组，内容是word的id
        batch_size: batch的大小
        num_step: 表示训练时的上下文，输入的单词个数
    '''
    num_batches = (len(id_list) - 1) // (batch_size * num_step) # batch的数量 1327
    print(num_batches)
    data = np.array(id_list[:num_batches * batch_size * num_step]) # 从训练数据中取整
    print(data.shape) # (928900, )
    data = np.reshape(data, [batch_size, num_batches * num_step]) # 将数据切分成 batch_size, num_batches * num_steps的数组 (20, 46445)
    # 沿着第二个维度将数据切分为num_batches的batch，存入一个数组
    print(data.shape)
    data_batches = np.split(data, num_batches, axis = 1)
    print(data_batches[0].shape)

    label = np.array(id_list[1:num_batches * batch_size * num_step + 1])
    label = np.reshape(label, [batch_size, num_batches * num_step])
    label_batches = np.split(label, num_batches, axis=1)
    return list(zip(data_batches, label_batches))

train_batches = make_batches(read_data(TRAIN_DATA), TRAIN_BATCH_SIZE, TRAIN_NUM_STEP)