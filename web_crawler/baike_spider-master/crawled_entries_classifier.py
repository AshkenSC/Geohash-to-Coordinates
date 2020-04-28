# 从爬取的json数据中筛选分类

import json

# json数据源路径
SOURCE = 'data\\4.json'

# 查找数据中是否存在某主题关键字
# wordlist: 关键字列表
# datalist: 在指定的summary或者labels中找寻关键字
def find_keyword(wordlist, datalist):
    for word in wordlist:
        if word in datalist:
            return True
    return False

# 打开各类别词条JSON文件对象
others = open('others.json', 'a+', encoding='utf-8')
disease = open('disease.json', 'a+', encoding='utf-8')
virus = open('virus.json', 'a+', encoding='utf-8')
bacteria = open('bacteria.json', 'a+', encoding='utf-8')
drug = open('drug.json', 'a+', encoding='utf-8')
symptom = open('symptom.json', 'a+', encoding='utf-8')
inspection = open('inspection.json', 'a+', encoding='utf-8')
# 文件对象列表
files = [others, symptom, drug, inspection, disease, virus, bacteria]
# 分类类别
category_name = ['其他', '症状', '药物', '医学检查', '疾病', '病毒', '细菌']
# 分类计数
category_count = [0 for i in range(7)]

# 各类别标签关键词
bacteria_keywords = ['菌']
disease_keywords = ['传染病', '肺炎']
drug_keywords = ['抗生素', '处方药', '非处方药']
inspection_keywords = ['影像学','造影','医学检查','医学影像','影像医学','影像检查','医学诊断']
symptom_keywords = ['临床症状', '症状', '综合征']
virus_keywords = ['病毒', '病原体']


# 处理顺序：症状，药物（中药label），检查科目，疾病label，病毒label，细菌label

# 读取并筛选json数据
with open(SOURCE, encoding='utf-8') as source:
    for json_line in source:  # 对于多行的json必须逐行读取
        line = json.loads(json_line)    # 载入一行json数据
        # 分类
        ctg = 0     # 初始分类：其他
        if ('临床' in line['summary'] and '症状' in line['summary']) \
                or '综合征' in line['summary']:
            ctg = 1     # 症状
        elif (find_keyword(drug_keywords, line['summary']) or \
                '科学百科中医药分类' in line['labels']) and \
                not find_keyword(['疾病', '科学百科疾病症状分类'], line['labels']):
            ctg = 2     # 药物
        elif find_keyword(inspection_keywords, line['summary']):
            ctg = 3     # 医学检查
        elif find_keyword(['疾病', '科学百科疾病症状分类'], line['labels']):
            if '病毒' in line['name']:
                ctg = 5     # 词条名带病毒，划分为病毒
            elif '菌' in line['name']:
                ctg = 6     # 词条名带菌，划分为菌类
            else:
                ctg = 4     # 疾病
        elif '病毒' in line['labels']:
            ctg = 5     # 病毒
        elif '细菌' in line['labels']:
            ctg = 6     # 细菌

        # 根据分类写入不同文件
        files[ctg].write(json.dumps(line, ensure_ascii=False) + '\n')
        category_count[ctg] += 1
        print(('写入条目： ' + line['name'] + \
               ' 属于：' + category_name[ctg]).encode('GBK', 'ignore').decode('GBk'))

# 关闭所有文件
print('写入完成，结果统计：')
for i in range(7):
    print(category_name[i] + ': ' + str(category_count[i]) + '个')
for file in files:
    file.close()