import tushare as ts
import datetime
import re
from requests import get
import os

sharecount=0
count=0
num=0
todaytime=datetime.datetime.today()
oneday=datetime.timedelta(days=1)
yestodaytime=todaytime-oneday

def function(storenumber,day,behavior):
    
    url='http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey='+storenumber+behavior+'&sdate=&edate=&isfulltext=false&sortName=pubdate&sortType=desc&pageNum=1'
    content=get(url,timeout=5).content.decode('utf8')
    timelist=re.findall(r'finalpage/(.*?)/',content,re.S)
    global count
    global num
    global sharecount 
    sharecount+=1
    limit='2018-01-01'
    limittime=datetime.datetime.strptime(limit,'%Y-%m-%d')
    if len(timelist)!=0:
        for i in timelist:   
            starttime=datetime.datetime.strptime(i,'%Y-%m-%d')
            if starttime>limittime:
                count+=1
                period=datetime.timedelta(days=day)
                endtime=starttime+period
                
                if endtime>todaytime:
                    endtime=yestodaytime

                data=ts.get_k_data(str(storenumber),start=str(starttime),end=str(endtime))
                if len(data)!=0:
                    datafix=data.dropna()
                    datahead=datafix['close'].iloc[0]
                    datatail=datafix['close'].iloc[-1]
                
                    if datatail-datahead>0:
                        num+=1

def storerange(url):
    storeweb=get(url).content.decode('gbk')
    storelist=re.findall(r'com/s[hz](.*?).html',storeweb,re.S)
    return(storelist)


list60=[]
list000=[]
list002=[]
list300=[]
list2=storerange('http://quote.eastmoney.com/stock_list.html')

for i in range(len(list2)):
    if list2[i][:2]=='60':
        list60.append(list2[i])
    elif list2[i][:3]=='000':
        list000.append(list2[i])
    elif list2[i][:3]=='002':
        list002.append(list2[i])
    elif list2[i][:3]=='300':
        list300.append(list2[i])
listall=list60+list000+list002+list300


print('股票的范围是？1、沪指主板成分股 2、深指主板成分股 3、中小板成分股 4、创业板成分股 5、全部股票 6、概念板块')
listneed=input('>')
print('想研究什么行为对股票股价的影响？')
behavior=input('>')
print('多少天之内的影响？')
day=int(input('>'))
print('正在分析中，请耐心等候...')
if listneed=='1' or '沪指主板成分股':
    for q in list60:
        function(q,day,behavior)
elif listneed=='2' or '深指主板成分股':
    for q in list000:
        function(q,day,behavior)
elif listneed=='3' or '中小板成分股':
    for q in list002:
        function(q,day,behavior)
elif listneed=='4' or '创业板成分股':
    for q in list300:
        function(q,day,behavior)
elif listneed=='5' or '全部股票':
    for q in listall:
        function(q,day,behavior)
elif listneed=='6' or '概念板块':
    print('请问需要查询的概念板块是？')
    theme=input('>')
    print('抱歉,该功能还没开放使用')

history=str(todaytime)+':查询了'+str(sharecount)+'个股票，自2018年来累计有 '+str(count)+' 个 '+behavior+' 历史，其中有 '+str(num)+' 次股票发生该行为 '+str(day)+' 日后是上升的，比率为 '+str(num/count)+' !'
print(history)  
path='H:\python项目\股票公告研究\历史分析结果.docx'
with open(path,'a+',encoding='utf8') as doc:
    doc.write('\n'+history+'\n')