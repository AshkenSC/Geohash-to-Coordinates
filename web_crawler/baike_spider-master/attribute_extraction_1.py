# 属性提取 step1：从三元组中提取

import json
SOURCE = 'classified-merged/triples_v2/1disease.txt'
DEST = 'classified-merged/normalized_triples/normalized_disease.json'


'''
症状

alias = {\
'名称': ['中文名','中文名称','中医学名','中文学名','别名','又称','别称','名称'],\
'病因':['常见病因','主要病因','病因'],\
'发病部位':['发病部位','常见发病部位']\
}
'''
'''
细菌

alias = {\
'名称':['中文名','中文名称','中医学名','中文学名','别名','又称','别称','名称'],\
'科':['科'],\
'界':['界'],\
'属':['属', '属于']\
}
'''
'''
病毒

alias = {\
'名称':['中文名','中文名称','中医学名','中文学名','别名','又称','别称','名称'],\
'科':['科'],\
'目':['界'],\
'属':['属', '属于'],\
'形状':['形状', '病毒形状'],\
'传播途径':['途径', '传播途径', '感染途径', '主要传播途径']\
}
'''


alias = {\
'名称':['中文名','中文名称','中医学名','中文学名','别名','又称','别称','名称'],\
'医学专科':['就诊科室'],\
'发病部位':['发病部位','常见发病部位'],\
'临床表现':['临床表现','临床症状','症状','常见症状','主要症状'],\
'常见病因':['常见病因','主要病因','患病原因','发病原因'],\
'传染性':['传染性'],\
'病原类型':['病原类型','病原','病原中文名','病原类别']\
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
# 读取三元组数据源
source = open(SOURCE, 'r', encoding='utf-8-sig')
entries = dict()
for line in source:
    triple = line.split(';;;;ll;;;;')   # 三元组字符串转为三元素列表
    strip_word(triple)
    if triple[0] not in entries.keys():
        entries[triple[0]] = {triple[1]:triple[2]}
        print(str(triple).encode('GBK', 'ignore').decode('GBk'))
    else:
        entries[triple[0]][triple[1]] = triple[2]
source.close()

# 整理后保存到新字典里
output = dict()
for entry in entries.items():
    output[entry[0]] = dict()
    for word in alias.keys():
        output[entry[0]][word] = find_value(entry[1], alias[word])
    # output[entry[0]]['名称'] = find_value(entry[1], alias['名称'])
    # output[entry[0]]['病因'] = find_value(entry[1], alias['病因'])
    # output[entry[0]]['发病周期'] = find_value(entry[1], alias['发病周期'])


# 转为json保存，输出检查结果
for entry in output.items():
    print(str(entry).encode('GBK', 'ignore').decode('GBk'))
print(len(output.items()))

dest = open(DEST, 'w', encoding='utf-8')
json.dump(output, dest, indent=2, ensure_ascii=False)   # 设置参数确保dump后不是unicode编码
dest.close()
print('数据导出完成')


