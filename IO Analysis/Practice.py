import pandas as pd
import numpy as np

# 변수정의
targetCode = (113,114) # 부문이 하나일 경우 (3,)으로 뒤에 ,를 써줘야 함
targetScale = "기본부문" # 기본부문 or 통합소분류 or 통합중분류 or 통합대분류

# 시작
targetSheet = ("A표_국산거래표(생산자)","A표_총거래표(생산자)")
targetFile = "2019_투입산출표_생산자가격_{}.xlsx".format(targetScale)
targetEmpFile = "2015-19_고용표_{}_취업자수 및 근로시간.xlsx".format(targetScale)
if targetScale=="통합중분류": targetSheet=("A표_국산거래표(생산자가격)","A표_총거래표(생산자가격)")
if targetScale=="기본부문": targetEmpFile = "2015-19_고용표_통합소분류_취업자수 및 근로시간.xlsx"

# 통합행렬
scale = {'기본부문':0,'통합소분류':1,'통합중분류':2,'통합대분류':3}
dataClass_flag = pd.read_excel("2015_부문분류표.xlsx",sheet_name="상품분류표", header=2, skipfooter=31).iloc[:,[0,2,4,6]]
dataClass = dataClass_flag.iloc[:,[scale[targetScale],scale['통합대분류']]].dropna(axis=0, how='all')
sMat = np.zeros(shape=(dataClass.notna().sum()[1]+1,dataClass.notna().sum()[0]))
dataClass = dataClass.fillna(-1).to_numpy()

i=0
for j in range(sMat.shape[1]):
    if j!=0 and dataClass[j][1]!=-1:
        i+=1
        sMat[i,j]=1
    else:
        sMat[i,j]=1

if targetScale == "기본부문":
    dataClass_emp = dataClass_flag.iloc[:,[scale[targetScale],scale['통합소분류']]].dropna(axis=0, how='all')
    sMat_emp = np.zeros(shape=(dataClass_emp.notna().sum()[1],dataClass_emp.notna().sum()[0]))
    dataClass_emp = dataClass_emp.fillna(-1).to_numpy()
    i=0
    for j in range(sMat_emp.shape[1]):
        if j!=0 and dataClass_emp[j][1]!=-1:
            i+=1
            sMat_emp[i,j]=1
        else:
            sMat_emp[i,j]=1   

for i in targetCode:
    sMat[:,np.where(dataClass==i)[0][0]]=0
    sMat[-1,np.where(dataClass==i)[0][0]]=1

# 국산거래표
domesticInteraction = pd.read_excel(targetFile,sheet_name=targetSheet[0], header=5, index_col=1).drop(columns="Unnamed: 0")
midInput = sMat@domesticInteraction.iloc[:-1,:-10].replace(" ","", regex=True).replace("\\n","", regex=True).to_numpy()@sMat.T
midDemandSum = sMat@domesticInteraction.loc[:,'중간수요계'].iloc[:-1].to_numpy()
finalDemandSum = sMat@domesticInteraction.loc[:,'최종수요계'].iloc[:-1].to_numpy()
totalDemandSum = sMat@domesticInteraction.loc[:,'총수요계'].iloc[:-1].to_numpy()

# 총거래표
totalInteraction = pd.read_excel(targetFile,sheet_name=targetSheet[1], header=5, index_col=1).drop(columns="Unnamed: 0")
valueaddedCoeff = (sMat@totalInteraction.loc['부가가치계'].dropna().iloc[:-1].to_numpy())/totalDemandSum
wageCoeff = (sMat@totalInteraction.loc['피용자보수'].dropna().iloc[:-1].to_numpy())/totalDemandSum

# 고용표
targetYear = 2019
year = {2015:0,2016:1,2017:2,2018:3,2019:4}
employee = pd.read_excel(targetEmpFile,sheet_name="취업자수 및 피용자수(상품)",header=5,skipfooter=5,index_col=0).drop(columns="Unnamed: 1").iloc[:,[0,2,4,6,8]].iloc[:,year[targetYear]].to_numpy()

if targetScale =="기본부문":
    totalDemandSum_basic = domesticInteraction.loc[:,'총수요계'].iloc[:-1].to_numpy()
    Employweight = (np.diag(totalDemandSum_basic)@sMat_emp.T)/((np.diag(totalDemandSum_basic)@sMat_emp.T).sum(axis=0))
    employee = Employweight@employee

employeeCoeff = sMat@employee/totalDemandSum

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
