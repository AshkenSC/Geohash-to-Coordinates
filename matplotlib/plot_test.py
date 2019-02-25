import matplotlib.pyplot as plt

labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
list1 = [3.2, 1.6, 6.8, 2.6, 4]
list2 = [2.3, 1.2, 3.3, 5.5, 3]

x = list(range(len(list1)))
total_width, n = 0.8, 2 #总宽度和并列柱体数
width = total_width / n

plt.bar(range(len(list1)), list1, label='part1', color=(0.7, 0.3, 0.8))
plt.bar(range(len(list1)), list2, bottom=list1, label='part2', tick_label=labels, color=(0.9, 0.9, 0.2))

# 添加标签和标题
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('bar graph')
plt.legend()

plt.show()