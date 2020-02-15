# 属性提取step2：从文本中匹配内容，对第一步进行补全

import json
import re

ENTITIES = 'classified-merged/normalized_triples/normalized_virus_678.json'
CONTENT = 'classified-merged/classified-merged-json/virus.json'
DEST = 'classified-merged/normalized_triples/updated_virus.json'

regex_virus = {
    '科':['(\u5c5e\u4e8e|\u5c5e)*([\u4e00-\u9fa5]*)\u79d1'],
    '目':['(\u5c5e\u4e8e|\u5c5e)*([\u4e00-\u9fa5]*)\u76ee'],
    '属':['(\u5c5e\u4e8e|\u5c5e)*([\u4e00-\u9fa5]*)\u5c5e'],
    '形状':['(\u5448)([\u4e00-\u9fa5]*)(\u5f62)*(\u72b6)', '(\u4e3a)([\u4e00-\u9fa5]*)(\u5f62)*(\u72b6)'],
    '传播途径':['(\u901a\u8fc7)([\u4e00-\u9fa5]*)(\u7b49|\u7684)*(\u9014\u5f84)*(\u4f20\u64ad)'],
}

# 在文本里根据正则表达式找到匹配语句，如找不到则返回字符串NULL
def find_match(key, regex, text):
    if key in regex_virus.keys():
        for expression in regex[key]:
            pattern = re.compile(repr(expression))
            if pattern.match(text) is not None:
                value = pattern.match(text)
                print("\033[0;31m%s\033[0m" % '补全属性：', end='')
                print("\033[0;31m%s\033[0m" % (key + ': ' + value).encode('GBK', 'ignore').decode('GBk'))
                return value
            else:
                return 'NULL'

# 读取数据源
# 规整待补全的实体，存入entities里
entities_source = open(ENTITIES, 'r', encoding='utf-8-sig')
entities = json.load(entities_source)
entities_source.close()
# 用于补全的数据源，存入字典baike
baike = dict()  # 使用字典保存，访问的时候可直接通过词条名定位
content = open(CONTENT, 'r', encoding='utf-8-sig')
for json_line in content:  # 对于多行的json必须逐行读取
    line = json.loads(json_line)  # 载入一行json数据
    baike[line['name']] = line
    #print('载入条目：', end='')
    #print(line['name'].encode('GBK', 'ignore').decode('GBk'))

# 遍历entities每个实体entity，同时根据词条名字在baike数据源里找对应的summary和content
# 在summary和content的每个章节的text中进行匹配来补全
# 最终补全的结果存入entities里
for entity in entities.items():
    if entity[0] not in baike.keys():
    # 如果baike里没有这个条目，无法补全，跳过
        print("\033[0;31m%s\033[0m" % '数据库中不存在该条目，无法补全：', end='')
        print("\033[0;31m%s\033[0m" % entity[0].encode('GBK', 'ignore').decode('GBk'))
        continue
    for info in entity[1].items():          # 遍历当前entity每个属性，找出空属性补全
        if info[1] == 'NULL':               # info[0]为属性名，info为[1]值
            # 1. 在summary中进行匹配
            info = (info[0], find_match(info[0], regex_virus, baike[entity[0]]['summary']))
            if info[1] != 'NULL':
                continue
            # 2. 在contents中匹配（summary未匹配成功）
            for section in baike[entity[0]]['contents']:
            # 遍历contents中的所有section，每个section由title和text组成。遍历的是text
                info = (info[0], find_match(info[0], regex_virus, section['text']))
                if info[1] != 'NULL':
                    break       # 一旦找到匹配的，就停止查找
        if info[1] == 'NULL':   # 遍历结束还没找到，报告匹配失败
            print('补全属性失败，未找到该属性的值：', end='')
            print(info[0].encode('GBK', 'ignore').decode('GBk'))

# 将补全后的entities存回json文件
dest = open(DEST, 'w', encoding='utf-8')
json.dump(entities, dest, indent=2, ensure_ascii=False)   # 设置参数确保dump后不是unicode编码
dest.close()
print('数据导出完成')








