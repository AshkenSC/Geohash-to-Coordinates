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
import opencc

# 整合所有词条的名称并且取交集
def load_entity_names():
    disease = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_disease.txt', 'r', encoding='utf-8')
    drug = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_drug.txt', 'r', encoding='utf-8')
    bacteria = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_bacteria.txt', 'r', encoding='utf-8')
    virus = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_virus.txt', 'r', encoding='utf-8')
    symptom = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_symptom.txt', 'r', encoding='utf-8')
    inspect = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_inspection.txt', 'r', encoding='utf-8')
    specialty = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_specialty.txt', 'r', encoding='utf-8')

    # 载入别名文件，将别名放入实体名库中
    alias_bacteria = open('alias/alias_bacteria.json', 'r', encoding='utf-8')
    alias_disease = open('alias/alias_disease.json', 'r', encoding='utf-8')
    alias_drug = open('alias/alias_drug.json', 'r', encoding='utf-8')
    alias_virus = open('alias/alias_virus.json', 'r', encoding='utf-8')

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

    # 载入别名
    alias_bacteria_json = json.load(alias_bacteria)
    for alias_list in alias_bacteria_json.values():
        for alias in alias_list:
            bacteria_set.add(alias)
    alias_disease_json = json.load(alias_disease)
    for alias_list in alias_disease_json.values():
        for alias in alias_list:
            disease_set.add(alias)
    alias_drug_json = json.load(alias_drug)
    for alias_list in alias_drug_json.values():
        for alias in alias_list:
            drug_set.add(alias)
    alias_virus_json = json.load(alias_virus)
    for alias_list in alias_virus_json.values():
        for alias in alias_list:
            virus_set.add(alias)

    disease.close()
    drug.close()
    bacteria.close()
    virus.close()
    symptom.close()
    inspect.close()
    specialty.close()

# 用于替换别名
def sub_alias(title, page):
    if title in aliases.keys():
        if len(aliases[title]) > 0:
            for alias in aliases[title]:
                print('替换别名：' + alias.encode('gbk', 'ignore').decode('gbk') + ' --> ' + title.encode('gbk', 'ignore').decode('gbk'))
                page = re.sub(alias, '<a href="/w/' + title + '" >' + title + '</a>', page)
    return page

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

def head_tail_strip(head, tail):
    # 写函数删除head tail中一些头尾词，例如Special: Template: （页面不存在）

    # 删除页面不存在
    if re.match(r'(.*)(（页面不存在）)', head) is not None:
        head = re.match(r'(.*)(（页面不存在）)', head)[1]
    if re.match(r'(.*)(（页面不存在）)', tail) is not None:
        tail = re.match(r'(.*)(（页面不存在）)', tail)[1]

    # 删除Special:
    if re.match(r'(Special:)(.*)', head) is not None:
        head = re.match(r'(Special:)(.*)', head)[2]
    if re.match(r'(Special:)(.*)', tail) is not None:
        tail = re.match(r'(Special:)(.*)', tail)[2]

    # 删除Template:
    if re.match(r'(Template:)(.*)', head) is not None:
        head = re.match(r'(Template:)(.*)', head)[2]
    if re.match(r'(Template:)(.*)', tail) is not None:
        tail = re.match(r'(Template:)(.*)', tail)[2]

    # 删除Wikipedia:
    if re.match(r'(Wikipedia:)(.*)', head) is not None:
        head = re.match(r'(Wikipedia:)(.*)', head)[2]
    if re.match(r'(Wikipedia:)(.*)', tail) is not None:
        tail = re.match(r'(Wikipedia:)(.*)', tail)[2]

    # 删除尾部括号注释
    if re.match(r'(.*)([(].*[)])', head) is not None:
        head = re.match(r'(.*)([(].*[)])', head)[1]
    if re.match(r'(.*)([(].*[)])', tail) is not None:
        tail = re.match(r'(.*)([(].*[)])', tail)[1]

    # 繁体转换
    c = opencc.OpenCC('t2s')
    head = c.convert(head)
    tail = c.convert(tail)

    return head, tail

def findrelation(page_source, title):
    # re.sub(被替换对象的正则表达式，要替换成什么，待处理的字符串）
    PATTERN1 = r'<a target=_blank href="/item/[a-zA-Z0-9%/-]*" data-lemmaid="[0-9]*">[-+/a-zA-Z0-9\u4e00-\u9fa5]*</a>'
    PATTERN2 = r'<a target=_blank href="/item/[a-zA-Z0-9%/-]*">[-+/a-zA-Z0-9\u4e00-\u9fa5]*</a>'
    #print('正在寻找关系，词条：' + title.encode('gbk', 'ignore').decode('gbk'))
    page_source = re.sub(title, '<a href="/w/' + title+ '" >'+ title + '</a>', page_source)
    page_source = re.sub('[这其它|他们|它们]', '<a href="/w/' + title+ '" >'+ title + '</a>', page_source)
    #page_source = sub_alias(title, page_source)    # 将网页里的别名替换
    html = BeautifulSoup(page_source, 'lxml')
    url = html.find_all('a')    # 未经筛选的URL，包含杂质
    # URL筛选，去掉所有不是词条链接的URL
    # for link in url:
    #     if re.match(PATTERN1, str(link)) is None or re.match(PATTERN2, str(link)) is None:
    #         url.remove(link)
    texts = []
    for i in range(len(url)-1):
        txt = get_content_between_tables(url[i], url[i+1])
        reg1 = r'[\-!。，；：,.?:;/／\n|、（）()<> ]'
        ban = r'Wikipedia|百科|隐私|维基|[<>]'   # 筛选头尾禁止出现的关键字
        pattern = re.compile(reg1)
        if len(pattern.findall(txt)) < 1 and \
            len(re.findall(ban, str(url[i].contents))) < 1 and len(re.findall(ban, str(url[i+1].contents))) < 1 and\
            txt != '' and \
            re.match(reg1, txt) is None and \
            url[i].contents != url[i+1].contents:
            if len(url[i].contents)>0 and len(url[i+1].contents)>0:
                if 'title' not in url[i].attrs.keys() or 'title' not in url[i + 1].attrs.keys():
                    print('title不存在')
                    continue
                if unquote(str(url[i]['title'])) == '' or unquote(str(url[i + 1]['title'])) == '':
                    print('head 或 tail 为空')
                    continue
                if unquote(str(url[i]['title'])) == unquote(str(url[i + 1]['title'])):
                    print('head tail相同：' + unquote(str(url[i + 1]['title'])).encode('gbk', 'ignore').decode('gbk'))
                    continue
                if txt == '':
                    print('rel为空')
                    continue
                # 如果head或tail头尾部含有多余信息（页面不存在），去除之
                head = unquote(str(url[i]['title']))
                tail = unquote(str(url[i + 1]['title']))
                head, tail = head_tail_strip(head, tail)
                line = head + ';;;;ll;;;;' + tail + ';;;;ll;;;;' + str(txt).replace('\n', ' ')
                #if unquote(str(url[i]['href']).split('/w/')[1]) in whole_data or unquote(str(url[i + 1]['href']).split('/w/')[1]) in whole_data:
                texts.append(line)
                print('找到关系：' + line.encode('gbk', 'ignore').decode('gbk'))
            if title in whole_data:
                # TODO： 计算A的pre、AB之间、A的next三段文本的gram，并储存于同一个文件中
                calculate(re.split(r'[，。；,.;]', str(url[i].previous_sibling))[-1])
                calculate(str(url[i].next_sibling))
                calculate(re.split(r'[，。；,.;]', str(url[i + 1].next_sibling))[0])
    return texts


disease_set = set()
drug_set = set()
bacteria_set = set()
virus_set = set()
symptom_set = set()
inspect_set = set()
specialty_set = set()
sets = [disease_set, drug_set, bacteria_set, virus_set, symptom_set, inspect_set, specialty_set]

# 载入集合，求并集
load_entity_names()
whole_data = set()
for subset in sets:
    whole_data = whole_data | subset
print('集合求解完成')

ngrams = dict()
for i in range(0,50):
    ngrams[i] = dict()

# 载入别名文件
alias_source = open('alias/alias.json', 'r', encoding='utf-8')
aliases = dict()
for json_line in alias_source:
    line = json.loads(json_line)
    for entry in line.items():
        aliases[entry[0]] = entry[1]
alias_source.close()

# 打开要写入结果的文件
files = os.listdir('f:/Projects/corona/wiki_data/xml')[:]
fp1 = open('relationships/wiki_relationship_disease_filter1.txt', 'w', encoding='utf-8')
fp2 = open('relationships/wiki_relationship_virus_filter1.txt', 'w', encoding='utf-8')
fp3 = open('relationships/wiki_relationship_bacteria_filter1.txt', 'w', encoding='utf-8')
fp4 = open('relationships/wiki_relationship_drug_filter1.txt','w', encoding='utf-8')
fp5 = open('relationships/wiki_relationship_symptom_filter1.txt','w', encoding='utf-8')
fp6 = open('relationships/wiki_relationship_inspection_filter1.txt','w', encoding='utf-8')
fp7 = open('relationships/wiki_relationship_specialty_filter1.txt','w', encoding='utf-8')
for file in files:
    print('正在载入XML……')
    with open(os.path.join('f:/Projects/corona/wiki_data/xml', file), 'r', encoding='utf-8') as f:
        print('XML载入完成')

        pages = dict()  # 以字典（title:html）保存当前XML中的页面
        title = ''
        isReadingPage = False
        for line in f:
            if isReadingPage is False:
                page_source = ''
            if '<page>' in line and isReadingPage is False:
                isReadingPage = True
            page_source += line
            if '</page>' in line and isReadingPage is True:
                isReadingPage = False
                pages[title] = page_source
                print('完成读取页面 ' + title.encode('gbk', 'ignore').decode('gbk'))
            # 如果读到标题页面，则获取title
            if re.match(r'(<title>)(.*)(</title>)', line.strip('\n')) is not None:
                title = re.match(r'(<title>)(.*)(</title>)', line)[2]
                # 去除title尾部，并转为简体字
                c = opencc.OpenCC('t2s')
                title = c.convert(title)
                title = re.match(r'(.*)( - 中文维基百科【维基百科中文版网站】)', title)[1]

        # 抽取页面中的句子。页面被存放在pages里
        for title, page_source in pages.items():
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

# 写入ngram文件
#writegramstofile(r'relationships\\ngrams', ngrams)
fp1.close()
fp2.close()
fp3.close()


