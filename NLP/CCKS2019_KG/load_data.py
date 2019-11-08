# 打开文件
target = open('d:\\Programs\\neo4j\\import\\people.csv', 'a', encoding='utf-8')

'''
name
country
birth_date
birth_place
death_date
death_place

predecessor
successor
spouse
children
'''

'''读取并写入数据'''
i = 0
for i in range(500):
    source = open(str(i)+'.txt', 'r', encoding='utf-8')
    is_Id_done = False
    for line in source:
        if '<id>' in line and is_Id_done is False:
            id = filter(str.isdigit, line)
            target.write(str(id)+'\t')
            is_Id_done = True
        else:
            break

        for j in range(9):
            if j % 9 == 0:
                if '| name =' in line:
                    target.write(line.strip('|name =')+'\t')
                else:
                    target.write('(empty)\t')
                continue

            if j % 9 == 1:
                if '| birth_date =' in line:
                    target.write(line.strip('| birth_date =') + '\t')
                else:
                    target.write('(empty)\t')
                continue

            if j % 9 == 2:
                if '| birth_place =' in line:
                    target.write(line.strip('| birth_date =') + '\t')
                else:
                    target.write('(empty)\t')
                continue

            if j % 9 == 3:
                if '| death_date =' in line:
                    target.write(line.strip('| death_date =') + '\t')
                else:
                    target.write('(empty)\t')
                continue

            if j % 9 == 4:
                if '| death_place =' in line:
                    target.write(line.strip('| death_place =') + '\t')
                else:
                    target.write('(empty)\t')
                continue

            if j % 9 == 5:
                if '| predecessor =' in line:
                    target.write(line.strip('| predecessor =') + '\t')
                else:
                    target.write('(empty)\t')
                continue

            if j % 9 == 6:
                if '| successor =' in line:
                    target.write(line.strip('| successor =') + '\t')
                else:
                    target.write('(empty)\t')
                continue

            if j % 9 == 7:
                if '| spouse =' in line:
                    target.write(line.strip('| spouse =') + '\t')
                else:
                    target.write('(empty)\t')
                continue

            if j % 9 == 8:
                if '| children =' in line:
                    target.write(line.strip('| children =') + '\t')
                else:
                    target.write('(empty)\t')
                target.write('\n')
                continue
    source.close()
target.close()