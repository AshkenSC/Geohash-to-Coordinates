# 打开文件
target = open('d:\\Programs\\neo4j\\import\\people.csv', 'a', encoding='utf-8')


'''读取并写入数据'''
for i in range(10):
    source = open(str(i)+'.txt', 'r', encoding='utf-8')

    for line in source:
        if '<id>' in line:
            id = filter(str.isdigit, line)
            id = ''.join(list(id))          # 抽取id行的数字 将其转为字符串
            target.write(str(id)+'\t')
            break

    isKeyEmpty = True
    for line in source:
        if '|' in line and 'name' in line:
            target.write(line.strip('| name =')+'\t')
            isKeyEmpty = False
            break
    if isKeyEmpty:
        target.write('(empty)\t')

    isKeyEmpty = True
    for line in source:
        if '|' in line and 'birth_date' in line:
            target.write(line.strip('| birth_date =') + '\t')
            isKeyEmpty = False
            break
    if isKeyEmpty:
        target.write('(empty)\t')

    isKeyEmpty = True
    for line in source:
        if '|' in line and 'death_date' in line:
            target.write(line.strip('| death_date =') + '\t')
            isKeyEmpty = False
            break
    if isKeyEmpty:
        target.write('(empty)\t')

    isKeyEmpty = True
    for line in source:
        if '|' in line and 'birth_place' in line:
            target.write(line.strip('| birth_place =') + '\t')
            isKeyEmpty = False
            break
    if isKeyEmpty:
        target.write('(empty)\t')

    isKeyEmpty = True
    for line in source:
        if '|' in line and 'death_place' in line:
            target.write(line.strip('| death_place =') + '\t')
            isKeyEmpty = False
            break
    if isKeyEmpty:
        target.write('(empty)\t')

    isKeyEmpty = True
    for line in source:
        if '|' in line and 'predecessor' in line:
            target.write(line.strip('| predecessor =') + '\t')
            isKeyEmpty = False
            break
    if isKeyEmpty:
        target.write('(empty)\t')

    isKeyEmpty = True
    for line in source:
        if '|' in line and 'successor' in line:
            target.write(line.strip('| successor =') + '\t')
            isKeyEmpty = False
            break
    if isKeyEmpty:
        target.write('(empty)\t')

    isKeyEmpty = True
    for line in source:
        if '|' in line and 'spouse' in line:
            target.write(line.strip('| spouse =') + '\t')
            isKeyEmpty = False
            break
    if isKeyEmpty:
        target.write('(empty)\t')

    isKeyEmpty = True
    for line in source:
        if '|' in line and 'children' in line:
            target.write(line.strip('| children =') + '\t\n')
            isKeyEmpty = False
            break
    if isKeyEmpty:
        target.write('(empty)\t\n')

    source.close()
    print('条目载入完成：' + str(i))
target.close()