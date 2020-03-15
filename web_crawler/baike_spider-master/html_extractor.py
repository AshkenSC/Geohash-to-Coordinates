# 从HTML页中提取JSON格式的数据

import os
from bs4 import BeautifulSoup
import json
import re

SOURCE = r"f:\Projects\corona\hudong_data\html\symptom"
DEST = r'f:\Projects\corona\hudong_data\json\symptom.json'

# 1. 将XML文件分割为page并单独保存

def split_page(file_path, dest_path):
    pages = list()
    xml = open(file_path + r'\entity_pages_12.xml','r', encoding='utf-8')
    isReadingPage = False
    page_num = 1
    for line in xml:
        if isReadingPage is False:
            page = list()
        if '<page>' in line and isReadingPage is False:
            isReadingPage = True
        page.append(line)
        if '</page>' in line and isReadingPage is True:
            isReadingPage = False
            pages.append(page)
            print('第{}页面载入完毕'.format(page_num))
            page_num += 1
    xml.close()

    page_num = 81844
    for page in pages:
        f = open(os.path.join(dest_path, '{}.htm'.format(page_num)), 'w', encoding='utf-8')
        for line in page:
            f.write(line)
        f.close()
        print('第{}页面保存完毕'.format(page_num))
        page_num += 1
    return page_num

# 2. 规格化提取每个page的信息，保存为字典
def get_new_data(soup, html):
    res_data = {}

    # get title
    title = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find('h1').get_text()
    sub_title = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find('h2')
    sub_title = sub_title.get_text() if sub_title is not None else ''
    res_data['name'] = title.strip() + sub_title.strip()

    # get summary
    summary_node = soup.find('div', class_="lemma-summary")
    if summary_node is None:
        res_data['summary'] = []
    else:
        summary_para_nodes = summary_node.find_all('div', class_='para')
        summary_paras = paras = [p.get_text().replace('\n', '').strip() for p in summary_para_nodes]
        res_data['summary'] = _clean_text('\n'.join(summary_paras))

    # get information
    info_node = soup.find('div', class_="basic-info cmn-clearfix")
    # key名与spider中调用的不一致，已更改
    if info_node is None:
        res_data['info'] = []
    else:
        name_nodes = info_node.find_all('dt', class_="basicInfo-item name")
        value_nodes = info_node.find_all('dd', class_="basicInfo-item value")
        assert len(name_nodes) == len(value_nodes), 'Number of names and values are not equal.'
        names = [_clean_text(name.get_text()).strip() for name in name_nodes]
        values = [value.get_text().strip() for value in value_nodes]
        res_data['info'] = dict(zip(names, values))

    # get contents
    nodes = soup.find_all('div', class_=['para-title level-2', 'para-title level-3', 'para'])
    res_data['contents'] = _get_contents(nodes)

    # get labels
    res_data['labels'] = []
    labels = soup.find_all('span', class_="taglist")
    for label in labels:
        res_data['labels'].append(label.get_text().strip())

    # get url
    # 对每个实体新增url属性，记录对应百科页面的url
    res_data['url'] = ''

    # get html
    res_data['html'] = html

    return res_data

# 2. 从互动百科的HTML中提取信息
def get_new_data_hudong(soup, html):
    res_data = {}

    # get title
    title = soup.find('title').get_text()
    res_data['name'] = title.strip()

    # get summary
    try:
        summary_node = soup.find('div', class_="summary").get_text().replace('\n', '').strip()
        res_data['summary'] = _clean_text(summary_node)
    except:
        res_data['summary'] = ''
        print(title.strip().encode('gbk', 'ignore').decode('gbk') + 'summary为空')

    # get contents
    # TODO 提取正文的纯文本
    nodes = soup.find_all('div', class_='content_h2')
    res_data['contents'] = _get_contents(nodes)

    # get labels
    # res_data['labels'] = []
    # labels = soup.find_all('span', class_="taglist")
    # for label in labels:
    #     res_data['labels'].append(label.get_text().strip())

    # get url
    # 对每个实体新增url属性，记录对应百科页面的url
    res_data['url'] = ''

    return res_data

def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    # new_data = get_new_data(soup, html) # 获取百度页面信息
    new_data = get_new_data_hudong(soup, html)  # 获取互动页面信息
    return new_data

def write_file(source_path, dest_path, page_num):
    output = open(dest_path, 'w', encoding='utf-8')
    for i in range(1, page_num):
        if i == 26:
            print(i)
            continue
        try:
            html_file = open(os.path.join(source_path, '{}.htm').format(i), 'r', encoding='utf-8')
        except:
            print('页码数超出了范围')
            continue
        html = ''
        for line in html_file:
            html += line
        if '您所访问的页面不存在' in html:
        # 跳过错误页
            print(str(i) + '页错误，跳过该页')
            continue
        line = json.dumps(parse(html), ensure_ascii=False) + '\n'
        output.write(line)
        print('写入词条成功:' + str(i))
    output.close()

def _clean_text(text):
    text = re.sub(r'(\u3000|\xa0)', '', text)
    text = re.sub(r'\n+', '\n', text)
    return text

def _get_contents(nodes):
    contents, splits = [], []
    for i, node in enumerate(nodes):
        if node['class'][-1] == 'level-2':
            splits.append(i)
    for i, start in enumerate(splits):
        end = splits[i + 1] if i < len(splits) - 1 else len(nodes)
        title = nodes[start].find('h2', class_='title-text').text.strip()
        has_h3 = any([n['class'][-1] == 'level-3' for n in nodes[start:end]])
        if not has_h3:
            paras = []
            for n in nodes[start:end]:
                if n['class'][-1] == 'para':
                    paras.append(_clean_text(n.text.replace('\n', '')).strip())
            content = '\n'.join(paras)
            if len(content) > 100:
                contents.append({'title': title, 'text': content.strip()})
        else:
            sub_nodes = nodes[start:end]
            _splits = []
            for ii, _node in enumerate(sub_nodes):
                if _node['class'][-1] == 'level-3':
                    _splits.append(ii)
            for ii, _start in enumerate(_splits):
                _end = _splits[ii + 1] if ii < len(_splits) - 1 else len(sub_nodes)
                sub_title = sub_nodes[_start].text.strip()
                _title = '-'.join([title, sub_title])
                _paras = []
                for n in sub_nodes[_start:_end]:
                    if n['class'][-1] == 'para':
                        _paras.append(_clean_text(n.text.replace('\n', '')).strip())
                _content = '\n'.join(_paras)
                if len(_content) > 100:
                    contents.append({'title': _title, 'text': _content.strip()})
    return contents

#page_num = split_page(SOURCE, DEST)
write_file(SOURCE, DEST, 1900)
