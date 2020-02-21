
import requests
from bs4 import BeautifulSoup
import bs4
import lxml
import os
import re
import json
from urllib.parse import urljoin, quote, unquote

'''
data1 = set()
data2 = set()
data3 = set()

with open('E:\Monash\Coronavirus\crawler\seperateclass\医学百科_疾病jiao.txt', 'r') as f:
    i = f.readline()
    i = i.split('\n')[0]
    data1.add(i)
    i = f.readline()
    while(i != ''):
        i = i.split('\n')[0]
        data1.add(i)
        i = f.readline()

with open('E:\Monash\Coronavirus\crawler\seperateclass\医学百科_病毒jiao.txt', 'r') as f:
    i = f.readline()
    i = i.split('\n')[0]
    data2.add(i)
    i = f.readline()
    while(i != ''):
        i = i.split('\n')[0]
        data2.add(i)
        i = f.readline()

with open('E:\Monash\Coronavirus\crawler\firstrounddata\医学百科_细菌jiao', 'r') as f:
    i = f.readline()
    i = i.split('\n')[0]
    data3.add(i)
    i = f.readline()
    while(i != ''):
        i = i.split('\n')[0]
        data3.add(i)
        i = f.readline()


wholedata = data1 | data2 | data3
'''

# 整合所有词条的名称并且取交集
disease = open('classified-merged/pure_names/pure_names_multisource/disease.txt', 'r', encoding='utf-8')
drug = open('classified-merged/pure_names/pure_names_multisource/drug.txt', 'r', encoding='utf-8')
bacteria = open('classified-merged/pure_names/pure_names_multisource/bacteria.txt', 'r', encoding='utf-8')
virus = open('classified-merged/pure_names/pure_names_multisource/virus.txt', 'r', encoding='utf-8')
symptom = open('classified-merged/pure_names/pure_names_multisource/symptoms.txt', 'r', encoding='utf-8')
inspect = open('classified-merged/pure_names/pure_names_multisource/inspect.txt', 'r', encoding='utf-8')
specialty = open('classified-merged/pure_names/pure_names_multisource/speciaty.txt', 'r', encoding='utf-8')

disease_set = set()
drug_set = set()
bacteria_set = set()
virus_set = set()
symptom_set = set()
inspect_set = set()
specialty_set = set()
sets = [disease_set, drug_set, bacteria_set, virus_set, symptom_set, inspect_set, specialty_set]

for line in disease:
    print('正在载入：' + line.encode('gbk', 'ignore').decode('gbk'))
    disease_set.add(line.strip('\n'))
for line in drug:
    print('正在载入：' + line.encode('gbk', 'ignore').decode('gbk'))
    drug_set.add(line.strip('\n'))
for line in bacteria:
    print('正在载入：' + line.encode('gbk', 'ignore').decode('gbk'))
    bacteria_set.add(line.strip('\n'))
for line in virus:
    print('正在载入：' + line.encode('gbk', 'ignore').decode('gbk'))
    virus_set.add(line.strip('\n'))
for line in symptom:
    print('正在载入：' + line.encode('gbk', 'ignore').decode('gbk'))
    symptom_set.add(line.strip('\n'))
for line in inspect:
    print('正在载入：' + line.encode('gbk', 'ignore').decode('gbk'))
    inspect_set.add(line.strip('\n'))
for line in specialty:
    print('正在载入：' + line.encode('gbk', 'ignore').decode('gbk'))
    specialty_set.add(line.strip('\n'))

whole_data = set()
for subset in sets:
    whole_data = whole_data | subset
print('集合求解完成')

def have_next(ele):
    try:
        ele.next()
    except:
        return False
    return True

def is_child(child, father):
    if child in father:
        return True
    seek_list = father.contents
    for i in seek_list:
        if isinstance(i, bs4.element.NavigableString):
            pass
        elif child in i:
            return True
        else:
            flag = is_child(child, i)
            if flag == True:
                return True
    return False

def get_content_between_tables(pre, nxt):
    #如果第二个table在第一个里面
    txt = ""
    if is_child(nxt, pre):
        cur = pre.next_element
        while cur != nxt and cur is not None:
            if isinstance(cur, bs4.element.NavigableString):
                txt += cur
            cur = cur.next_element
    #类似并列关系
    else:
        #先找到pre结束的下一个元素
        cur = pre.next_element
        while is_child(cur, pre):
            cur = cur.next_element
        #获取内容
        while cur != nxt and cur is not None:
            if isinstance(cur, bs4.element.NavigableString):
                txt += cur
            cur = cur.next_element
    return txt

def findrelation(page_source, title):
    # re.sub(被替换对象的正则表达式，要替换成什么，待处理的字符串）
    PATTERN1 = r'<a target=_blank href="/item/[a-zA-Z0-9%/-]*" data-lemmaid="[0-9]*">[-+/a-zA-Z0-9\u4e00-\u9fa5]*</a>'
    PATTERN2 = r'<a target=_blank href="/item/[a-zA-Z0-9%/-]*">[-+/a-zA-Z0-9\u4e00-\u9fa5]*</a>'
    print('正在寻找关系，词条：' + title.encode('gbk', 'ignore').decode('gbk'))
    page_source = re.sub(title, '<a href="/w/' + title+ '" >'+ title + '</a>', page_source)
    page_source = re.sub('[这其它]', '<a href="/w/' + title+ '" >'+ title + '</a>', page_source)
    html = BeautifulSoup(page_source, 'lxml')
    url = html.find_all('a')    # 未经筛选的URL，包含杂质
    # for link in url:
    #     # URL筛选，去掉所有不是词条链接的URL
    #     if re.match(PATTERN1, str(link)) is None or re.match(PATTERN2, str(link)) is None:
    #         url.remove(link)
    texts = []
    for i in range(len(url)-1):
        if i == 297:    #'以孢子繁殖的陆生性较强的原核生物'
            print(str(i))
        txt = get_content_between_tables(url[i], url[i+1] )
        reg1 = r'[!。； ：,.?:;\n]'
        pattern = re.compile(reg1)
        if len(pattern.findall(txt)) < 1:
            if len(url[i].contents)>0 and len(url[i+1].contents)>0:
                line = 'head:' +  unquote(str(url[i].contents[0])) +  '\t'+ '\t'+'tail' + unquote(str(url[i+1].contents[0])) + '\t'+ '\t'+'rel:'+  str(txt)
                #if unquote(str(url[i]['href']).split('/w/')[1]) in whole_data or unquote(str(url[i + 1]['href']).split('/w/')[1]) in whole_data:
                texts.append(line)
                print('找到关系：' + line.encode('gbk', 'ignore').decode('gbk'))
    return texts


files = os.listdir('classified-merged/classified-merged-json/v1')[:-1]
fp1 = open('relationships/relationship_disease_filter.txt', 'w', encoding='utf-8')
fp2 = open('relationships/relationship_virus_filter.txt', 'w', encoding='utf-8')
fp3 = open('relationships/relationship_bacteria_filter.txt', 'w', encoding='utf-8')
for file in files:
    with open(os.path.join('classified-merged/classified-merged-json/v1', file), 'r', encoding='utf-8') as f:
        i = f.readline()
        # print(single_file)
        data = json.loads(i, strict=False)
        title = data['name']
        if 'html' in data.keys():
            page_source = data['html']
            lines = findrelation(page_source, title.encode('gbk', 'ignore').decode('gbk'))
            print('寻找关系：' + title)
            if title[-1] in '病炎症' and '分类' not in title:
                fp1.write(title + '\n')
                if len(lines) > 0:
                    for i in lines:
                        fp1.write(str(i) + '\n')
            if title[-2:] == '病毒' and '分类' not in title:
                fp2.write(title + '\n')
                if len(lines) > 0:
                    for i in lines:
                        fp2.write(str(i) + '\n')
            if title[-1] == '菌' and '分类' not in title:
                fp3.write(title + '\n')
                if len(lines) > 0:
                    for i in lines:
                        fp3.write(str(i) + '\n')
            i = f.readline()
        while (i != ''):
            data = json.loads(i, strict=False)
            title = data['name']
            if 'html' in data.keys():
                page_source = data['html']
                lines = findrelation(page_source, title)
                if title[-1] in '病炎症' and '分类' not in title:
                    fp1.write(title + '\n')
                    if len(lines) > 0:
                        for i in lines:
                            fp1.write(str(i) + '\n')
                if title[-2:] == '病毒' and '分类' not in title:
                    fp2.write(title + '\n')
                    if len(lines) > 0:
                        for i in lines:
                            fp2.write(str(i) + '\n')
                if title[-1] == '菌' and '分类' not in title:
                    fp3.write(title + '\n')
                    if len(lines) > 0:
                        for i in lines:
                            fp3.write(str(i) + '\n')
            i = f.readline()
fp1.close()
fp2.close()
fp3.close()


