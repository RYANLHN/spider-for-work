from requests import get
from lxml import etree
import os

print('你想搜索的政策文件主题是？')
content=input('>')
obtall=['']
for i in range(9):
    url='http://118.178.151.173/s?q=1&qt='+content+'&pageSize=10&database=zcwj&siteCode=4406040004&docQt=&page='+str(i)
    obt=get(url).content.decode('utf8')
    obt1=etree.HTML(obt)
    obttitle=obt1.xpath('//div/a[@class="fl txt_color"]/@title')
    obthref=obt1.xpath('//div/a[@class="fl txt_color"]/@href')
    obtlist=list(zip(obttitle,obthref))
    obtall+=obtlist
# print(list(obtall)[1][1])
print('您想保存在哪个盘？')
chir=input('>')
path=chir+'://政府搜索文件/'+content+'/'+content+'.docx'
if os.path.exists(path):
    with open(path,'a+',encoding='utf8') as fi:
        for i in range(len(obtall)-1):
            fi.write('%s\n%s\t\n'%(list(obtall)[i+1][0],list(obtall)[i+1][1]))
else:
    os.makedirs(chir+'://政府搜索文件/'+content)
    with open(path,'w+',encoding='utf8') as fi:
        for i in range(len(obtall)-1):
            fi.write('%s\n%s\t\n'%(list(obtall)[i+1][0],list(obtall)[i+1][1]))

