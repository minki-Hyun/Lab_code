import pandas as pd
import numpy as np

# 통합행렬
targetCode = (3,4)
targetScale = "중분류"
scale = {'기본부문':0,'소분류':1,'중분류':2,'대분류':3}
dataClass = pd.read_excel("2015_부문분류표.xlsx",sheet_name="상품분류표", header=2, skipfooter=31).iloc[:,[0,2,4,6]].iloc[:,[scale[targetScale],scale['대분류']]]
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

# 투입산출표
targetFile = "2019_투입산출표_생산자가격_통합중분류.xlsx"

# 국산거래표
domesticInteraction = pd.read_excel(targetFile,sheet_name="A표_국산거래표(생산자가격)", header=5, index_col=1).drop(columns="Unnamed: 0")
midInput = sMat@domesticInteraction.iloc[:-1,:-10].replace(" ","", regex=True).replace("\\n","", regex=True).to_numpy()@sMat.T
midDemandSum = sMat@domesticInteraction.loc[:,'중간수요계'].iloc[:-1].to_numpy()
finalDemandSum = sMat@domesticInteraction.loc[:,'최종수요계'].iloc[:-1].to_numpy()
totalDemandSum = sMat@domesticInteraction.loc[:,'총수요계'].iloc[:-1].to_numpy()

# 총거래표
totalInteraction = pd.read_excel(targetFile,sheet_name="A표_총거래표(생산자가격)", header=5, index_col=1).drop(columns="Unnamed: 0")
valueaddedCoeff = (sMat@totalInteraction.loc['부가가치계'].dropna().iloc[:-1].to_numpy())/totalDemandSum
wageCoeff = (sMat@totalInteraction.loc['피용자보수'].dropna().iloc[:-1].to_numpy())/totalDemandSum

# 고용표
targetYear = 2019
year = {2015:0,2016:1,2017:2,2018:3,2019:4}
employeeCoeff = sMat@pd.read_excel('2015-19_고용표_통합{}_취업자수 및 근로시간.xlsx'.format(targetScale),header=5,skipfooter=5,index_col=0).drop(columns="Unnamed: 1").iloc[:,[0,2,4,6,8]].iloc[:,year[targetYear]].to_numpy()/totalDemandSum

# 레온티예프 행렬
Leontieff = np.linalg.inv(np.eye(len(totalDemandSum))-(midInput@np.linalg.inv(np.diag(totalDemandSum))))
AH = midInput@np.linalg.inv(np.diag(totalDemandSum))[:,-1]

# 생산유발효과
prodEff = Leontieff[:-1,:-1]@AH[:-1]

# 부가가치유발효과
vaEff = np.diag(valueaddedCoeff[:-1])@prodEff

# 취업유발효과
empEff = np.diag(employeeCoeff[:-1])@prodEff

# 임금유발효과
wageEff = np.diag(wageCoeff[:-1])@prodEff
print(wageEff)