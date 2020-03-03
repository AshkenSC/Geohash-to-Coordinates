# 将李强的百科数据分类后添加到现有分类json中

# 打开李强文件，遍历条目
# 对每个条目，根据名单检查其类别，确定待放进去的类别
# 在对应类别json中检查是否已经存在条目，如果不存在放进对应的分类json

import json
SOURCE = r'f:\Projects\corona\data\lizhiqiang\LIZHIQIANG.json'

# {0:{细菌，杆菌，。。。}, 1:{疾病，心脏病，。。。}}
old_ctg_table = dict()
full_ctg_table = dict()
full_ctg_table['bacteria'] = set()
full_ctg_table['disease'] = set()
full_ctg_table['drug'] = set()
full_ctg_table['inspection'] = set()
full_ctg_table['specialty'] = set()
full_ctg_table['symptom'] = set()
full_ctg_table['virus'] = set()

# 读取老数据词条名
def load_old_table():
    global old_ctg_table
    
    old_ctg_table['bacteria'] = set()
    bacteria_source = open('classified-merged/classified-merged-json/v1/bacteria.json', 'r', encoding='utf-8')
    for json_line in bacteria_source:
        line = json.loads(json_line)
        old_ctg_table['bacteria'].add(line['name'])
    bacteria_source.close()
    print('原bacteria条目名单载入完成')

    old_ctg_table['disease'] = set()
    disease_source = open('classified-merged/classified-merged-json/v1/disease.json', 'r', encoding='utf-8')
    for json_line in disease_source:
        line = json.loads(json_line)
        old_ctg_table['disease'].add(line['name'])
    disease_source.close()
    print('原disease条目名单载入完成')

    old_ctg_table['drug'] = set()
    drug_source = open('classified-merged/classified-merged-json/v1/drug.json', 'r', encoding='utf-8')
    for json_line in drug_source:
        line = json.loads(json_line)
        old_ctg_table['drug'].add(line['name'])
    drug_source.close()
    print('原drug条目名单载入完成')

    old_ctg_table['inspection'] = set()
    inspection_source = open('classified-merged/classified-merged-json/v1/inspection.json', 'r', encoding='utf-8')
    for json_line in inspection_source:
        line = json.loads(json_line)
        old_ctg_table['inspection'].add(line['name'])
    inspection_source.close()
    print('原inspection条目名单载入完成')

    old_ctg_table['specialty'] = set()
    specialty_source = open('classified-merged/classified-merged-json/v1/specialty.json', 'r', encoding='utf-8')
    for json_line in specialty_source:
        line = json.loads(json_line)
        old_ctg_table['specialty'].add(line['name'])
    specialty_source.close()
    print('原specialty条目名单载入完成')

    old_ctg_table['symptom'] = set()
    symptom_source = open('classified-merged/classified-merged-json/v1/symptom.json', 'r', encoding='utf-8')
    for json_line in symptom_source:
        line = json.loads(json_line)
        old_ctg_table['symptom'].add(line['name'])
    symptom_source.close()
    print('原symptom条目名单载入完成')

    old_ctg_table['virus'] = set()
    virus_source = open('classified-merged/classified-merged-json/v1/virus.json', 'r', encoding='utf-8')
    for json_line in virus_source:
        line = json.loads(json_line)
        old_ctg_table['virus'].add(line['name'])
    virus_source.close()
    print('原virus条目名单载入完成')

# 读取完整数据词条名
def load_full_table():
    global full_ctg_table

    bacteria_source = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_bacteria.txt', 'r', encoding='utf-8')
    for line in bacteria_source:
        full_ctg_table['bacteria'].add(line.strip('\n'))
    bacteria_source.close()
    print('完整bacteria条目名单载入完成')

    disease_source = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_disease.txt', 'r', encoding='utf-8')
    for line in disease_source:
        full_ctg_table['disease'].add(line.strip('\n'))
    disease_source.close()
    print('完整disease条目名单载入完成')

    drug_source = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_drug.txt', 'r', encoding='utf-8')
    for line in drug_source:
        full_ctg_table['drug'].add(line.strip('\n'))
    drug_source.close()
    print('完整drug条目名单载入完成')

    inspection_source = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_inspection.txt', 'r', encoding='utf-8')
    for line in inspection_source:
        full_ctg_table['inspection'].add(line.strip('\n'))
    inspection_source.close()
    print('完整inspection条目名单载入完成')

    specialty_source = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_specialty.txt', 'r', encoding='utf-8')
    for line in specialty_source:
        full_ctg_table['specialty'].add(line.strip('\n'))
    specialty_source.close()
    print('完整specialty条目名单载入完成')

    symptom_source = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_symptom.txt', 'r', encoding='utf-8')
    for line in symptom_source:
        full_ctg_table['symptom'].add(line.strip('\n'))
    symptom_source.close()
    print('完整symptom条目名单载入完成')

    virus_source = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_virus.txt', 'r', encoding='utf-8')
    for line in virus_source:
        full_ctg_table['virus'].add(line.strip('\n'))
    virus_source.close()
    print('完整virus条目名单载入完成')
    
# 确定当前条目应该放到哪个分类里
# 如果条目不在full_table里，返回-1
def find_category(name, full_table):
    for sub_table in full_table.items():
        if name in sub_table[1]:
            return sub_table[0]
    return -1

# 必须满足：条目在full_table里，但不在old_table里
def is_existed(name, old_table):
    for sub_table in old_table.items():
        if name in sub_table[1]:
            return True
    return False

# 载入完整词条名单
load_full_table()
# 载入原词条名单
load_old_table()

# 载入李强数据源
# 待更新数据文件
bacteria_file = open('classified-merged/classified-merged-json/v1/bacteria.json', 'a+', encoding='utf-8')
disease_file = open('classified-merged/classified-merged-json/v1/disease.json', 'a+', encoding='utf-8')
drug_file = open('classified-merged/classified-merged-json/v1/drug.json', 'a+', encoding='utf-8')
inspection_file = open('classified-merged/classified-merged-json/v1/inspection.json', 'a+', encoding='utf-8')
specialty_file = open('classified-merged/classified-merged-json/v1/specialty.json', 'a+', encoding='utf-8')
symptom_file = open('classified-merged/classified-merged-json/v1/symptom.json', 'a+', encoding='utf-8')
virus_file = open('classified-merged/classified-merged-json/v1/virus.json', 'a+', encoding='utf-8')
files = {'bacteria':bacteria_file, 
         'disease':disease_file, 
         'drug':drug_file, 
         'specialty':specialty_file, 
         'symptom':symptom_file, 
         'virus':virus_file,
         'inspection': inspection_file,}

# 李强数据源
source = open(SOURCE, 'r', encoding='utf-8')
for json_line in source:
    line = json.loads(json_line)
    category = find_category(line['name'], full_ctg_table)
    if category != -1:
        # 若条目不在现有数据里，将其导入
        if is_existed(line['name'], old_ctg_table) is False:
            files[category].write(json_line + '\n')
            print('向' + category + '导入' + line['name'].encode('gbk', 'ignore').decode('gbk'))
        else:
            print('条目 ' + line['name'].encode('gbk', 'ignore').decode('gbk') + ' 已存在')
    else:
        print('条目 ' + line['name'].encode('gbk', 'ignore').decode('gbk') + ' 不属于任何类，舍弃')
source.close()

# 关闭待更新数据文件
bacteria_file.close()
disease_file.close()
drug_file.close()
inspection_file.close()
specialty_file.close()
symptom_file.close()
virus_file.close()
