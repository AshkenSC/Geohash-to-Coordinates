# 将句子转为NER标记
# 该程序需在服务器上依赖NER-BERT模型运行

import time
from bert_base.client import BertClient
import json

SOURCE_PATH = ''
DEST_PATH = ''

# 载入数据源文件
source_file = open(SOURCE_PATH, 'r', encoding='utf-8')
# 打开写入结果的文件
output_file = open(DEST_PATH, 'a', encoding='utf-8')

with BertClient(show_server_config=False, check_version=False, check_length=True, mode='NER') as bc:
    start_t = time.perf_counter()

    # 读取文件，将所有句子分成前后两部分的短句。所有短句放在同一个大list中
    sub_sentences = list()
    for line in source_file:
        fragments = line.split(';;;;ll;;;;')
        sub_sentences.append(fragments[0])
        sub_sentences.append(fragments[2])

    # 将所有短句进行NER转码
    ner = bc.encode(fragments)
    print(time.perf_counter() - start_t)

    # 将结果存入json文件
    result = json.dumps(ner)
    output_file.write(result)

source_file.close()
output_file.close()