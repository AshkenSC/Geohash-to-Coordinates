import os
import json


# 整合所有词条的名称并且取交集
def load_entity_names():
    disease = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_disease.txt', 'r', encoding='utf-8')
    drug = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_drug.txt', 'r', encoding='utf-8')
    bacteria = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_bacteria.txt', 'r', encoding='utf-8')
    virus = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_virus.txt', 'r', encoding='utf-8')
    symptom = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_symptom.txt', 'r', encoding='utf-8')
    inspect = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_inspection.txt', 'r', encoding='utf-8')
    specialty = open(r'f:\Projects\corona\ngrams_baidu\entity_names\new_specialty.txt', 'r', encoding='utf-8')

    # 载入别名文件，将别名放入实体名库中
    alias_bacteria = open('alias/alias_bacteria.json', 'r', encoding='utf-8')
    alias_disease = open('alias/alias_disease.json', 'r', encoding='utf-8')
    alias_drug = open('alias/alias_drug.json', 'r', encoding='utf-8')
    alias_virus = open('alias/alias_virus.json', 'r', encoding='utf-8')

    for line in disease:
        print('正在载入：' + line.encode('gbk', 'ignore').decode('gbk'))
        disease_set.add(line.strip('\n'))
    for line in drug:
        print('正在载入：' + line.encode('gbk', 'ignore').decode('gbk'))
        drug_set.add(line.strip('\n'))
    for line in bacteria:
        print('正在载入：' + line.encode('gbk', 'ignore').decode('gbk'))
        bacteria_set.add(line.strip('\n'))
    for line in virus:
        print('正在载入：' + line.encode('gbk', 'ignore').decode('gbk'))
        virus_set.add(line.strip('\n'))
    for line in symptom:
        print('正在载入：' + line.encode('gbk', 'ignore').decode('gbk'))
        symptom_set.add(line.strip('\n'))
    for line in inspect:
        print('正在载入：' + line.encode('gbk', 'ignore').decode('gbk'))
        inspection_set.add(line.strip('\n'))
    for line in specialty:
        print('正在载入：' + line.encode('gbk', 'ignore').decode('gbk'))
        specialty_set.add(line.strip('\n'))

    # 载入别名
    alias_bacteria_json = json.load(alias_bacteria)
    for alias_list in alias_bacteria_json.values():
        for alias in alias_list:
            bacteria_set.add(alias)
    alias_disease_json = json.load(alias_disease)
    for alias_list in alias_disease_json.values():
        for alias in alias_list:
            disease_set.add(alias)
    alias_drug_json = json.load(alias_drug)
    for alias_list in alias_drug_json.values():
        for alias in alias_list:
            drug_set.add(alias)
    alias_virus_json = json.load(alias_virus)
    for alias_list in alias_virus_json.values():
        for alias in alias_list:
            virus_set.add(alias)

    disease.close()
    drug.close()
    bacteria.close()
    virus.close()
    symptom.close()
    inspect.close()
    specialty.close()

def addtoset(file, data):
    with open(file, 'r') as f:
        i = f.readline()
        i = i.split('\n')[0]
        data.add(i)
        i = f.readline()
        while(i != ''):
            i = i.split('\n')[0]
            data.add(i)
            i = f.readline()

def preprocess(summary):
    length = len(summary)
    flag = '0'*length
    dict1 = {}
    for i in range(length):
        dict1[i] = 'O'
    return dict1

def find_in_set(string):
    global disease_set
    global virus_set
    global bacteria_set
    global symptom_set
    global specialty_set
    global inspection_set
    global drug_set
    if string in disease_set:
        return '1'
    if string in virus_set:
        return '2'
    if string in bacteria_set:
        return '3'
    if string in symptom_set:
        return '4'
    if string in specialty_set:
        return '5'
    if string in inspection_set:
        return '6'
    if string in drug_set:
        return '7'
    return '0'

def value_modification(start,len,dict_mark):
    for i in range(start+len,start):
        if dict_mark[i] == 'O':
            return False
    return True

marks = {'1':("B-DIS", "I-DIS"),
        '2':("B-VIR", "I-VIR"),
        '3':("B-BAC", "I-BAC"),
        '4':("B-SYM", "I-SYM"),
        '5':("B-SPE", "I-SPE"),
        '6':("B-INS", "I-INS"),
        '7':("B-DRU", "I-DRU")
        } 

def mark_the_dict(start_point,length,type1,dict1):
    global marks
    if type1 == '0':
        return dict1
    dict1[start_point] = marks[type1][0]
    if length > 1:
        for j in range(start_point+1,start_point+length):
            dict1[j] = marks[type1][1]
    return dict1

def analyze(data_str):
    length = len(data_str) 
    iteration = min(length,10)
    dict_mark = preprocess(data_str)
    for i in range(1,iteration+1):
        # print(i)
        for j in range(0,length-i+1):
            str_tem = data_str[j:j+i]
            num_set = find_in_set(str_tem)
            flag_mod = value_modification(j,i,dict_mark)
            if flag_mod:
                mark_the_dict(j,i,num_set,dict_mark)
    return dict_mark

def write_to_f(fp,summary,dict_res):
    count = 0
    if len(summary) > 0:
        for i in range(len(summary)):
            count = count + 1
            if summary[i] == ' ':
                continue
            fp.write(str(summary[i]) + ' ' + dict_res[i] +'\n')
            if count == 100 or summary[i] in '。；':
                fp.write(' '+'\n')


disease_set = set()
drug_set = set()
bacteria_set = set()
virus_set = set()
symptom_set = set()
inspection_set = set()
specialty_set = set()
sets = [disease_set, drug_set, bacteria_set, virus_set, symptom_set, inspection_set, specialty_set]

# 载入集合，求并集
load_entity_names()
totaldata = set()
for subset in sets:
    totaldata = totaldata | subset
print('集合求解完成')

titlecached = set()
count = 0
filenum = 0

path = os.getcwd() 
filelist = []
fp1 = open(r'NER/baidu/train.txt','w', encoding='utf-8')
fp2 = open(r'NER/baidu/test.txt','w', encoding='utf-8')
fp3 = open(r'NER/baidu/dev.txt','w', encoding='utf-8')

for dirpath,dirnames,filenames in os.walk(r'D:\Project\Python\PythonGadgets\web_crawler\baike_spider-master\classified-merged\classified-merged-json\v2'):
    for filename in filenames:
        filelist.append(os.path.join(dirpath,filename))
for file in filelist:
    if file.endswith('.json'):
        print('New file of train')
        print(filenum)
        print(file)
        filenum = filenum + 1
        with open(os.path.join('classified-merged/classified-merged-json/v2/', file), 'r', encoding='utf-8') as f:
            i = f.readline()
            data = json.loads(i,strict=False)
            title = data['name']
            if title in totaldata:
                summary = data['summary']
                dict_summmary = preprocess(summary)
                dict_res = analyze(summary)
                if count % 10 == 1:
                    write_to_f(fp2,summary,dict_res)
                elif count % 10 == 2 or count % 10 == 3:
                    write_to_f(fp3,summary,dict_res)
                else:
                    write_to_f(fp1,summary,dict_res)

            i = f.readline()
            while(i != ''):
                count = count + 1
                if count % 1000 == 0:
                    print(count)
                data = json.loads(i,strict=False)
                title = data['name']
                if title in totaldata:
                    summary = data['summary']
                    dict_summmary = preprocess(summary)
                    dict_res = analyze(summary)
                    if count % 10 == 1:
                        write_to_f(fp2,summary,dict_res)
                    elif count % 10 == 2 or count % 10 == 3:
                        write_to_f(fp3,summary,dict_res)
                    else:
                        write_to_f(fp1,summary,dict_res)
                i = f.readline()
fp1.close()
fp2.close()
fp3.close()
