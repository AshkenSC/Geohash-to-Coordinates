'''注意：在不同文件夹下要修改文件地址'''

#用于print()正常显示文本内容
'''
import sys,io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")
'''

# 数据源文件地址
DATA_PATH = 'zhwiki-latest-pages-articles1.xml-p1p162886'
#DATA_PATH = 'test.xml-p1p3'


'''将每个条目保存在独立文件中'''
def save_pages(file_path):
    # 读取数据源
    data = open(file_path, 'r', encoding='utf-8')
    print('原始数据载入完成。')

    i = 0
    isWriting= False    # 是否处于写入文件状态
    for line in data:
        #print(line)
        if line == '  <page>\n' and isWriting == False:
            # 开始新的条目
            newpage = open(str(i)+'.txt', 'w', encoding='utf-8')
            newpage.write(line)
            isWriting = True
        elif line == '  </page>\n' and isWriting == True:
            # 当前条目结束
            newpage.write(line)
            newpage.close()
            isWriting = False
            print('已保存条目：' + str(i))
            i = i + 1
        elif isWriting == True:
            # 正在写入正文
            newpage.write(line)


'''将繁体转为简体'''
# opecc Python安装命令： pip install opencc-python-reimplemented

# t2s - 繁体转简体（Traditional Chinese to Simplified Chinese）
# s2t - 简体转繁体（Simplified Chinese to Traditional Chinese）
# mix2t - 混合转繁体（Mixed to Traditional Chinese）
# mix2s - 混合转简体（Mixed to Simplified Chinese）

def chinese_t2s(writefile, readfile):
    import opencc

    cc = opencc.OpenCC('t2s')       # t2s: Traditional to Simplified, 繁体转简体

    # 遇到 UnicodeEncodeError: ‘gbk’ codec can’t encode character，由于GBK和UTF-8编码冲突
    # 添加参数设置： encoding='utf-8'
    file = open(writefile, 'w', encoding='utf-8')
    prompt = 0      # 用于输出显示工作进度的变量

    for line in open(readfile, 'rb').readlines():
        # l = cc.convert(l).encode('utf8', 'ignore')
        # file.write(l + '\n')
        l = line.decode('utf8', 'ignore').rstrip(u'\n')
        file.write(cc.convert(l) + u'\n')

        # 输出显示工作进度
        #print('traditional to simplified, processing: ' + str(prompt))
        prompt += 1

    file.close()


'''筛选词条'''
def filter():
    cnt = 0 # 记录人物词条总数
    output = open('people_list.txt', 'w', encoding='utf-8')
    for i in range(75137):
        page = open('./pages/'+str(i)+'.txt', 'r', encoding='utf-8')
        for line in page:
            if '[[Category' in line:
                if '人物' in line or '学者' in line:
                    output.write(str(i)+'\n')
                    print('词条' + str(i) + '是人物词条')
                    page.close()
                    cnt += 1
                    break
    print('人物词条总数：' + str(cnt))
    output.close()


'''复制过滤后的文件'''
def copy_filtered():
    from shutil import copyfile
    i = 0
    people = open('people_list.txt', 'r', encoding='utf-8')
    for index in people:
        id = index.strip('\n')
        copyfile('./pages/'+id+'.txt', './people/'+str(i)+'.txt')
        print(str(id)+'写入完成')
        i += 1


'''执行处理'''
#save_pages(DATA_PATH)

# 总数：75137
# for i in range(1001):
#     chinese_t2s('./pages/'+str(i)+'.txt', str(i)+'.txt')
#     print('条目'+str(i)+'转换完成')

# 人物词条总数：3150
#filter()
copy_filtered()
