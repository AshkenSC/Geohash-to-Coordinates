import json

SOURCE_PATH = 'classified-merged/classified-merged-json/others.json'
DEST_PATH = 'classified-merged/classified-merged-json/filtered-drug.txt'

# 药物：
# name_key = ['丸', '液', '片', '膏', '素', '丹', '散', '剂', '贴', '粒']
# info_key = ['禁忌','不良反应','剂量', '胶囊', '疫苗']

# 疾病
name_key = ['病','炎症']
info_key = ['常见病因','发病部位','临床表现','医学专科','就诊科室','病因','发病']

# 细菌
# name_key = ['菌']
# info_key = []

# 病毒
# name_key = []
# info_key = ['传播途径']

# 找name中是否有keywords中出现的关键字
def find_keyword(name, keywords):
    for key in keywords:
        if key in name:
            return True
    return False

# 找字典中的每个键名是否出现了keywords中的关键字
# 遍历字典每个键，对每个键，又遍历keywords列表查找
def find_attribute(entry, keywords):
    for attribute in entry.keys():
        if find_keyword(attribute, keywords):
            return True
    return False

# 查询名字是否符合条件
def find_in_name(name, keywords):
    for key in keywords:
        if name[-1] == key:
            return True
    return False

# 查询infobox属性是否符合条件
def find_in_info(entry, keywords):
    for attribute in entry.keys():
        for key in keywords:
            if key in attribute:
                return True
    return False

# 找到所有符合条件的词条
result = []
source = open(SOURCE_PATH, 'r', encoding='utf-8')
for json_line in source:
    line = json.loads(json_line)
    print('读取词条：', end='')
    print(line['name'].encode('gbk', 'ignore').decode('gbk'))
    if find_in_name(line['name'], name_key):
        result.append(line['name'])
        continue
    if find_attribute(line['info'], info_key):
        result.append(line['name'])
source.close()

# 写入文件
dest = open(DEST_PATH, 'w', encoding='utf-8')
for word in result:
    print('写入：', end='')
    print(word.encode('gbk', 'ignore').decode('gbk'))
    dest.write(word + '\n')
dest.close()



