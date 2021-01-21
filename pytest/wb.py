# -*- coding: utf-8 -*-
import time
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
#from requests.packages.urllib3.exceptions import InsecureRequestWarning

#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
ua=UserAgent().random
#session = requests.session()

for i in range(6):
        num=str(i+1)
        url = "http://blog.sina.com.cn/s/articlelist_1310563685_0_%s.html"%num
        headers= {
                'Host': 'blog.sina.com.cn',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'User-Agent': ua,
        }
        headers1 = {
                'Host': 's12.sinaimg.cn',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'User-Agent': ua,
                'Referer': 'http://blog.sina.com.cn/',
                'Upgrade-Insecure-Requests': '1',
        }
            # #urllib或requests在打开https站点是会验证证书。 简单的处理办法是在get方法中加入verify参数，并设为False
        res = requests.get(url, headers=headers) #,verify=False
        #print(res.text)
        html = res.content.decode()
        htm = BeautifulSoup(html, features="lxml")

        #messages = htm.find_all("tr", class_="item")
        # arl = htm.find_all("div", class_="articleCell SG_j_linedot1")
        arl = htm.find_all("span", class_="atc_title")
        #print(arl)
        print(len(arl))
        for ar in arl:
                try:
                        tx=ar.a
                        bt=tx.get_text()
                        link=tx['href']
                        r = requests.get(link, headers=headers)
                        ht = r.content.decode()
                        ht1 = BeautifulSoup(ht, features="lxml")
                        arl1 = ht1.find("div", class_="articalContent")
                        tx1 = arl1.find_all('p')
                        f1 = open(r'C:\test\dist\wb.txt', 'a', encoding='utf-8')
                        f1.write(bt)
                        f1.write('\n')
                        try:
                                tx2=arl1.find('div')
                                nei2=tx2.get_text()
                                #print(nei2)
                                f1.write(nei2)
                                f1.write('\n')
                                lin2 = tx2.find_all('img')
                                print(lin2)
                                if not lin2:
                                        pass
                                else:
                                        for e in lin2:
                                                link2 = e['real_src']
                                                rm = requests.get(link2, headers=headers1)
                                                name = link2[-11::]
                                                f = open(r'C:\test\dist\wb\%s.png' % name, 'wb')
                                                f.write(rm.content)
                                                print(link2)
                                                f1.write(link2)
                                                f1.write('\n')
                                                f.close()


                        except:
                                pass

                        #print(bt)

                        for n in tx1:
                                nei = n.get_text()
                                #lin = n.a
                                lin = n.find_all('img')
                                f1.write(nei)
                                f1.write('\n')
                               # print(lin)
                                #print(nei)
                                if not lin:
                                        pass
                                else:
                                        for i in lin:
                                                link = i['real_src']
                                                rm = requests.get(link, headers=headers1)
                                                name = link[-5::]
                                                f = open(r'C:\test\dist\wb\%s.png' % name, 'wb')
                                                f.write(rm.content)
                                                print(link)
                                                f1.write(link)
                                                f1.write('\n')
                                                f.close()
                                                f1.close()

                except:
                        pass

                #print(bt,link)




#ts = time.strftime("%Y/%m/%d %H:%M", time.localtime())
#f = open('/usr/share/nginx/html/豆瓣新片Top10.txt', "w", encoding='utf-8')

# cookieJar1 = RequestsCookieJar()
# #print(res.cookies)
# for cookie in res.cookies:
#      cookieJar1.set(cookie.name, cookie.value)
# print("cookieJar1:", cookieJar1)
#url1 = "https://xueqiu.com/statuses/hot/listV2.json?since_id=-1&max_id=-1&size=15"