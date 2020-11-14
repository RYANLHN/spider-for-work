import xlrd
from xlutils.copy import copy
import re

print('你是在哪个盘操作？1、G 2、D 3、H')
com=input('>')
filename='租户信息表.xlsx'
path=com+':\python项目\资产报表自动化\\'+filename

workexcel=xlrd.open_workbook(path)
sheet1=workexcel.sheet_by_name('收租情况') #获取租户信息表的工作表一（租户信息）
t=sheet1.nrows

class zuhu:
    num=0
    def __init__(self,row):
        self.name=sheet1.cell(row,0).value
        self.rent=sheet1.cell(row,2).value
        self.danyuan=str(sheet1.cell(row,4).value).split('/')
        self.debt=sheet1.cell(row,1).value
        self.get=sheet1.cell(row,3).value
        zuhu.num+=1
    def form(self):
        A=self.debt+self.rent
        if self.get>A:
            yjrent=self.get-A
            debtpay=self.debt
            rentpay=self.rent
            newdebt=0
        elif A>=self.get>=self.debt:
            yjrent=0
            debtpay=self.debt
            rentpay=self.get-self.debt
            newdebt=A-self.get
        elif self.get<self.debt:
            yjrent=0
            rentpay=0
            debtpay=self.get
            newdebt=A-self.get

        sheet2=workexcel.sheet_by_name('单元信息') #获取租户信息表的工作表二（单元信息）
        area=0
        for i in self.danyuan:
            area+=float(sheet2.cell(int(float(i)),1).value)          #由于从Excel中获取到的i有小数形式和整数形式两种，因此要统一一下
        
        for i in self.danyuan:
            proportion=float(sheet2.cell(int(float(i)),1).value)/area
            singleyjrent=yjrent*proportion
            singledebtpay=debtpay*proportion
            singlerentpay=rentpay*proportion
            singlenewdebt=newdebt*proportion
            
            
            sheet2wt.write(int(float(i)),2,singlerentpay)
            sheet2wt.write(int(float(i)),4,singledebtpay)
            sheet2wt.write(int(float(i)),5,singleyjrent)
            sheet2wt.write(int(float(i)),6,singlenewdebt)
            
        
            

print('几月？')
month=input('>')
pathform=com+':\python项目\资产报表自动化\生产报表/%s.xlsx'% (month+'月资产报表')

workexceltt=xlrd.open_workbook(com+':\python项目\资产报表自动化/资产报表空表.xlsx')
workexcelw=copy(workexceltt)           #利用空白模板建立一个新表
sheet2wt=workexcelw.get_sheet(0)       #在新表中建立一个工作表
for x in range(1,t):
    zuhu(x).form()
    print(zuhu(x).name+'已完成统计！')
workexcelw.save(pathform)
