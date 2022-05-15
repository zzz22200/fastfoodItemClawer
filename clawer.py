import requests
import re
from bs4 import BeautifulSoup

from db_connect import initFirebase, setPointData

mosPointItemUrl = "https://www.mos.com.tw/member/bonus.aspx"
mosPriceItemUrl = "https://www.mos.com.tw/menu/set.aspx"

mosPriceItemUrlList=["https://www.mos.com.tw/menu/set.aspx","https://www.mos.com.tw/menu/breakfast.aspx",
"https://www.mos.com.tw/menu/soup.aspx","https://www.mos.com.tw/menu/beverage.aspx"]

def clawerMosPointItem():
    response = requests.get(mosPointItemUrl)
    soup = BeautifulSoup(response.text, "html.parser")
    db = initFirebase()
    productList = soup.select("ul.productsList > li > img")
    regexp = re.compile(r'RedeemProduct/[0-9]')
    count=0
    pointProductList=[]
    for product in productList:
        
        title = product.find("p")
    
        if  title and title.contents[0].text and "<" not in title:
            point = product.select(".program")[0].text
            imageUrl = "https://www.mos.com.tw/"+product.attrs["src"]
            count+=1
            title = title.contents[0].text
            print({"point":point,"image":imageUrl,"title":title})

            id = title.replace("/","")
            print("-----------")
            doc_ref = db.collection(u'MosPointItem')
            doc_ref.document(str(id)).set({"point":point,"image":imageUrl,"title":title})
            pointProductList.append( {"point":point,"image":imageUrl,"title":title})
        
    print(pointProductList) 
    print(count)  

def clawerMosPriceItemList():
    db = initFirebase()

    for url in mosPriceItemUrlList:
        clawerMosPriceItem(url,db)


def clawerMosPriceItem(url,db):
    response = requests.get(mosPriceItemUrl)
    soup = BeautifulSoup(response.text, "html.parser")
    productList = soup.select("ul.productsList > li")
    regexp = re.compile(r'RedeemProduct/[0-9]')
    count=0
    priceProductList=[]
    for product in productList:
        title = product.find("h1")
        # print(title)

        if title:
           
            price = product.select(".price > span")[0].text
            title = title.text
            id = title.replace("/","")
            count+=1
            data = {"title": title,"price":int(price)}
            print(data)
            doc_ref = db.collection(u'MosPriceItem')
            doc_ref.document(str(id)).set(data)
        
    print(priceProductList) 
    print(count)


def getData():
    db = initFirebase()
    priceItemList = db.collection(u'MosPriceItem').stream()
    for doc in priceItemList:
        print(f'{doc.id} => {doc.to_dict()}')



def hello():
    print("hello")


clawerMosPointItem()
clawerMosPriceItemList()
# getData()