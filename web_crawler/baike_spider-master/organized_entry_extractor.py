'''
数据源重新提取规整

1. 读取名单
2. 读取两个json：名单对应的json，others.json。存为一个字典，键值对是 名称：数据
3. 遍历名单，对应json读取，读取失败再从others读取。如还是未读取成功的词条，单独记录在txt
'''

'''
4. 执行attribute_extraction 1到2
5. 保存规整化提取结果，保存失败txt
'''

'''
4. 执行get_triple
5. 保存规整化执行结果，保存失败txt
'''

import json

NAME_LIST = 'classified-merged/pure_names/organized/virus_names2.txt'
JSON_SOURCE_CLASS = 'classified-merged/classified-merged-json/virus.json'
JSON_SOURCE_OTHERS = 'classified-merged/classified-merged-json/others.json'
OUTPUT_TRIPLES = 'classified-merged/triples_fused_v3/virus_triples_fused.txt'
NOT_FOUND = 'classified-merged/triples_fused_v3/virus_notfound.txt'

# 按名单提取数据
namelist = list()
name_list_source = open(NAME_LIST, 'r', encoding='utf-8')
for line in name_list_source:
    namelist.append(line.strip('\n'))

# 读取json数据，保存为字典，键值对为 词条名：数据
data_dict = dict()
json_data_class = open(JSON_SOURCE_CLASS, 'r', encoding='utf-8')
print('开始从本类json中读取数据')
for json_line in json_data_class:
    line = json.loads(json_line)
    data_dict[line['name']] = line
    print('载入条目：', end='')
    print(line['name'].encode('gbk','ignore').decode('gbk'))
print('开始从others.json读取数据')
json_data_others = open(JSON_SOURCE_OTHERS, 'r', encoding='utf-8')
for json_line in json_data_others:
    line = json.loads(json_line)
    data_dict[line['name']] = line
    print('载入条目：', end='')
    print(line['name'].encode('gbk','ignore').decode('gbk'))

# 遍历名单，从json数据中做对应提取，并保存未找到的词条名单
classified = dict()
missing = list()
for name in namelist:
    if name in data_dict.keys():
        classified[name] = data_dict[name]
    else:
        print("\033[0;31m%s\033[0m" % ('缺失条目：' + name).encode('gbk','ignore').decode('gbk'))
        missing.append(name.encode('gbk','ignore').decode('gbk'))

# 提取三元组
triples = list()    # 保存三元组
triple_cnt = 0
for entity in classified.items():
    if entity[1]['info']:
        for key, value in entity[1]['info'].items():
            value.replace('\n', ' ')  # 替换value里的换行
            new_triple = (entity[1]['name'], key, value)
            triples.append(new_triple)
            # 输出新增三元组
            print('新增三元组：', end='')
            print(new_triple.__str__().encode('GBK', 'ignore').decode('GBk'))
            triple_cnt += 1
print('读取完毕，共导入三元组' + str(triple_cnt) + '个')

# 输出三元组
output_triple = open(OUTPUT_TRIPLES, 'w', encoding='utf-8')
triple_cnt = 1
for triple in triples:
    output_triple.write(triple[0] + ';;;;ll;;;;' + triple[1] + ';;;;ll;;;;' + triple[2] + '\n')
    print('正在写入第' + str(triple_cnt) + '个三元组')
    triple_cnt += 1
output_triple.close()
print('三元组写入完毕')

# 输出未找到词条
not_found = open(NOT_FOUND, 'w', encoding='utf-8')
for name in missing:
    not_found.write(name + '\n')
print('未找到词条已经保存')

