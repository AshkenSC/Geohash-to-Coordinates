from PIL import Image, ImageSequence

# 将gif与源代码文件存放在相同目录下，并将下方cat.gif修改为要转换的文件名
im = Image.open(r'./cat.gif')
sequence = []

for f in ImageSequence.Iterator(im):
    sequence.append(f.copy())
sequence.reverse()

# 倒放gif保存在相同目录下，名为output.gif
sequence[0].save(r'./output.gif',save_all = True, append_images=sequence[1:])