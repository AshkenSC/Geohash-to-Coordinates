# encoding:utf-8
from parser1 import HtmlParser
from utils import Set, Dict
from queue import Queue
from threading import Thread, Timer
from time import sleep, time
import json, os, fire

class Spider(object):
    def __init__(self, worker_num=10, chunk_size=10000, log_interval=600,
                 data_dir='data', log_dir='log'):
        self.chunk_size = chunk_size
        self.log_interval = log_interval
        self.urls = Queue()
        self.results = Queue()
        self.url_cache = Set()
        self.name_cache = Set()
        self.black_urls = Set()
        self.black_cache = Dict()
        self.chunk_num = 0
        self.parser = HtmlParser(home='https://baike.baidu.com')

        self.last = 0
        self.state = 1

        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        self.data_dir = data_dir
        self.log_dir = log_dir

        self.writer = Thread(target=self._write)
        self.logger = Timer(log_interval, self._log)
        self.spiders = [Thread(target=self._scrap) for _ in range(worker_num)]


    def start(self, url):
        new_urls, new_data = self.parser.parse(url)
        self.results.put(new_data)
        self.url_cache.add(url)
        self.name_cache.add(new_data['name'])
        for url in new_urls:
            self.urls.put(url)
        
        self.logger.start()
        self.writer.start()
        for spider in self.spiders:
            spider.start()
        
    def _write(self):
        """只使用self.results
        """
        while self.state:
            self.chunk_num += 1
            n = 0
            with open(os.path.join(self.data_dir, '{}.json'.format(self.chunk_num)), 'wb') as fp:
                while n < self.chunk_size:
                    if not self.results.empty():
                        result = self.results.get()
                        line = json.dumps(result, ensure_ascii=False) + '\n'
                        fp.write(line.encode('utf8'))
                        n += 1
                    else:
                        sleep(10)

    def _log(self):
        now = len(self.name_cache)
        increase = now - self.last
        self.last = now
        if increase == 0:
            self.state = 0
            print('Exit: no entities scraped in this round.')
            exit()
        else:
            with open(os.path.join(self.log_dir, 'log'), 'ab+') as fp:
                message = '新增词条数量：{}，已抓取词条数量：{}；已获取url数量：{}，缓存任务数量：{}，缓存结果数量：{}.'.format(
                    increase, now, len(self.url_cache), self.urls._qsize(), self.results._qsize(),
                ) + '\n'
                fp.write(message.encode('utf8'))
        timer = Timer(self.log_interval, self._log)
        timer.start() 

    def _scrap(self):
        while self.state:
            if not self.urls.empty():
                url = self.urls.get()
                try:
                    new_urls, new_data = self.parser.parse(url)
                except:
                    self.url_cache.remove(url)
                    # 多次请求不成功的url加入黑名单
                    if url not in self.black_cache:
                        self.black_cache[url] = 1
                    self.black_cache[url] += 1
                    if self.black_cache[url] >= 3:
                        self.black_urls.add(url)
                    continue
                name = new_data['name']
                if name not in self.name_cache:
                    self.name_cache.add(name)
                    # TODO:添加筛选条件
                    if '病毒' in new_data['labels'] or '微生物' in new_data['labels']\
                    or '传染病' in new_data['summary'] or '病原体' in new_data['summary'] \
                    or '肺炎' in new_data['summary'] or '感染' in new_data['summary'] \
                    or '传染' in new_data['summary'] or 'RNA病毒' in new_data['summary'] \
                    or 'DNA病毒' in new_data['summary'] or '冠状病毒' in new_data['summary'] \
                    or '免疫' in new_data['summary'] or '呼吸系统' in new_data['summary']:
                        self.results.put(new_data)
                        print('获取条目：' + name)
                    else:
                        print("\033[0;31m%s\033[0m" %('放弃条目 ' + name + ' :分类不符'))
                        #print('放弃条目 ' + name + ':没有属性信息或分类不符')
                for url in new_urls:
                    if url not in self.url_cache and url not in self.black_urls:
                        self.url_cache.add(url)
                        self.urls.put(url)
            else:
                sleep(10)


def main(worker_num=20,
         chunk_size=10000,
         log_interval=600,
         data_dir='data',
         log_dir='log',
         #start_url='https://baike.baidu.com/item/姚明/28'):
         start_url='https://baike.baidu.com/item/2019%E6%96%B0%E5%9E%8B%E5%86%A0%E7%8A%B6%E7%97%85%E6%AF%92'):
         #start_url='https://baike.baidu.com/wikitag/taglist?tagId=76625'):


    spider = Spider(
        worker_num=worker_num,
        chunk_size=chunk_size,
        log_interval=log_interval,
        data_dir=data_dir,
        log_dir=log_dir,
    )
    spider.start(start_url)


if __name__ == '__main__':
    fire.Fire(main)
