# 测试用代码，除了考虑实体AB之间的文本外，还考虑了A之前，B之后的文本，并计算这三个文本的NGRAM

# 从url文本中的超链接提取实体之间的文本，从而获取关系
# 计算ngram

import requests
from bs4 import BeautifulSoup
import bs4
import lxml
import os
import re
import json
from urllib.parse import urljoin, quote, unquote

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

ngrams = dict()

for i in range(0,50):
    ngrams[i] = dict()

# 计算ngram
def calculate(data_str):
    length = len(data_str)
    iteration = min(length,50)
    for i in range(0, iteration):
        for j in range(0, length-i+1):
            if data_str[j:j+i] not in ngrams[i].keys():
                ngrams[i][data_str[j:j+i]] = 1
            else:
                ngrams[i][data_str[j:j+i]] = ngrams[i][data_str[j:j+i]] +  1

# 导出ngram
def writegramstofile(dir,ngrams):
    for i in ngrams.keys():
        length = str(i)
        with open(os.path.join(dir, '{}.txt'.format(i)),'w', encoding='utf-8') as f:
            sorted_dict = sorted(ngrams[i].items(),key=lambda x:x[1], reverse = True)
            for j in sorted_dict:
                number = j[0]
                rel = j[1]
                line = str(j)
                f.write(line + '\n')

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
    #print('正在寻找关系，词条：' + title.encode('gbk', 'ignore').decode('gbk'))
    page_source = re.sub(title, '<a href="/w/' + title+ '" >'+ title + '</a>', page_source)
    page_source = re.sub('[这其它|他们|它们]', '<a href="/w/' + title+ '" >'+ title + '</a>', page_source)
    html = BeautifulSoup(page_source, 'lxml')
    url = html.find_all('a')    # 未经筛选的URL，包含杂质
    # URL筛选，去掉所有不是词条链接的URL
    # for link in url:
    #     if re.match(PATTERN1, str(link)) is None or re.match(PATTERN2, str(link)) is None:
    #         url.remove(link)
    texts = []
    for i in range(len(url)-1):
        txt = get_content_between_tables(url[i], url[i+1])
        reg1 = r'[!。，；：,.?:;\n|、（）<> ]'
        ban = r'百度|百科|隐私|[<>]'   # 筛选头尾禁止出现的关键字
        pattern = re.compile(reg1)
        if len(pattern.findall(txt)) < 1 and \
            len(re.findall(ban, str(url[i].contents))) < 1 and len(re.findall(ban, str(url[i+1].contents))) < 1 and\
            txt != '' and \
            re.match(reg1, txt) is None and \
            url[i].contents != url[i+1].contents:
            if len(url[i].contents)>0 and len(url[i+1].contents)>0:
                if '纤维杆菌门' in re.split(r'[，。；,.;]', str(url[i].previous_sibling))[-1]:
                    print(str(url[i].previous_element)[-1])
                line = unquote(re.split(r'[，。；,.;>]', str(url[i].previous_element))[-1]) + ';;;;ll;;;;' + \
                       unquote(str(url[i].contents[0])) + ';;;;ll;;;;' + \
                       unquote(str(url[i].next_sibling)) + ';;;;ll;;;;' + \
                       unquote(str(url[i + 1].contents[0])) + ';;;;ll;;;;' + \
                       unquote(re.split(r'[，。；,.;<]', str(url[i + 1].next_element))[0])
                    #if unquote(str(url[i]['href']).split('/w/')[1]) in whole_data or unquote(str(url[i + 1]['href']).split('/w/')[1]) in whole_data:
                texts.append(line)
                print('找到关系：' + line.encode('gbk', 'ignore').decode('gbk'))
            if title in whole_data:
                if title == '高血钾' and i == 139:
                    print(title + str(i))
                # TODO： 计算A的pre、AB之间、A的next三段文本的gram，并储存于同一个文件中
                calculate(re.split(r'[，。；,.;]', str(url[i].previous_sibling))[-1])
                calculate(str(url[i].next_sibling))
                calculate(re.split(r'[，。；,.;]', str(url[i + 1].next_sibling))[0])
    return texts


files = os.listdir('classified-merged/classified-merged-json/v1')[:-1]
fp1 = open('relationships/relationship_disease_filter1.txt', 'w', encoding='utf-8')
fp2 = open('relationships/relationship_virus_filter1.txt', 'w', encoding='utf-8')
fp3 = open('relationships/relationship_bacteria_filter1.txt', 'w', encoding='utf-8')
fp4 = open('relationships/relationship_drug_filter1.txt','w', encoding='utf-8')
fp5 = open('relationships/relationship_symptom_filter1.txt','w', encoding='utf-8')
fp6 = open('relationships/relationship_inspect_filter1.txt','w', encoding='utf-8')
fp7 = open('relationships/relationship_specialty_filter1.txt','w', encoding='utf-8')
for file in files:
    with open(os.path.join('classified-merged/classified-merged-json/v1', file), 'r', encoding='utf-8') as f:
        i = f.readline()
        # print(single_file)
        data = json.loads(i, strict=False)
        title = data['name']
        if 'html' in data.keys():
            page_source = data['html']
            lines = findrelation(page_source, title.encode('gbk', 'ignore').decode('gbk'))
            if title in disease_set:
                if len(lines) > 0:
                    for i in lines:
                        fp1.write(str(i) + '\n')
            if title in virus_set:
                if len(lines) > 0:
                    for i in lines:
                        fp2.write(str(i) + '\n')
            if title in bacteria_set:
                if len(lines) > 0:
                    for i in lines:
                        fp3.write(str(i) + '\n')
            if title in drug_set:
                if len(lines) > 0:
                    for i in lines:
                        fp4.write(str(i) + '\n')
            if title in symptom_set:
                if len(lines) > 0:
                    for i in lines:
                        fp5.write(str(i) + '\n')
            if title in inspect_set:
                if len(lines) > 0:
                    for i in lines:
                        fp6.write(str(i) + '\n')
            if title in specialty_set:
                if len(lines) > 0:
                    for i in lines:
                        fp7.write(str(i) + '\n')
            i = f.readline()
        while i != '':
            data = json.loads(i, strict=False)
            title = data['name']
            if 'html' in data.keys():
                page_source = data['html']
                lines = findrelation(page_source, title)
                if title in disease_set:
                    #fp1.write(title + '\n')
                    if len(lines) > 0:
                        for i in lines:
                            fp1.write(str(i) + '\n')
                if title in virus_set:
                    #fp2.write(title + '\n')
                    if len(lines) > 0:
                        for i in lines:
                            fp2.write(str(i) + '\n')
                if title in bacteria_set:
                    #fp3.write(title + '\n')
                    if len(lines) > 0:
                        for i in lines:
                            fp3.write(str(i) + '\n')
                if title in drug_set:
                    # fp4.write(title + '\n')
                    if len(lines) > 0:
                        for i in lines:
                            fp4.write(str(i) + '\n')
                if title in symptom_set:
                    # fp4.write(title + '\n')
                    if len(lines) > 0:
                        for i in lines:
                            fp5.write(str(i) + '\n')
                if title in inspect_set:
                    # fp4.write(title + '\n')
                    if len(lines) > 0:
                        for i in lines:
                            fp6.write(str(i) + '\n')
                if title in specialty_set:
                    # fp4.write(title + '\n')
                    if len(lines) > 0:
                        for i in lines:
                            fp7.write(str(i) + '\n')
            i = f.readline()
# 写入ngram文件
writegramstofile(r'relationships\\ngrams', ngrams)
fp1.close()
fp2.close()
fp3.close()


