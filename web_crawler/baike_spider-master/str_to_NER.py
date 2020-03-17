# 将句子转为NER标记，保存为JSON格式
# JSON格式为：[[句1左，句1右]，[句2左，句2右]，...]
# 该程序需在服务器上依赖NER-BERT模型运行

import time
from bert_base.client import BertClient
import json
import re

SOURCE_PATH = '/home/xuxi/BERT-BiLSTM-CRF-NER/sentences/baidu/cure.txt'
DEST_PATH = '/home/xuxi/BERT-BiLSTM-CRF-NER/sentences/baidu/NER/cure_NER.json'

# 载入数据源文件
source_file = open(SOURCE_PATH, 'r', encoding='utf-8')
# 打开写入结果的文件
output_file = open(DEST_PATH, 'w', encoding='utf-8')

with BertClient(show_server_config=False, check_version=False, check_length=False, mode='NER') as bc:
    start_t = time.perf_counter()

    # 读取文件，将所有句子分成前后两部分的短句。所有短句放在同一个大list中
    sub_sentences = list()
    for line in source_file:
        fragments = line.split(';;;;ll;;;;')
        if len(fragments) == 3 and re.match(r' +', fragments[0]) is None and re.match(r' +', fragments[2]) is None:
            fragments = [fragments[0], fragments[2]]
            print(fragments[0], fragments[1])
            # 将所有短句进行NER转码
            marked_fragments = bc.encode(fragments)
            sub_sentences.append(marked_fragments.tolist())
            print(time.perf_counter() - start_t)

    # 将结果存入json文件
    result = json.dumps(sub_sentences)
    output_file.write(result)

source_file.close()
output_file.close()