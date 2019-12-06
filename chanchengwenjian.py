import os
from requests import get
import re
from lxml import etree
from time import sleep

dis=''

def gett(url): 
    ob1=get(url).content.decode('UTF8')
    ota=etree.HTML(ob1)
    otaitem=ota.xpath('//div/div/div/div/div/div/a/text()')
    otahref=ota.xpath('//div/div/div/div/div/div/div/a/@href')
    otatime=ota.xpath('//div/div/div/div/div/div/div/span/text()')
    
    assert(len(otaitem)==len(otahref))
    return list(zip(otaitem,otahref,otatime)) 

def writefile(target,result): 
    for i in range(len(result)):
        target.write('%s\t%s\t\t%s\n\n'%(result[i][2],result[i][0],'http://www.chancheng.gov.cn'+result[i][1]))

def download_detail(result,filename):
    os.makedirs(dis+'/政策文件/'+filename+'/全部文章')
    for g in range(len(result)):
        oba=get('http://www.chancheng.gov.cn'+result[g][1]).content.decode('utf8')
        obaa=etree.HTML(oba)
        obatitle=obaa.xpath('//div[@class="title_cen mar-t2 text"]/text()')
        obadetail=obaa.xpath('//div/ucapcontent/p/text()')
        with open(dis+'/政策文件/'+filename+'/全部文章/'+obatitle[0]+'.docx','a+',encoding='utf8') as fi:
            for i in obadetail:
                fi.write(i+'\n')
    print('下载完成')

def download_list(url,filename): 
    result=gett(url)
    os.chdir('D:')
    path=dis+'/政策文件/'+filename+'\/'+filename+'.docx'
    if os.path.exists(path): 
        fi=open(path,'a+',encoding='utf8')
        writefile(fi,result)
    elif os.path.exists(dis+'/政策文件/'+filename): 
        fi=open(path,'w+',encoding='utf8')
        writefile(fi,result)
    elif os.path.exists(dis+'/政策文件'):
        os.makedirs(dis+'/政策文件/'+filename) 
        fi=open(path,'w+',encoding='utf8')
        writefile(fi,result)
    else:
        os.makedirs(dis+'/政策文件')
        os.makedirs(dis+'/政策文件/'+filename)
        fi=open(path,'w+',encoding='utf8')
        writefile(fi,result)
    return result

def getpage(url):
    ob=get(url).content.decode('UTF8')
    if re.search(r'createPageHTML(.*?);',ob,re.S):
        return re.findall(r'createPageHTML(.*?);',ob,re.S)[0][12]
    else:
        return False
      
def start(place):
    print('开始查找关于 \''+place+'\' 的政策文件....')
    for i in range(len(ob4)):
        if re.search(place,ob4[i][0],re.S):
            urlfront=ob4[i][1]
            filename=ob4[i][0]+'政策文件'
            sleep(0.8)
            print('查找'+filename+'....')
            url=urlfront+'/0200/bmlist.shtml'
            if not getpage(url)==False:  
                sleep(0.8)
                print('正在下载资料目录...')
                assemble=download_list(url,filename)
                page=int(getpage(url))
                for j in range(page+1):
                    url2=urlfront+'/0200/bmlist_'+str(j)+'.shtml'
                    assemble2=download_list(url2,filename)
                    assemble+=assemble2
                sleep(0.8)
                print('下载成功！')
                sleep(0.5)
                print('您是否需要下载所有的阅读资料？')
                need=input('>')
                if need=='是' or need=='需要':
                    download_detail(assemble,filename)
                else:
                    print('感谢老板使用！')
            else:
                sleep(0.8)
                print('没有政策文件')

ob3=get('http://www.chancheng.gov.cn/').content.decode('utf8')
ob3text=etree.HTML(ob3).xpath('//div[@id="div_4"]/ul/li/a/text()')
ob3href=etree.HTML(ob3).xpath('//div[@id="div_4"]/ul/li/a/@href')
ob4=list(zip(ob3text,ob3href))

print('您想搜索哪个单位的文章？')
name=input('>') 
print('保存到哪个盘？')
dis=input('>')+':'

start(name)


