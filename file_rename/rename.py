# 统一重命名当前文件夹下的所有文件

import os

file_names = os.listdir()
for file in file_names:
    os.rename(file, file + '.py')