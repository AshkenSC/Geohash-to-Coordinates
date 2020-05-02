# 从JSON数据源中提取出每个实体的来源HTML/XML文件

import json
import os

# JSON数据源路径
SOURCE = 'classified-merged/classified-merged-json/v2/virus.json'
# HTML导出文件夹路径
DEST = r'classified-merged/classified-merged-json/v2/HTML/virus'

def extract_html(source_path, dest_path):
    source_file = open(source_path, 'r', encoding='utf-8')
    page_num = 1
    for json_line in source_file:
        line = json.loads(json_line)
        print('正在写入：' + line['name'].encode('gbk', 'ignore').decode('gbk'))

        f = open(os.path.join(dest_path, '{}.htm'.format(page_num)), 'w', encoding='utf-8')
        f.write(line['html'])
        f.close()

        print('第{}页面保存完毕'.format(page_num))
        page_num += 1
    source_file.close()

if __name__ == '__main__':
    extract_html(SOURCE, DEST)