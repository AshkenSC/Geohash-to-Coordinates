'''
https://github.com/gaussic/tf-rnnlm

使用数据集：PTB
http://www.fit.vutbr.cz/~imikolov/rnnlm/simple-examples.tgz
'''

# -*- coding: utf-8 -*-

from preprocess import *
import tensorflow as tf


'''1. 模型参数设置'''
BATCH_SIZE = 64             # 单批次数据大小
NUM_STEPS = 20              # 单句长度
STRIDE = 3                  # 取数据的步长

VOCAB_SIZE = 10000          # 字典规模
EMBEDDING_DIM = 64          # 词向量维度
HIDDEN_DIM = 128            # 隐含层维度
NUM_LAYERS = 2              # RNN 层数
RNN_MODEL = 'gru'

LEARNING_RATE = 0.05        # 学习率
DROPOUT = 0.2               # 每层丢弃率

'''2. 按批次读取数据'''
class PTBInput(object):
    def __init__(self, data):
        self.batch_size = BATCH_SIZE
        self.num_steps = NUM_STEPS
        self.vocab_size = VOCAB_SIZE

        self.input_data, self.targets = ptb_batching(data,
            self.batch_size, self.num_steps)

        self.batch_len = self.input_data.shape[0]   # 总批次
        self.current_batch = 0                      # 当前批次

    '''读取下一批次'''
    def next_batch(self):
        x = self.input_data[self.current_batch]
        y = self.targets[self.current_batch]

        '''转换为one-hot编码'''
        y_ = np.zeros((y.shape[0], self.vocab_size), dtype=np.bool)
        for i in range(y.shape[0]):
            y_[i][y[i]] = 1

        '''如果到达最后一个批次，则回到开头'''
        self.current_batch = (self.current_batch + 1) % self.batch_len

        return x, y_


'''3. PTB模型类 '''
class PTBModel(object):
    def __init__(self, num_steps, vocab_size,
                 embedding_dim, hidden_dim, num_layers, rnn_model,
                 learning_rate, dropout,
                 is_training=True):

        self.num_steps = num_steps
        self.vocab_size = vocab_size

        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.rnn_model = rnn_model

        self.learning_rate = learning_rate
        self.dropout = dropout

        self.placeholders()     # 输入占位符
        self.rnn()              # 构建RNN模型
        self.cost()             # 代价函数
        self.optimize()         # 优化器
        self.error()            # 错误率


    '''输入占位符'''
    def placeholders(self):
        self.inputs = tf.placeholder(tf.int32, [None, self.num_steps])
        self.targets = tf.placeholder(tf.int32, [None, self.vocab_size])


    '''将数据转换为词向量表示'''
    def input_embedding(self):
        with tf.device("/cpu:0"):
            embedding = tf.get_variable(
                "embedding", [self.vocab_size,
                    self.embedding_dim], dtype=tf.float32)
            inputs = tf.nn.embedding_lookup(embedding, self.inputs)

        return inputs


    '''建立RNN模型'''
    def rnn(self):
        # 基本LSTM cell
        def lstm_cell():
            return tf.contrib.rnn.BasicLSTMCell(self.hidden_dim,
                state_is_tuple=True)

        # GRU cell
        def gru_cell():
            return tf.contrib.rnn.GRUCell(self.hidden_dim)

        # 在每个cell后添加dropout
        def dropout_cell():
            if (self.rnn_model == 'lstm'):
                cell = lstm_cell()
            else:
                cell = gru_cell()
            return tf.contrib.rnn.DropoutWrapper(cell,
                output_keep_prob=self.dropout)

        cells = [dropout_cell() for _ in range(self.num_layers)]
        cell = tf.contrib.rnn.MultiRNNCell(cells, state_is_tuple=True)

        inputs = self.input_embedding()
        outputs, _ = tf.nn.dynamic_rnn(cell=cell,
            inputs=inputs, dtype=tf.float32)

        # outputs的形状为[batch_size, num_steps, hidden_dim]
        last = outputs[:, -1, :]    # 只需最后一个输出

        logits = tf.layers.dense(inputs=last, units=self.vocab_size)
        prediction = tf.nn.softmax(logits)

        self._logits = logits
        self._pred = prediction


    '''计算交叉熵代价'''
    def cost(self):
        cross_entropy = tf.nn.softmax_cross_entropy_with_logits(
            logits=self._logits, labels=self.targets)
        cost = tf.reduce_mean(cross_entropy)
        self.cost = cost


    '''使用Adam优化器'''
    def optimize(self):
        optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
        self.optim = optimizer.minimize(self.cost)


    '''计算错误率'''
    def error(self):
        mistakes = tf.not_equal(
            tf.argmax(self.targets, 1), tf.argmax(self._pred, 1))
        self.errors = tf.reduce_mean(tf.cast(mistakes, tf.float32))


'''4. 训练函数'''
def run_epoch(num_epochs=5):
    # 载入训练集数据
    train_data, _, _, word_list, word_to_id = get_ptb_data('simple-examples/data')

    # 数据分批
    input_train = PTBInput(train_data)
    batch_len = input_train.batch_len
    # 建立模型
    model = PTBModel(NUM_STEPS, VOCAB_SIZE, EMBEDDING_DIM,
                     HIDDEN_DIM, NUM_LAYERS, RNN_MODEL,
                     LEARNING_RATE, DROPOUT)

    # 创建session并初始化变量
    session = tf.Session()
    session.run(tf.global_variables_initializer())

    print('开始训练：')
    for epoch in range(num_epochs):     # 迭代次数
        for i in range(batch_len):      # 经过batch批次数
            x_batch, y_batch = input_train.next_batch()

            # 取一批次数据进行优化
            feed_dict = {model.inputs: x_batch, model.targets: y_batch}
            session.run(model.optim, feed_dict=feed_dict)

            # 每过500个批次 输出一次结果
            if i % 500 == 0:
                cost = session.run(model.cost, feed_dict=feed_dict)

                msg = "Epoch: {0:>3}, batch: {1:>5}, Loss: {2:>6.3}"
                print(msg.format(epoch + 1, i + 1, cost))

                # 输出部分预测结果
                pred = session.run(model._pred, feed_dict=feed_dict)
                word_ids = session.run(tf.argmax(pred, 1))
                print('Predicted:', ' '.join(word_list[w] for w in word_ids))
                true_ids = np.argmax(y_batch, 1)
                print('True:', ' '.join(word_list[w] for w in true_ids))

    print('训练结束。')
    session.close()


# 进行训练
run_epoch(3)
