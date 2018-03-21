import csv
import pygeohash as pgh
import pandas as pd


# 读取数据
filename = 'test.csv'
df = pd.read_csv(filename)
geohash_start_loc = []
geohash_end_loc = []
for i in range(len(df.index)):
    geohash_start_loc.append(df.iloc[i][5])
    geohash_end_loc.append(df.iloc[i][6])
print("Loading complete.")

# 坐标转换
coord_start_loc = []
coord_end_loc = []
for i in range(len(geohash_start_loc)):
    decodeTemp = pgh.decode(geohash_start_loc[i])
    coord_start_loc.append(decodeTemp)
    decodeTemp = pgh.decode(geohash_end_loc[i])
    coord_end_loc.append(decodeTemp)
print("Conversion complete.")

# 坐标覆盖写入
for i in range(len(coord_start_loc)):
    df.set_value(i, col='geohashed_start_loc', value=str(coord_start_loc[i]))
    df.set_value(i, col='geohashed_end_loc', value=str(coord_end_loc[i]))
df.to_csv(filename)
print("Rewrite complete.")