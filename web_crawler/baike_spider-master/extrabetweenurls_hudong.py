from bs4 import BeautifulSoup
import bs4
import lxml
import os
import re
import json
from urllib.parse import urljoin, quote, unquote
import os

def clean(s):
    s = re.sub(r'/s+', '', s)
    if s.endswith('：'):
        s = s[:-1]
    s = s.replace('[', '')
    s = s.replace(']', '')
    s = s.replace('(', '')
    s = s.replace(')', '')
    return s

data1 = set()
data2 = set()
data3 = set()
data4 = set()
data5 = set()
data6 = set()
data7 = set()

name_dict = []
for i in range(1, 4):
    file_name = 'entity_names_' + str(i) + '.json'
    with open(os.path.join(r'f:/Projects/corona/hudong_data/xml/', file_name), 'r', encoding='utf-8') as f:
        name_dict.append(json.load(f))
        f.close()

with open(os.path.join('f:/Projects/corona/ngrams_baidu/entity_names/', 'new_bacteria.txt'), 'r', encoding='utf-8') as f:
    i = f.readline()
    i = i.strip('\n')
    data1.add(i)
    i = f.readline()
    while(i != ''):
        i = i.strip('\n')
        data1.add(i)
        i = f.readline()

with open(os.path.join('f:/Projects/corona/ngrams_baidu/entity_names/', 'new_disease.txt'), 'r', encoding='utf-8') as f:
    i = f.readline()
    i = i.strip('\n')
    data2.add(i)
    i = f.readline()
    while(i != ''):
        i = i.strip('\n')
        data2.add(i)
        i = f.readline()

with open(os.path.join('f:/Projects/corona/ngrams_baidu/entity_names/', 'new_drug.txt'), 'r', encoding='utf-8') as f:
    i = f.readline()
    i = i.strip('\n')
    data3.add(i)
    i = f.readline()
    while(i != ''):
        i = i.strip('\n')
        data3.add(i)
        i = f.readline()

with open(os.path.join('f:/Projects/corona/ngrams_baidu/entity_names/', 'new_inspection.txt'), 'r', encoding='utf-8') as f:
    i = f.readline()
    i = i.strip('\n')
    data4.add(i)
    i = f.readline()
    while(i != ''):
        i = i.strip('\n')
        data4.add(i)
        i = f.readline()

with open(os.path.join('f:/Projects/corona/ngrams_baidu/entity_names/', 'new_specialty.txt'), 'r', encoding='utf-8') as f:
    i = f.readline()
    i = i.strip('\n')
    data5.add(i)
    i = f.readline()
    while(i != ''):
        i = i.strip('\n')
        data5.add(i)
        i = f.readline()

with open(os.path.join('f:/Projects/corona/ngrams_baidu/entity_names/', 'new_symptom.txt'), 'r', encoding='utf-8') as f:
    i = f.readline()
    i = i.strip('\n')
    data6.add(i)
    i = f.readline()
    while(i != ''):
        i = i.strip('\n')
        data6.add(i)
        i = f.readline()

with open(os.path.join('f:/Projects/corona/ngrams_baidu/entity_names/', 'new_virus.txt'), 'r', encoding='utf-8') as f:
    i = f.readline()
    i = i.strip('\n')
    data7.add(i)
    i = f.readline()
    while(i != ''):
        i = i.strip('\n')
        data7.add(i)
        i = f.readline()

wholedata = set()
wholedata = data1 | data2 | data3 | data4 | data5 | data6 | data7

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
    for dict in name_dict:
        name_list = dict.get(title, [])
        if len(name_list) != 0:
            break
    title = clean(title)
    print("\033[0;31m%s\033[0m" % ('TITLE:' + title))
    if title == '颈椎增生':
        print(title)
    for name in name_list:
        page_source = re.sub(clean(name), '<a class = "innerlink" title = '+title+'>' + '</a>', page_source)
    page_source = re.sub('[这]', '<a class = "innerlink" title = '+title+'>'+ title + '</a>', page_source)
    page_source = re.sub('[该]', '<a class = "innerlink" title = '+title+'>' + title + '</a>', page_source)
    page_source = re.sub('[此]', '<a class = "innerlink" title = '+title+'>' + title + '</a>', page_source)
    page_source = re.sub('[它]', '<a class = "innerlink" title = '+title+'>' + title + '</a>', page_source)
    html = BeautifulSoup(page_source, 'lxml')
    url = html.find_all('a',{'class':'innerlink'})
    texts = []
    for i in range(len(url)-1):
        txt = get_content_between_tables(url[i], url[i+1])
        reg1 = r'[!。，；：,.?:;\n|、（）<> ]'
        pattern = re.compile(reg1)
        if len(pattern.findall(txt)) < 1:
            if 'title' not in url[i].attrs.keys() or 'title' not in url[i+1].attrs.keys():
                print('title不存在')
                continue
            if unquote(str(url[i]['title'])) == '' or unquote(str(url[i+1]['title'])) == '':
                print('head 或 tail 为空')
                continue
            if unquote(str(url[i]['title'])) == unquote(str(url[i+1]['title'])):
                print('head tail相同：' + unquote(str(url[i+1]['title'])).encode('gbk', 'ignore').decode('gbk'))
                continue
            if txt == '':
                print('rel为空')
                continue
            line = unquote(str(url[i]['title'])) + ';;;;ll;;;;'+ unquote(str(url[i+1]['title'])) + ';;;;ll;;;;'+ str(txt).replace('\n', ' ')
            texts.append(line)
            print(line.encode('gbk', 'ignore').decode('gbk'))
    return texts

def get_triple(relation_line):
    triple = relation_line.split(';;;;ll;;;;')
    return triple[0], triple[1], triple[2]

if __name__ == '__main__':
    wf = open(os.path.join(r'f:/Projects/corona/hudong_data/xml/', r'hudongbaike_sentence.txt'), 'a', encoding='utf-8')
    # i = 1,2 ...,12
    i = 3
    file_name = 'entity_pages_' + str(i) + '.xml'
    inner_link_dict = {}
    with open(os.path.join(r'f:/Projects/corona/hudong_data/xml/', file_name), 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
        print('正在读取页面……')
        all_page = soup.find_all('page')
        print('文件读取完成')
        for page in all_page:
            inner_link_set = set()
            if page.title:
                list = findrelation(str(page), page.title.string)
                if len(list) != 0:
                    print(len(list))
                for triple in list:
                    head, tail, rel = get_triple(triple)
                    if head in wholedata and tail in wholedata:
                        if re.search(r'[ •·]', rel) is None:
                            wf.write(triple + '\n')
                            print(triple.encode('gbk', 'ignore').decode('gbk'))
                    else:
                        print('head tail未登录：' + triple.encode('gbk', 'ignore').decode('gbk'))
