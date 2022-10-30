import csv
import numpy as np
import re

file = open(r"xo stuff\xo_dict.csv", "r")
data = list(csv.reader(file, delimiter=","))
file.close()
print(list(np.fromstring(data[0][0][1:len(data[0][0])-1:], dtype=int, sep=' ')))
print(float(data[0][1]))