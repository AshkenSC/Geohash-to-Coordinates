# 从文本中按照正则表达式提取不同类别的关系句子

'''
rel == 治疗:   归为 可医治
治疗，head == 细菌，tail == 症状（如肉毒杆菌治疗肌肉痉挛）

rel == 推荐药物 就叫推荐药物
使用， head == 疾病，tail == 药物
（反过来）抑制，治疗，用于，预防 head== 药物，tail== 疾病，症状

rel == 引起: 就叫引起

引起，起的，head == 细菌/病因/病毒/疾病, tail == 症状/疾病/细菌（细菌引起细菌）
导致，所致head == 各种原因，tail == 疾病，症状
（反过来）由于，原因，head == 疾病，tail == 病因
可引，head == 疾病，tail == 症状，head == 原因，tail == 疾病
刺激，head == 病因，tail == 疾病/症状
感染，head == 细菌，病毒，tail == 疾病
因为，head == 疾病，tail == 病毒
产生，head == 病毒，tail == 症状
造成, 而出现

rel == 相似疾病，相似症状: 统一叫相关症状or相关疾病（需要判断head tail分类确定）

伴有，常有，典型，并发，继发，出现
 引起，导致，常伴有，表现为，并发症 是一种，最常见

 出现以上关键词，headtail同为疾病或症状

rel == 检测:

检查（可发现），head == 检查项目，tail == 疾病/症状
检测，head == 检查项目，tail == 病毒/药物（抗体类）
诊断，head == 检查项目，tail == 病毒

rel == 病症:

患者，head == 疾病，tail == 症状
主要，表现，不同程度，head == 疾病，tail == 症状
伴有，常有，典型，并发，继发，出现， head == 疾病，tail == 症状
临床表现
表现为，症状为，head== 疾病，tail==症状
（反过来）多见于，多发生，可见于，为特征 head== 症状，tail==疾病

rel== 检查：
检查，检测 head==医学专科，tail==疾病

'''

import json
import os
import re

regex_list = {
    '可医治':r'([，。；]*)([^，。；]*)(治疗)([^，。；]*)([，。；])',
    '推荐药物':r'([，。；]*)([^，。；]*)(使用|医治|治疗|用于|推荐|预防)([^，。；]*)([，。；])',
    '引起':r'([，。；]*)([^，。；]*)(引起|导致|所致|由于|原因|刺激|感染|产生|造成|因为|出现)([^，。；]*)([，。；])',
    '检测':r'([，。；]*)([^，。；]*)(检查|可发现|检测|诊断)([^，。；]*)([，。；])',
    '病症':r'([，。；]*)([^，。；]*)(患者|主要|表现|不同程度|伴有|常有|典型|并发|继发|表现为|症状为|多见于|多发生|可见于|为特征)([^，。；]*)([，。；])',
    '检查':r'([，。；]*)([^，。；]*)(检查|检测)([^，。；]*)([，。；])',
}

# 保存所有找到的句子及其类别的字典，格式为sentence:type
sentences = dict()

# 找到给定文本里所有符合规则的句子
# 返回一个字典（sentence:type），sentence用于保存句子，type用于保存sentence对应的句子类别
def find_sentence(text):
    global sentences
    sentence_and_type = dict()
    for regex in regex_list:
        re.findall()
    for entry in sentence_and_type.items():
        sentences[entry[0]] = entry[1]


file_list = list()  # 保存当前目录下的文件列表
for dir_path, dir_names, file_names in os.walk(r'D:\Project\Python\PythonGadgets\web_crawler\baike_spider-master\classified-merged\classified-merged-json\v2'):
    for file_name in file_names:
        file_list.append(os.path.join(dir_path, file_name))
for file in file_list:
    if file.endswith('.json'):
        print('正在读取文件：' + repr(file).encode('gbk', 'ignore').decode('gbk'))
        json_file = open(os.path.join('classified-merged/classified-merged-json/v2/', file), 'r', encoding='utf-8')
        for json_line in json_file:
            line = json.loads(json_line)
            # 在summary里根据正则表达式找匹配的句子及其所属类别，将结果加入总字典sentences中
            find_sentence(line['summary'])
            # 在contents的各个text里根据正则表达式找匹配的句子及其所属类别
            for content in line['contents']:
                find_sentence(content['text'])



        json_file.close()

