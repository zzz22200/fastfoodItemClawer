import requests
import re
from bs4 import BeautifulSoup

from db_connect import initFirebase, setPointData

mosPointItemUrl= "https://www.mos.com.tw/member/bonus.aspx"


response = requests.get(mosPointItemUrl)
soup = BeautifulSoup(response.text, "html.parser")

def clawerMosPointItem():
    db = initFirebase()
    productList = soup.select("ul.productsList > li > img")
    regexp = re.compile(r'RedeemProduct/[0-9]')
    count=0
    pointProductList=[]
    for product in productList:
        
        title = product.find("p")
    
        if  title:
            point = product.select(".program")[0].text
            imageUrl = "https://www.mos.com.tw/"+product.attrs["src"]
            count+=1

            doc_ref = db.collection(u'MosPointItem')
            doc_ref.add({"point":point,"image":imageUrl,"title":title.contents[0]})
            pointProductList.append( {"point":point,"image":imageUrl,"title":title.contents[0]})
        
    print(pointProductList) 
    print(count)  

def hello():
    print("hello")