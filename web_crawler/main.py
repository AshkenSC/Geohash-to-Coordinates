import re
import time

import requests
from requests import RequestException

import conference


def get_page(url):
    try:
        # 添加User-Agent，放在headers中，伪装成浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
        return None
    except RequestException as e:
        print(e)
        return None


def get_url(html, type):
    url_list = []
    pattern = re.compile("this.id,'(.*?)'", re.S)
    ids = pattern.findall(html)

    for id in ids:
        if type == 'c':
            url_list.append('http://www.wanfangdata.com.cn/details/detail.do?_type=conference&id=' + id)
        elif type == 'd':
            url_list.append('http://www.wanfangdata.com.cn/details/detail.do?_type=degree&id=' + id)
        else:
            url_list.append('http://www.wanfangdata.com.cn/details/detail.do?_type=perio&id=' + id)

    return url_list


def get_info(url,type):
    if type == 'c':
        conference.main(url)

    # elif type == 'd':
    #     degree.main(url)
    # else:
    #     perio.main(url)


if __name__ == '__main__':
    key_word = input('请输入搜索关键词：')  # 可以交互输入 也可以直接指定
    type = input('请选择论文类型(p:期刊 c:会议 d:学位 )：')
    # 从哪一页开始爬 爬几页
    start_page = int(input('请输入爬取的起始页：'))
    page_num = int(input('请输入要爬取的页数(每页默认20条)：'))

    if type == 'c':
        base_url = 'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=conference&pageSize=20&page={}&searchWord={}&showType=detail&order=common_sort_time&isHit=&isHitUnit=&firstAuthor=false&navSearchType=conference&rangeParame='
    elif type == 'd':
        base_url = 'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=degree&pageSize=20&page={}&searchWord={}&showType=detail&order=pro_pub_date&isHit=&isHitUnit=&firstAuthor=false&navSearchType=degree&rangeParame='
    else:
        base_url = 'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=perio&pageSize=20&page={}&searchWord={}&showType=detail&order=orig_pub_date&isHit=&isHitUnit=&firstAuthor=false&navSearchType=perio&rangeParame='

    for page in range(int(start_page), int(start_page + page_num)):
        new_url = base_url.format(page, key_word)
        # 爬取当前页面 发送请求、获取响应
        html = get_page(new_url)
        # 解析响应 提取当前页面所有论文的url
        url_list = get_url(html, type)
        for url in url_list:
            # 获取每篇论文的详细信息
            get_info(url, type)
            time.sleep(2)  # 间隔2s