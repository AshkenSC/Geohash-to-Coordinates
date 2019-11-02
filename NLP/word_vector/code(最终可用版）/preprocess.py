'''去除多余字符'''
def remove_char(write_file, read_file):
    import codecs
    import re

    f=codecs.open(write_file, "w",'utf-8')

    i = 0
    for line in open(read_file, encoding='utf-8'):
        newline = re.sub('[·a-zA-Z0-9_,]','',line)
        f.write(newline)
        # 输出显示工作进度
        print('removing redundant characters, processing: ' + str(i))
        i += 1

    f.close()


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
        print('traditional to simplified, processing: ' + str(prompt))
        prompt += 1

    file.close()


'''去除多余字符（适用于未分词数据集）'''
def remove_and_cut(writefile, readfile):
    import codecs
    import re
    import jieba

    f = codecs.open(writefile, 'w', 'utf-8')

    prompt = 0
    for line in open(readfile, encoding='utf-8'):
        for i in re.sub('[·a-zA-Z0-9:/]', '', line).split(' '):
            if i != '':
                data = list(jieba.cut(i, cut_all=False))
                readline = ' '.join(data) + '\r\n'  # 在一行末尾，添加\r\n而不仅是\n实现换行
                f.write(readline)

        # 输出显示工作进度
        print('removing redundant characters, processing: ' + str(prompt))
        prompt += 1

    f.close()