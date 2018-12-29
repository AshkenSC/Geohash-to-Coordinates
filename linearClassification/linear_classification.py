import pandas as pd
import numpy as np

# create characteristic list
column_names = ['Sample code number', 'Clump Thickness', 'Uniformity of Cell Size',
                'Uniformity of Cell Shape', 'Marginal Adhesion', 'Single Epithelial Cell Size',
                'Bare Nuclei', 'Bland Chromatin', 'Normal Nucleoli', 'Mitoses', 'Class']

# load designated data from Internet
data = pd.read_csv(
        'https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data',
        names=column_names)


# replace '?' with standard missing value
data = data.replace(to_replace='? ', value=np.nan)
# abandon data with missing value (as long as there is one dimension missing)
data = data.dropna(how='any')
# output the amount and dimension of 'data'
data.shape
