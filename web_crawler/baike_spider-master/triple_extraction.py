# 读取三元组数据源
source = open('classified-merged/triples_v2/1symptom-triple3395.txt', 'r', encoding='utf-8-sig')
dest = open('classified-merged/normalized_triples/normalized_symptoms.txt', 'w', encoding='utf-8-sig')

alias = {\
'名称': ['中文名','中文名称','中医学名','中文学名','别名','又称','别称','名称'],\
'病因':['常见病因','主要病因','病因'],\
'发病部位':['发病部位','常见发病部位']\
}


# 查找字典中是否有该键
def find_value(dict, wordlist):
    for key in dict.keys():
        if key in wordlist:
            return dict[key]
    return 'NULL'


# 删除词条头尾的标记字符
def strip_word(words):
    for i in range(len(words)):
        words[i] = words[i].strip('\n')
        words[i] = words[i].strip('<')
        words[i] = words[i].strip('>')
        words[i] = words[i].strip('\"')


# 将条目建立为2层嵌套字典
entries = dict()
for line in source:
    triple = line.split(';;;;ll;;;;')   # 三元组字符串转为三元素列表
    strip_word(triple)
    if triple[0] not in entries.keys():
        entries[triple[0]] = {triple[1]:triple[2]}
    else:
        entries[triple[0]][triple[1]] = triple[2]


# 整理后保存到新字典里
output = dict()
for entry in entries.items():
    output[entry[0]] = dict()
    for word in alias.keys():
        output[entry[0]][word] = find_value(entry[1], alias[word])
    # output[entry[0]]['名称'] = find_value(entry[1], alias['名称'])
    # output[entry[0]]['病因'] = find_value(entry[1], alias['病因'])
    # output[entry[0]]['发病周期'] = find_value(entry[1], alias['发病周期'])


# 输出检查结果
for entry in output.items():
    print(str(entry).encode('GBK', 'ignore').decode('GBk'))
