import requests
from bs4 import BeautifulSoup
import csv
import datetime

#연단위 일정 긁어오기. TargetYear만 바꿔주면 됨.
TargetYear = 2022
kind2 = ["common","grad"]

for kind in kind2:

    DataDate=[]
    DataSchedule=[]

    for i in range(11,13):
        url = "https://www.seoultech.ac.kr/life/sch/{0}/?mon={1}&year={2}".format(kind,i,TargetYear)
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")

        dates = soup.find_all("td", attrs={"class":"date"})

        flag_DataDate=[]
        flag_DataSchedule=[]

        for i in range(len(dates)):
            flag_DataDate.append(dates[i].get_text().replace(" ","").split('~'))

        for i in range(len(dates)):
            if len(flag_DataDate[i][1].split('.')) == 2:
                if(float(flag_DataDate[i][0][5:])>float(flag_DataDate[i][1][:5])):
                    flag_DataDate[i][1] = str(int(flag_DataDate[i][0][0:4])+1) +"."+ flag_DataDate[i][1]
                else:
                    flag_DataDate[i][1] = flag_DataDate[i][0][0:5] + flag_DataDate[i][1]
            
    
            for j in range(0,2):
                flag_DataDate[i][j] = datetime.datetime.strptime(flag_DataDate[i][j], '%Y.%m.%d')

            if flag_DataDate[i][0] != flag_DataDate[i][1]:
                flag_DataDate[i][1] = flag_DataDate[i][1] + datetime.timedelta(days=1)

            for j in range(0,2):
                flag_DataDate[i][j] = flag_DataDate[i][j].strftime('%F')

        schedule = soup.find_all("td", attrs={"class":"al"})
        for i in range(len(schedule)):
            flag_DataSchedule.append(schedule[i].get_text())
        
        for i in range(len(flag_DataDate)):
            DataDate.append(flag_DataDate[i])
            DataSchedule.append(flag_DataSchedule[i])

    Summary = [["Subject","Start Date","Start Time","End Date","End Time","All Day Event","Description","Location","Private"]]

    for i in range(len(DataDate)):
        Summary.append([DataSchedule[i],DataDate[i][0],"",DataDate[i][1],"","TRUE","","","TRUE"])
    
    f = open("Schedule({0}).csv".format(kind),"w",newline='')
    writer = csv.writer(f)

    writer.writerows(Summary)
    f.close()