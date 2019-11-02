'''
https://zhuanlan.zhihu.com/p/37886740
'''

# coding: utf-8
import numpy as np
import tensorflow as tf

# 定义文件路径
TRAIN_DATA = 'ptb.train'
TEST_DATA = 'ptb.test'
EVAL_DATA = 'ptb.valid'

# 定义超参数
HIDDEN_SIZE = 300
NUM_LAYERS = 2  # LSTM 结构的层数
VOCAB_SIZE = 10000  # 字典规模
TRAIN_BATCH_SIZE = 20  # 训练数据batch大小
TRAIN_NUM_STEP = 35  # 训练数据阶段长度

EVAL_BATCH_SIZE = 1  # 测试数据batch大小
EVAL_NUM_STEP = 1  # 测试数据阶段长度
NUM_EPOCH = 5  # 使用训练数据轮数
LSTM_KEEP_PROB = 0.9
EMBEDDING_KEEP_PROB = 0.9
MAX_GRAD_NORM = 5  # 用于控制梯度膨胀的梯度大小上限
SHARED_EMB_AND_SOFTMAX = True  # 在softmax层和词向量层之间共享参数


# 通过一个PTBModel类来描述模型
class PTBModel(object):
    def __init__(self, is_training, batch_size, num_steps):
        '''
        Arg:
            is_training: 表示是否在训练
            batch_size: 表示batch size
            num_stpes: 表示截断长度
        '''
        self.batch_size = batch_size
        self.num_steps = num_steps
        self.input_data = tf.placeholder(tf.int32, [batch_size, num_steps])
        self.targets = tf.placeholder(tf.int32, [batch_size, num_steps])

        # 构造LSTM结构，多层的LSTM，包括了dropout机制
        dropout_keep_prob = LSTM_KEEP_PROB if is_training else 1.0
        lstm_cells = [
            tf.nn.rnn_cell.DropoutWrapper(
                tf.nn.rnn_cell.BasicLSTMCell(HIDDEN_SIZE),
                output_keep_prob=dropout_keep_prob
            ) for _ in range(NUM_LAYERS)
        ]
        # 多层结构
        cell = tf.nn.rnn_cell.MultiRNNCell(lstm_cells)

        # 表示初始状态
        self.initial_state = cell.zero_state(batch_size, tf.float32)

        # 定义单词的词向量矩阵
        embedding = tf.get_variable("embedding", [VOCAB_SIZE, HIDDEN_SIZE])

        # 将数据转化为词向量表示
        inputs = tf.nn.embedding_lookup(embedding, self.input_data)

        # 只在训练时使用dropout
        if is_training:
            inputs = tf.nn.dropout(inputs, EMBEDDING_KEEP_PROB)

        # 定义输出列表，先将不同时刻LSTM结构的输出收集起来，再一起提供给softmax层
        outputs = []
        state = self.initial_state
        with tf.variable_scope('RNN'):
            for time_step in range(num_steps):
                if time_step > 0:
                    tf.get_variable_scope().reuse_variables()
                cell_output, state = cell(inputs[:, time_step, :], state)  # 每次计算每个time_step的结果
                outputs.append(cell_output)

        # 把输出队列展开成[batch, hidden_size * num_steps]的形状，然后再reshape成
        output = tf.reshape(tf.concat(outputs, 1), [-1, HIDDEN_SIZE])

        # softmax层：将RNN在每个位置上的输出转化为各个单词的logits
        if SHARED_EMB_AND_SOFTMAX:
            weight = tf.transpose(embedding)
        else:
            weight = tf.get_variable("weight", [HIDDEN_SIZE, VOCAB_SIZE])

        bias = tf.get_variable("bias", [VOCAB_SIZE])

        logits = tf.matmul(output, weight) + bias

        loss = tf.nn.sparse_softmax_cross_entropy_with_logits(
            labels=tf.reshape(self.targets, [-1]),
            logits=logits
        )
        self.cost = tf.reduce_sum(loss) / batch_size
        self.final_state = state

        # 如果是训练状态，那么还需要实现反向传播
        if not is_training:
            return

        # 这个训练过程没有学过
        trainable_variables = tf.trainable_variables()
        grads, _ = tf.clip_by_global_norm(tf.gradients(self.cost, trainable_variables), MAX_GRAD_NORM)
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=1.0)
        self.train_op = optimizer.apply_gradients(
            zip(grads, trainable_variables)
        )


# In[4]:


def run_epoch(session, model, batches, train_op, output_log, step):
    '''
    训练函数
    Args:
        session 上下文
        model 上述模型的实例
        batches 数据
        train_op
        output_log 是否打印输出日志
        step
    Return:
        step
        结果
    '''
    total_costs = 0.0
    iters = 0
    state = session.run(model.initial_state)

    # 训练一个epoch
    for x, y in batches:
        # 在当前batch上运行train_op 并计算损失值
        cost, state, _ = session.run([model.cost, model.final_state, train_op],
                                     feed_dict={model.input_data: x, model.targets: y, model.initial_state: state}
                                     )
        total_costs += cost
        iters += model.num_steps  # 迭代次数

        # 在训练时输出日志
        if output_log and step % 100 == 0:
            print("After %d steps, perplexity is % .3f" % (step, np.exp(total_costs / iters)))
        step += 1

    return step, np.exp(total_costs / iters)


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
    num_batches = (len(id_list) - 1) // (batch_size * num_step)  # batch的数量
    print
    num_batches
    data = np.array(id_list[:num_batches * batch_size * num_step])
    print
    data.shape
    data = np.reshape(data, [batch_size, num_batches * num_step])  # 将数据切分成 batch_size, num_batches * num_steps的数组
    # 沿着第二个维度将数据切分为num_batches的batch，存入一个数组
    print
    data.shape
    data_batches = np.split(data, num_batches, axis=1)
    print
    data_batches[0].shape

    label = np.array(id_list[1:num_batches * batch_size * num_step + 1])
    label = np.reshape(label, [batch_size, num_batches * num_step])
    label_batches = np.split(label, num_batches, axis=1)
    return list(zip(data_batches, label_batches))


def main():
    initializer = tf.random_uniform_initializer(-0.05, 0.05)  # 初始化函数

    # 训练的RNN模型
    with tf.variable_scope("language_model", reuse=None, initializer=initializer):
        train_model = PTBModel(is_training=True, batch_size=TRAIN_BATCH_SIZE, num_steps=TRAIN_NUM_STEP)

    # 测试用的模型，与train_model共用参数，但没有dropout(is_training=False)
    with tf.variable_scope("language_model", reuse=True, initializer=initializer):
        eval_model = PTBModel(is_training=False, batch_size=EVAL_BATCH_SIZE, num_steps=EVAL_NUM_STEP)

    # 训练模型
    with tf.Session() as sess:
        # 初始化
        tf.global_variables_initializer().run()

        # 训练数据
        train_batches = make_batches(
            read_data(TRAIN_DATA),
            TRAIN_BATCH_SIZE,
            TRAIN_NUM_STEP
        )

        # eval数据
        eval_batches = make_batches(
            read_data(EVAL_DATA),
            EVAL_BATCH_SIZE,
            EVAL_NUM_STEP
        )

        # test数据
        test_batches = make_batches(
            read_data(TEST_DATA),
            EVAL_BATCH_SIZE,
            EVAL_NUM_STEP
        )

        step = 0
        # 每一轮
        for i in range(NUM_EPOCH):
            print("In iteration: %d" % (i + 1))
            # 训练过程
            step, train_pplx = run_epoch(sess, train_model, train_batches,
                                         train_model.train_op,
                                         output_log=True,
                                         step=step
                                         )
            print("Epoch: %d Train Perplexity: %.3f" % (i + 1, train_pplx))

            # evaluation过程
            _, eval_pplx = run_epoch(sess, eval_model, eval_batches,
                                     tf.no_op(),
                                     output_log=False,
                                     step=0
                                     )
            print("Epoch: %d Eval Perplexity: %.3f" % (i + 1, eval_pplx))
        _, test_pplx = run_epoch(sess, eval_model, eval_batches, tf.no_op(), output_log=False, step=0)
        # 训练结束进行test
        print("Test Perplexity: %.3f" % (test_pplx))


main()