# 将获得的ngram文字片段进行统计，获得x_detail文件

import os

ngrams = dict()

for i in range(0,50):
    ngrams[i] = dict()

def processtxt(origin):
    lists = origin.split(';;;;ll;;;;')
    print(repr(lists).encode('gbk', 'ignore').decode('gbk'))
    pre = lists[0]
    rel = lists[2]
    next = lists[4]
    line = origin
    return pre, rel, next, line

def calculate(data_str,line):
    length = len(data_str) 
    iteration = min(length,50)
    for i in range(0,iteration):
        for j in range(0,length-i+1):
            if i == 6 and j == 1 and '一般术前半小时至1小时给予' in line:
                pass#print(str(i) + ' ' + str(j))
            if data_str[j:j+i] not in ngrams[i].keys():
                ngrams[i][data_str[j:j+i]] = set()
                ngrams[i][data_str[j:j+i]].add(line)
                print(str(i) + ' ' + str(j))
            else:
                ngrams[i][data_str[j:j+i]].add(line)
                print(str(i) + ' ' + str(j))

def writegramstofile(dir,ngrams):
    for i in ngrams.keys():
        length = str(i)
        with open(os.path.join(dir, 'detail/{}_detail.txt'.format(i)),'w', encoding='utf-8') as f1:
            with open(os.path.join(dir, 'brief/{}_brief.txt'.format(i)),'w', encoding='utf-8') as f2:
                sorted_dict = sorted(ngrams[i].items(),key=lambda x:len(x[1]), reverse = True)
                for j in sorted_dict:
                    rel = j[0]
                    number = len(j[1])
                    line = 'calculate: \t' + str(rel) + '\t' + str(number)
                    f1.write(line + '\n')
                    f2.write(line + '\n')
                    for k in j[1]:
                        line = k.split(';;;;ll;;;;')
                        line = line[0] + '\t' + line[1] + '\t' +  line[2] + '\t' +  line[3] + '\t' +  line[4]
                        f1.write(line + '\n')
                        # f1.write(k + '\n')

with open(r'relationships/relationship_disease_filter1.txt', 'r', encoding='utf-8') as f:
    i = f.readline()
    i = i.split('\n')[0]
    pre, rel, next, line = processtxt(i)
    if pre:
        calculate(pre,line)
    if rel:
        calculate(rel, line)
    if next:
        calculate(next, line)
    i = f.readline()
    cnt = 0
    for i in f:
    #while(i != ''):
        if ';;;;ll;;;;' not in i:
            continue
        i = i.split('\n')[0]
        pre, rel, next, line = processtxt(i)
        if pre:
            calculate(pre, line)
        if rel:
            calculate(rel, line)
        if next:
            calculate(next, line)
        #i = f.readline()


writegramstofile(r'ngrams_addline/disease', ngrams)