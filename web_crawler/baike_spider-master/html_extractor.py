# 从HTML页中提取JSON格式的数据
import os
SOURCE = 'data/lizhiqiang/LIZHIQIANG.xml'
DEST = 'data/lizhiqiang/'

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


# 2. 规格化提取每个page的信息

split_page(SOURCE, DEST)