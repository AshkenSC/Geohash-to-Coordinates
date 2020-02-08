# 从爬取的json数据中获取格式化三元组

import json
SOURCE = 'data\\baike_2949.json'  # json数据源路径
DEST = 'baike_triple_formatted.txt' # 三元组路径

keywords = ['病毒', '微生物', '疾病', '医学', '医学术语', '科学', '科研人员', \
            '科学百科生命科学分类', '科学百科健康医疗分类', '科学百科农业科学分类']

# 读取并筛选json数据
triples = []
entities = []
deleted = []
cnt = 0
with open(SOURCE, encoding='utf-8') as f:
    for json_line in f:  # 对于多行的json必须逐行读取
        line = json.loads(json_line)
        # 判断是否是主题相关词条
        isRelated = False
        for keyword in keywords:
            if keyword in line['labels']:
                isRelated = True
                break
        if not line['labels']:  # 针对2019新冠病毒等无标签情况 设置他们为True
            isRelated = True
        # 若不相关，则存入被丢弃条目合集
        if isRelated is False:
            print('丢弃无关条目：' + line['name'])
            deleted.append(line)
            continue
        # 符合条件且infobox有信息的条目，输出三元组
        if line['info']:
            for key, value in line['info'].items():
                value.replace('\n', ' ')    # 替换value里的换行
                new_triple = (line['name'], key, value)
                triples.append(new_triple)
                entities.append(line['name'])   # 记录所有实体的名称
                # 输出新增三元组
                print('新增三元组：', end='')
                print(new_triple.__str__().encode('GBK','ignore').decode('GBk'))
                cnt += 1
    print('读取完毕，共导入三元组' + str(cnt) + '个')

# 写入三元组数据
output = open(DEST, 'w', encoding='utf-8')
cnt = 1
for triple in triples:
    # 将实体和literal格式化，实体加上<>，或literal加上""
    if triple[2] in entities:
        output.write('<' + triple[0] + '>' + ';;;;ll;;;;' + triple[1] +
                     ';;;;ll;;;;' + '<' + triple[2] + '>' + '\n')
    else:
        output.write('<' + triple[0] + '>' + ';;;;ll;;;;' + triple[1] +
                     ';;;;ll;;;;' + '\"' + triple[2] + '\"' + '\n')
    print('正在写入第' + str(cnt) + '个三元组')
    cnt += 1
output.close()
print('三元组写入完毕')

# 写入丢弃条目文件
output = open('deleted', 'w', encoding='utf-8')
for item in deleted:
    output.write(item['name'] + '\n')
output.close()
print('废弃条目写入完毕')