# 匹配无dilemmaID <a target=_blank href="/item/[a-zA-Z0-9%/-]*">[-+/a-zA-Z0-9\u4e00-\u9fa5]*</a>
# 有dilemmaID <a target=_blank href="/item/[a-zA-Z0-9%/-]*" data-lemmaid="[0-9]*">[-+/a-zA-Z0-9\u4e00-\u9fa5]*</a>

# 数据结构 {实体名1:[{连接词条a:链接a}, {链接词条b:链接b}, ...], 实体名2：[{连接词条a:链接a}, {链接词条b:链接b}, ...]｝

import re
import json

regex_list = [r'(<a target=_blank href="/item/[a-zA-Z0-9%/-]*">)([-+/a-zA-Z0-9\u4e00-\u9fa5]*)(</a>)',
         r'(<a target=_blank href="/item/[a-zA-Z0-9%/-]*" data-lemmaid="[0-9]*">)([-+/a-zA-Z0-9\u4e00-\u9fa5]*)(</a>)']

result = dict()     # 保存结果的字典
source_json_file = open('classified-merged/classified-merged-json/v1/bacteria.json', 'r', encoding='utf-8')
for json_line in source_json_file:
    entity = json.loads(json_line)
    html = entity['html']
    links = list()
    for regex in regex_list:
        pattern = re.compile(regex)
        new_link = re.findall(regex, html)
        if new_link is not None:
            new_link = [entry[1] for entry in new_link]  # 删去列表元素中url其他部分，只保留词条名
            links.append(new_link)
            print(entity['name'].encode('GBK', 'ignore').decode('GBk'), end='')
            print('新增链接')
        result[entity['name']] = links
source_json_file.close()

json_line = json.dumps(result, indent=2,ensure_ascii=False)
out_json_file = open('classified-merged/organized_entities/v2/bacteria_links.json', 'w', encoding='utf-8')
out_json_file.write(json_line)
out_json_file.close()

