# 从HTML页中提取JSON格式的数据

import os
from bs4 import BeautifulSoup
import json

SOURCE = 'data/lizhiqiang/'
DEST = 'data/lizhiqiang/LIZHIQIANG.json'

# 1. 将XML文件分割为page并单独保存
def split_page(file_path, dest_path):
    pages = list()
    xml = open(file_path,'r', encoding='utf-8')
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

    page_num = 1
    for page in pages:
        f = open(os.path.join(dest_path, '{}.htm'.format(page_num)), 'w', encoding='utf-8')
        for line in page:
            f.write(line)
        f.close()
        print('第{}页面保存完毕'.format(page_num))
        page_num += 1


# 2. 规格化提取每个page的信息，保存为字典
def get_new_data(self, soup, html):
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
        res_data['summary'] = self._clean_text('\n'.join(summary_paras))

    # get information
    info_node = soup.find('div', class_="basic-info cmn-clearfix")
    # key名与spider中调用的不一致，已更改
    if info_node is None:
        res_data['info'] = []
    else:
        name_nodes = info_node.find_all('dt', class_="basicInfo-item name")
        value_nodes = info_node.find_all('dd', class_="basicInfo-item value")
        assert len(name_nodes) == len(value_nodes), 'Number of names and values are not equal.'
        names = [self._clean_text(name.get_text()).strip() for name in name_nodes]
        values = [value.get_text().strip() for value in value_nodes]
        res_data['info'] = dict(zip(names, values))

    # get contents
    nodes = soup.find_all('div', class_=['para-title level-2', 'para-title level-3', 'para'])
    res_data['contents'] = self._get_contents(nodes)

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

def parse(html_file):
    html = ''
    for line in html_file:
        html += line
    soup = BeautifulSoup(html, 'html.parser')
    new_data = get_new_data(soup, html)
    return new_data

def write_file(source_path, dest_path):
    output = open(dest_path, 'w', encoding='utf-8')
    for i in range(1, 5241):
        html_file = open(os.path.join(source_path, '{}.htm').format(i), 'r', encoding='utf-8')
        line = json.dumps(parse(html_file), ensure_ascii=False) + '\n'
        output.write(line)
        print('写入词条成功:' + str(i))
    output.close()

# split_page(SOURCE, DEST)
write_file(SOURCE, DEST)
