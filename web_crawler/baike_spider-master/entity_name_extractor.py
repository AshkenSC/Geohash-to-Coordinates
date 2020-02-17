# 用于从三元组中提取实体名称

'''
SOURCE_PATH = 'classified-merged/triples/drug-triple3819.txt'
DEST_PATH = 'classified-merged/triples_v2/drug_names.txt'

names = set()
source = open(SOURCE_PATH, 'r', encoding='utf-8')

for line in source:
    triple = line.split(';;;;ll;;;;')
    triple[0] = triple[0].strip('<')
    triple[0] = triple[0].strip('>')
    names.add(triple[0])
source.close()

dest = open(DEST_PATH, 'w', encoding='utf-8')
for name in names:
    dest.write(name + '\n')
    print(name.encode('gbk','ignore').decode('gbk'))
dest.close()
'''

# 整合所有词条的名称并且取交集
disease = open('classified-merged/pure_names/intersected/disease_names.txt', 'r', encoding='utf-8')
drug = open('classified-merged/pure_names/intersected/drug_names.txt', 'r', encoding='utf-8')
bacteria = open('classified-merged/pure_names/intersected/bacteria_names.txt', 'r', encoding='utf-8')
virus = open('classified-merged/pure_names/intersected/virus_names.txt', 'r', encoding='utf-8')

disease_set = set()
drug_set = set()
bacteria_set = set()
virus_set = set()

for line in disease:
    disease_set.add(line)
for line in drug:
    drug_set.add(line)
for line in bacteria:
    bacteria_set.add(line)
for line in virus:
    virus_set.add(line)

sets = [disease_set, drug_set, bacteria_set, virus_set]

new_file = open('classified-merged/pure_names/intersected/new_virus.txt', 'w', encoding='utf-8')
for item in sets[3]:
    new_file.write(item)
new_file.close()

print(sets[2] & sets[3])
