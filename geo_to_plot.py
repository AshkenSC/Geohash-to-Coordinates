import pygeohash as pgh
from openpyxl import load_workbook
import matplotlib.pyplot as plt


# step1: 载入工作表
workbook = load_workbook('source_excel.xlsx')
sheet = workbook.get_sheet_by_name("Sheet1")


# 指定表格数据读取范围
start_loc_range = sheet['A2':'A51']
end_loc_range = sheet['B2':'B51']
# 读取数据
start_loc_geohash = []
end_loc_geohash = []
# 读取start_loc列
for row_of_cell in start_loc_range:
    for cell in row_of_cell:
        start_loc_geohash.append(cell.value)
# 读取end_loc列
for row_of_cell in end_loc_range:
    for cell in row_of_cell:
        end_loc_geohash.append(cell.value)


# step2: 转换为坐标
start_loc_coord = []
end_loc_coord = []
for i in range(len(start_loc_geohash)):
    decode = pgh.decode(start_loc_geohash[i])
    start_loc_coord.append(decode)
for i in range(len(end_loc_geohash)):
    decode = pgh.decode(end_loc_geohash[i])
    end_loc_coord.append(decode)


# step3: 生成散点图
for i in range(len(start_loc_coord)):
    plt.scatter(start_loc_coord[i][0], start_loc_coord[i][1], color='blue', s=50)
    plt.scatter(end_loc_coord[i][0], end_loc_coord[i][1], color='red', s=50)
plt.show()
