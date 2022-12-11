import pandas as pd
import numpy as np

employTable = pd.read_excel('2015-19_고용표_통합중분류_취업자수 및 근로시간.xlsx',header=5,skipfooter=5,index_col=0).drop(columns="Unnamed: 1").iloc[:,[0,2,4,6,8]].iloc[:,4]

print(employTable)