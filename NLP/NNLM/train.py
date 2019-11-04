'''
https://zhuanlan.zhihu.com/p/37886740
'''

# coding: utf-8
import numpy as np
import tensorflow as tf

'''定义文件路径与超参数'''
TRAIN = 'ptb.train'
TEST = 'ptb.test'
EVAL = 'ptb.valid'

HIDDEN_SIZE = 300
NUM_LAYERS = 2                  # LSTM结构的层数
VOCAB_SIZE = 10000              # 字典规模
TRAIN_BATCH_SIZE = 20           # 训练数据batch大小
TRAIN_STEP = 35                 # 训练数据阶段长度

EVAL_BATCH_SIZE = 1             # 测试集batch大小
EVAL_STEP = 1                   # 测试集阶段长度
NUM_EPOCH = 5                   # 训练轮次数
LSTM_KEEP_PROB = 0.9
EMBEDDING_KEEP_PROB = 0.9
MAX_GRAD_NORM = 5               # 用于控制梯度膨胀的梯度大小上限
SHARED_EMB_AND_SOFTMAX = True   # 在softmax层和词向量层之间共享参数


'''使用PTBModel类描述模型'''
class PTBModel(object):
    def __init__(self, is_training, batch_size, num_steps):
        '''
        参数：
        is_training: 是否在训练
        batch_size: batch大小
        num_stpes: 截断长度
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

        # 初始状态
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

        # 如果处于训练状态，还需要进行反向传播
        if not is_training:
            return

        # 这个训练过程没有学过
        trainable_variables = tf.trainable_variables()
        grads, _ = tf.clip_by_global_norm(tf.gradients(self.cost, trainable_variables), MAX_GRAD_NORM)
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=1.0)
        self.train_op = optimizer.apply_gradients(
            zip(grads, trainable_variables)
        )


'''训练函数'''
def run_epoch(session, model, batches, train_op, output_log, step):
    '''
    参数：
        session 上下文
        model 上述模型的实例
        batches 数据
        train_op
        output_log 是否打印输出日志
        step
    返回值：
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


'''读取文本，将每行句子拼接，一整个文本转化为一个单词序号列表，作为函数返回值'''
def get_id_list(path):
    with open(path, 'r') as fin:
        source_str = ' '.join([line.strip() for line in fin.readlines()])
    id_list = []
    for word in source_str.split():
        id_list.append(int(word))
    return id_list


'''获取batch'''
def get_batch(id_list, batch_size, num_step):
    '''
    参数：
    id_list: 一整个文本组成的数组，内容是word的id
    batch_size: batch的大小
    num_step: 表示训练时的上下文，输入的单词个数
    '''

    num_batch = (len(id_list) - 1) // (batch_size * num_step)
    print('batch数量:' + num_batch)
    data = np.array(id_list[:num_batch * batch_size * num_step])    # 从训练数据中取整
    print(data.shape)
    data = np.reshape(data,
                      [batch_size, num_batch * num_step])           # 将数据切分成 batch_size, num_batch * num_steps的数组 (20, 46445)
    # (注：尚不完全理解该注释含义）
    # 沿着第二个维度将数据切分为num_batch的batch，存入一个数组
    print(data.shape)
    data_batches = np.split(data, num_batch, axis=1)
    print(data_batches[0].shape)

    label = np.array(id_list[1:num_batch * batch_size * num_step + 1])
    label = np.reshape(label, [batch_size, num_batch * num_step])
    label_batches = np.split(label, num_batch, axis=1)
    return list(zip(data_batches, label_batches))


'''进行训练'''
initializer = tf.random_uniform_initializer(-0.05, 0.05)  # 初始化函数

# 训练的RNN模型
with tf.variable_scope("language_model", reuse=None, initializer=initializer):
    train_model = PTBModel(is_training=True, batch_size=TRAIN_BATCH_SIZE, num_steps=TRAIN_STEP)

# 测试用的模型，与train_model共用参数，但没有dropout(is_training=False)
with tf.variable_scope("language_model", reuse=True, initializer=initializer):
    eval_model = PTBModel(is_training=False, batch_size=EVAL_BATCH_SIZE, num_steps=EVAL_STEP)

# 训练模型
with tf.Session() as sess:
    # 初始化
    tf.global_variables_initializer().run()

    # 训练数据
    train_batch = get_batch(get_id_list(TRAIN), TRAIN_BATCH_SIZE, TRAIN_STEP)

    # 验证数据
    eval_batch = get_batch(get_id_list(EVAL), EVAL_BATCH_SIZE, EVAL_STEP)

    # 测试数据
    test_batch = get_batch(get_id_list(TEST), EVAL_BATCH_SIZE, EVAL_STEP)

    step = 0
    # 每一轮
    for i in range(NUM_EPOCH):
        print("Iteration: %d" % (i + 1))
        # 训练过程
        step, train_ppl = run_epoch(sess, train_model, train_batch,
                                     train_model.train_op,
                                     output_log=True,
                                     step=step
                                     )
        print("Epoch: %d Train Perplexity: %.3f" % (i + 1, train_ppl))

        # 验证过程
        _, eval_ppl = run_epoch(sess, eval_model, eval_batch,
                                 tf.no_op(),
                                 output_log=False,
                                 step=0
                                 )
        print("Epoch: %d Evaluation Perplexity: %.3f" % (i + 1, eval_ppl))
    _, test_ppl = run_epoch(sess, eval_model, eval_batch, tf.no_op(), output_log=False, step=0)

    # 训练完成，进行测试
    print("Test Perplexity: %.3f" % (test_ppl))
