from PIL import Image, ImageSequence

# ��gif��Դ�����ļ��������ͬĿ¼�£������·�cat.gif�޸�ΪҪת�����ļ���
im = Image.open(r'./cat.gif')
sequence = []

for f in ImageSequence.Iterator(im):
    sequence.append(f.copy())
sequence.reverse()

# ����gif��������ͬĿ¼�£���Ϊoutput.gif
sequence[0].save(r'./output.gif',save_all = True, append_images=sequence[1:])