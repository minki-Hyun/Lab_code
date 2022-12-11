import pandas as pd
import numpy as np

totalInteraction = pd.read_excel("2019_투입산출표_생산자가격_통합대분류.xlsx",sheet_name="A표_국산거래표(생산자)", header=5, index_col=1).drop(columns="Unnamed: 0")
domesticInteraction = pd.read_excel("2019_투입산출표_생산자가격_통합대분류.xlsx",sheet_name="A표_총거래표(생산자)", header=5, index_col=1).drop(columns="Unnamed: 0")

# 국산거래표
midInput = totalInteraction.iloc[:-1,:-10].replace(" ","", regex=True).replace("\\n","", regex=True).to_numpy()
# totalInput = totalInteraction.iloc[-1,:-10].replace(" ","", regex=True).replace("\\n","", regex=True).to_numpy()
midDemandSum = totalInteraction.loc[:,'중간수요계'].iloc[:-1].to_numpy()
finalDemandSum = totalInteraction.loc[:,'최종수요계'].iloc[:-1].to_numpy()
totalDemandSum = totalInteraction.loc[:,'총수요계'].iloc[:-1].to_numpy()

# 레온티예프 행렬
Leontieff = np.linalg.inv(np.eye(len(totalDemandSum))-(midInput@np.linalg.inv(np.diag(totalDemandSum))))

# 총거래표
valueaddedCoeff = np.array([domesticInteraction.loc['부가가치계'].dropna().iloc[:-1].to_numpy()]/totalDemandSum)
wageCoeff = np.array([domesticInteraction.loc['피용자보수'].dropna().iloc[:-1].to_numpy()]/totalDemandSum)
# 1차원 배열일 때는 항상 np.array([x]).T 가 되어야 함.

# valueaddedSum = domesticInteraction.loc['부가가치계',:].iloc[:,:-1].to_numpy()


print(Leontieff.shape)
print(wageCoeff.shape)
# print(np.diag((totalInput.to_numpy())).shape)
# Leontieff = midInput.dot(pd.DataFrame(np.diag(totalInput.to_numpy())))


# print(sumOfMidDemand)
# print(middleInput)
