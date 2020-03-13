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

regex_dict = {
    '可医治':r'(?:[，。；]*)([^，。；]+)(治疗)([^，。；]+)(?:[，。；])',
    '推荐药物':r'(?:[，。；]*)([^，。；]+)(使用|医治|治疗|用于|推荐|预防)([^，。；]+)(?:[，。；])',
    '引起':r'(?:[，。；]*)([^，。；]+)(引起|导致|所致|由于|原因|刺激|感染|产生|造成|因为|出现)([^，。；]+)(?:[，。；])',
    '检测':r'(?:[，。；]*)([^，。；]+)(检查|可发现|检测|诊断)([^，。；]+)(?:[，。；])',
    '病症':r'(?:[，。；]*)([^，。；]+)(患者|主要|表现|不同程度|伴有|常有|典型|并发|继发|表现为|症状为|多见于|多发生|可见于|为特征)([^，。；]+)(?:[，。；])',
    '检查':r'(?:[，。；]*)([^，。；]+)(检查|检测)([^，。；]+)(?:[，。；])',
}


# 保存所有找到的句子及其类别的字典，格式为sentence:type
sentences_dict = dict()
# 保存结果的文件
cure_file = open('sentences/baidu/cure.txt', 'w', encoding='utf-8')
recommend_drug_file = open('sentences/baidu/recommend_drug.txt', 'w', encoding='utf-8')
cause_file = open('sentences/baidu/cause.txt', 'w', encoding='utf-8')
detect_file = open('sentences/baidu/detect.txt', 'w', encoding='utf-8')
disease_file = open('sentences/baidu/disease.txt', 'w', encoding='utf-8')
inspect_file = open('sentences/baidu/inspect.txt', 'w', encoding='utf-8')


# 找到给定文本里所有符合规则的句子
# 返回一个字典（sentence:type），sentence用于保存句子，type用于保存sentence对应的句子类别
def find_sentence(text):
    global sentences_dict
    for sentence_type, regex in regex_dict.items():
        # 找到text所有句子
        sentences = re.findall(regex, text)
        # 确定当前text里所有句子的类别
        for sentence in sentences:
            # 去除句子里的换行符
            stripped_sentence = list()
            for substring in sentence:
                stripped_sentence.append(substring.replace('\n', ' '))
            # 将句子存入sentences里
            sentences_dict[tuple(stripped_sentence)] = sentence_type
            print('找到句子：' + repr(stripped_sentence).encode('gbk', 'ignore').decode('gbk') + '；类别：' + sentence_type)

# 将结果保存到相应文件里
def save_output():
    #     '可医治':cure_file,
    #     '推荐药物':recommend_drug_file,
    #     '引起':cause_file
    #     '检测':detect_file
    #     '病症':disease_file
    #     '检查':inspect_file
    for entry in sentences_dict:
        if entry[1] is '可医治':
            for substring in entry[0]:
                cure_file.write(substring)
                if substring != entry[0][-1]:
                    cure_file.write(';;;;ll;;;;')
            cure_file.write('\n')
        if entry[1] is '推荐药物':
            for substring in entry[0]:
                recommend_drug_file.write(substring)
                if substring != entry[0][-1]:
                    recommend_drug_file.write(';;;;ll;;;;')
            recommend_drug_file.write('\n')
        if entry[1] is '引起':
            for substring in entry[0]:
                cause_file.write(substring)
                if substring != entry[0][-1]:
                    cause_file.write(';;;;ll;;;;')
            cause_file.write('\n')
        if entry[1] is '检测':
            for substring in entry[0]:
                detect_file.write(substring)
                if substring != entry[0][-1]:
                    detect_file.write(';;;;ll;;;;')
            detect_file.write('\n')
        if entry[1] is '病症':
            for substring in entry[0]:
                disease_file.write(substring)
                if substring != entry[0][-1]:
                    disease_file.write(';;;;ll;;;;')
            disease_file.write('\n')
        if entry[1] is '检查':
            for substring in entry[0]:
                inspect_file.write(substring)
                if substring != entry[0][-1]:
                    inspect_file.write(';;;;ll;;;;')
            inspect_file.write('\n')

# 关闭所有保存句子的文件
def close_output():
    cure_file.close()
    recommend_drug_file.close()
    cause_file.close()
    detect_file.close()
    disease_file.close()
    inspect_file.close()


file_list = list()  # 保存当前目录下的文件列表
for dir_path, dir_names, file_names in os.walk(r'D:\Project\Python\PythonGadgets\web_crawler\baike_spider-master\classified-merged\classified-merged-json\v2'):
    for file_name in file_names:
        file_list.append(os.path.join(dir_path, file_name))

# 逐个读取文件并抽取句子
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

# 将结果保存在文件里
save_output()
# 关闭所有输出结果的文件
close_output()


res = [('胰岛\n素可以', '治疗', '糖\n尿病'), ('同时各类、降压\n药能', '医治', '高血压')]
print(res)
new = list()
for sentence in res:
    a = list()
    for substring in sentence:
        a.append(substring.replace('\n', ' '))
    new.append(a)
print(new)
