# 合并多次爬取产生的json数据，并删除重复项目

import json
OLD = 'processing\\baike_2761.json'
NEW = 'processing\\data4.json'

# 读取老数据词条名
old_names = list()
with open(OLD, encoding='utf-8') as f:
    for json_line in f:  # 对于多行的json必须逐行读取
        line = json.loads(json_line)
        old_names.append(line['name'])

# 读取新数据，合并
cnt = 0
old = open(OLD, 'a', encoding='utf-8')
new = open(NEW, 'r', encoding='utf-8')
for json_line in new:
    line = json.loads(json_line)
    if line['name'] not in old_names:
        print('正在写入新条目：' + line['name'])
        old.write(json.dumps(line) + '\n')
        cnt += 1
    else:
        print('该条目已存在：' + line['name'])
print('合并完成，共新增条目：' + str(cnt))

old.close()
new.close()