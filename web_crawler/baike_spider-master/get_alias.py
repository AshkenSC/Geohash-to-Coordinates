# 获取实体名称的别名，从而用于在文本中获取更多的关系
# 读取数据源JSON，然后根据其infobox中的名称、别名信息获取别名
# 别名字典存为JSON格式

import json
import re

# 别名数据源
SOURCE = open("f:/Projects/corona/classified-merged/organized_entities/v2/updated_bacteria2.json", 'r', encoding='utf-8')
# 最终得到的别名字典
DEST = open('alias/alias_bacteria.json', 'w', encoding='utf-8')

alias_dict = dict()     # 保存别名的字典

# 读取数据源中的别名
data_source = json.load(SOURCE)
for entity in data_source.items():
    if len(entity[1].keys()) < 1:
        continue
    if entity[1]['名称'] != 'NULL':
        alias_list = re.split('[;,，、；]', entity[1]['名称'])
        alias_dict[entity[0]] = alias_list
        print(entity[0].encode('gbk', 'ignore').decode('gbk') + '别名：' + repr(alias_list).encode('gbk', 'ignore').decode('gbk'))
    else:
        alias_dict[entity[0]] = []
SOURCE.close()

# 将别名字典存为json格式
json.dump(alias_dict, DEST, ensure_ascii=False)   # 设置参数确保dump后不是unicode编码
DEST.close()