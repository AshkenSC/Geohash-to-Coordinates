import os
import re

import requests
import xlrd
import xlutils.copy
import xlwt
from bs4 import BeautifulSoup
from requests import RequestException


def get_html(url):
    try:
        # 添加User-Agent，放在headers中，伪装成浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
        return None
    except RequestException as e:
        print(e)
        return None

def parse_html(html, url):
    # 使用beautifulSoup进行解析
    soup = BeautifulSoup(html, 'lxml')
    # 题目
    title = soup.select('[style="font-weight:bold;"]')[0].text
    # 摘要
    abstract = soup.select('.abstract')[0].textarea
    if abstract:
        abstract = abstract.text.strip()
    else:
        abstract = ''

    # 关键词
    keyword = soup.select(
        '[title="知识脉络分析"][href="#"][onclick^="wfAnalysis"]')  # 返回列表 ^表示以什么开头 找到title=x，href=x，οnclick=x的节点
    keywords = ''
    for word in keyword:
        keywords = keywords + word.text + ';'

    # 作者
    author = soup.select('[onclick^="authorHome"]')
    if author:
        author = author[0].text

    # 作者单位
    unit = soup.select('[class^="unit_nameType"]')
    if unit:
        unit = unit[0].text

    # 母体文献
    pattern = re.compile('母体文献.*?<div class="info_right author">(.*?)</div>', re.S)
    literature = re.findall(pattern, html)
    if literature:
        literature = literature[0]
    print(literature)

    # 会议名
    # TODO
    pattern = re.compile('会议名称.*?<div class="info_right">(.*?)</div>', re.S)
    conference = pattern.findall(html)
    # if len(soup.select('[href="#"][onclick^="searchResult"]')) > 0:
    #     conference = soup.select('[href="#"][onclick^="searchResult"]')[0].text
    # else:
    #     conference = ''
    print(conference)

    # 会议时间
    pattern = re.compile('会议时间.*?<div class="info_right">(.*?)</div>', re.S)
    date = pattern.findall(html)
    if date:
        date = date[0].strip()

    # 会议地点
    pattern = re.compile('会议地点.*?<div class="info_right author">(.*?)</div>', re.S)
    address = re.findall(pattern, html)
    if address:
        address = address[0].strip()
    print(address)

    # 主办单位
    # TODO
    organizer = ''#soup.select('[href="javascript:void(0)"][onclick^="searchResult"]')
    # if organizer:
    #     organizer = organizer[0].text
    print(organizer)

    # 在线发表时间
    pattern = re.compile('在线出版日期.*?<div class="info_right author">(.*?)</div>', re.S)
    online_date = pattern.findall(html)
    if online_date:
        online_date = online_date[0].strip()

    paper = [title, abstract, keywords, author, unit, literature, conference, date, address, organizer, online_date,
             url]
    print(paper)
    return paper


def save_p(paper):
    if not os.path.exists('会议论文.xls'):
        wb = xlwt.Workbook()
        sheet = wb.add_sheet('sheet1')
        title = ['题目', '摘要', '关键词', '作者', '作者单位', '母体文献', '会议名称', '会议时间', '会议地点', '主办单位', '在线发表时间', '链接']
        for i in range(len(title)):
            sheet.write(0, i, title[i]) #在第0行写入标题
        wb.save('会议论文.xls')
    wb = xlrd.open_workbook('会议论文.xls')
    sheet = wb.sheet_by_index(0)
    rows = sheet.nrows #当前行数
    print(rows)
    ws = xlutils.copy.copy(wb)
    sheet = ws.get_sheet(0)
    for i in range(len(paper)):
        sheet.write(rows, i, paper[i])
    ws.save('会议论文.xls')

def main(url):
    # 发送请求、获取响应
    html = get_html(url)
    # 解析响应
    paper = parse_html(html, url)
    # 数据存储
    save_p(paper)