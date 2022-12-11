import pandas as pd
import numpy as np

targetCode = (81,82)
targetSclae = "중분류"
scale = {'기본부문':0,'소분류':1,'중분류':2,'대분류':3}
dataClass = pd.read_excel("2015_부문분류표.xlsx",sheet_name="상품분류표", header=2, skipfooter=31).iloc[:,[0,2,4,6]].iloc[:,[scale[targetSclae],scale['대분류']]]
dataClass = dataClass.iloc[:,[np.where(dataClass==targetCode[0])[1][0],-1]].dropna(axis=0, how='all')
sMat = np.zeros(shape=(dataClass.notna().sum()[1]+1,dataClass.notna().sum()[0]))
dataClass = dataClass.fillna(-1).to_numpy()

i=0
for j in range(sMat.shape[1]):
    if j!=0 and dataClass[j][1]!=-1:
        i+=1
        sMat[i,j]=1
    else:
        sMat[i,j]=1

for i in targetCode:
    sMat[:,np.where(dataClass==i)[0][0]]=0
    sMat[-1,np.where(dataClass==i)[0][0]]=1

print(sMat)




        

        





# print(np.where(dataClass==targetCode)[0][0])
# print(dataClass.shape)