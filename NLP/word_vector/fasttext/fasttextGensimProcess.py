from gensim.models import FastText

'''数据集去除多余字符'''
import codecs
import re

f=codecs.open('clean_data.txt', "a+",'utf-8')

prompt = 0
for line in open("test.txt", encoding='utf-8'):
    newline = re.sub('[·a-zA-Z0-9_]','',line)
    f.write(newline)
    # 输出显示工作进度
    print('removing redundant characters, processing: ' + str(prompt))
    prompt += 1

f.close()


'''数据集导入'''
# 将文本行存入列表
'''prompt = 1
lines = []
for line in open("clean_data.txt", encoding='utf-8'):
    lines.append(line.split(' '))
    print("appending line " + str(i))
    prompt += 1
'''