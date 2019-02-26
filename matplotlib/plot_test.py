import matplotlib.pyplot as plt

labels = 'Andy','Mary','Tom','Susan'
data = [30,40,45,20]

explode = (0.1,0.2,0.3,0.1)
plt.pie(data, explode=explode, labels=labels, autopct='%.2f')

plt.title('pie chart')
plt.axis('equal')
plt.show()

 #0.1表示将Hogs那一块凸显出来
#autopct='%1.1f%%',shadow=False,startangle=90

#startangle表示饼图的起始角度