import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import xml.etree.ElementTree as et
from datetime import datetime
import requests
from time import sleep
import random 

def parse_XML(xml_file, df_cols): 
    xtree = et.parse(xml_file)
    xroot = xtree.getroot()
    rows = []
    
    for node in xroot:
        res = []
        for el in df_cols[0:]: 
            if node is not None and node.find(el) is not None:
                res.append(node.find(el).text)
            else: 
                res.append(None)
        rows.append({df_cols[i]: res[i] 
                     for i, _ in enumerate(df_cols)})
    
    out_df = pd.DataFrame(rows, columns=df_cols)
        
    return out_df


xtree = et.parse('product.xml')
xroot = xtree.getroot()

df_cols = ["product_code","product_name","category_code","category_name","is_active","inventory","original_price","discounted_price","product_url","small_image","medium_image","large_image","original_price_currency","discount_price_currency","itemgroupid","attribute1","attribute2"]
dataset = parse_XML('product.xml',df_cols)
visitor = pd.read_csv('visitor.csv')

tID = 10000

def postRequest(url, data):
        print('Initializing the request...')
        data = requests.get(url,params = data,headers=headers)
        print('Initialization completed.')
        print(data.url)
        print('==============================\n')

segunde = 0.5
counter = 0
while True:
    counter+=1
    print(counter)
    todaysHour = datetime.today().hour
    print('Random data initialization started...')

    randomDataFrame = dataset.sample()    
    randomVisitorDF = visitor.sample()

    hash = random.getrandbits(32)
    tID = "%8x" % hash 

    if todaysHour > 17 and todaysHour <= 23:
        segunde=5
    elif todaysHour >= 0 and todaysHour < 10:
        segunde=600
    else:
        segunde=0.5

    mainEventList = ['OM.pb', 'OM.pv', 'OM.clist', 'OM.pp','OM.pp','OM.pp','OM.pp','OM.pp']
    todaysDate = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    productAmount = random.randint(1,5)
    exVisitorID = randomVisitorDF.iloc[0,0]
    cookieID = randomVisitorDF.iloc[0,1]
    productUri = '/'+randomDataFrame.iloc[0,8].split('/')[-1]
    dPrice = randomDataFrame.iloc[0,7]
    productCode = randomDataFrame.iloc[0,0]
    productName = randomDataFrame.iloc[0,1]
    inventory = randomDataFrame.iloc[0,5]
    itemGroupID = randomDataFrame.iloc[0,-3]
    siteID = "3177556267326330556A383D"
    oID = "53444A2B4B5071322F50303D"
    domain = "store.therelated.com"
    categoryCode = randomDataFrame.iloc[0,2]
    categoryName = randomDataFrame.iloc[0,3]
    if(dPrice == '0'):
        randomChoice = random.choice(mainEventList[1:3])
    else:
        randomChoice = random.choice(mainEventList)
    
    print(cookieID)
    print(randomChoice)
    print(todaysDate)
    print('Object is being created due to choice above...')

    productView = {
        'OM.siteID':siteID,
        'OM.cookieID':cookieID,
        'OM.oid': oID,
        'OM.pv':productCode,
        'OM.pn':productName,
        'OM.inv':inventory,
        'OM.pvt':todaysDate,
        'OM.ppr':dPrice,
        'OM.pv.2':itemGroupID,
        'OM.exVisitorID': exVisitorID,
        'OM.title':productName,
        'OM.lvt':todaysDate,
        'OM.uri':productUri,
        'OM.domain':domain,
    }
    addToCart = {
        'OM.siteID':siteID,
        'OM.cookieID':cookieID,
        'OM.oid': oID,
        'OM.pvt':todaysDate,
        'OM.pb':productCode,
        'OM.pu':productAmount,
        'OM.ppr':dPrice,
        'OM.pb.2':itemGroupID,
        'OM.lvt':todaysDate,
        'OM.exVisitorID': exVisitorID,
        'OM.domain':domain
    }
    productPurchase = {
        'OM.siteID':siteID,
        'OM.cookieID':cookieID,
        'OM.oid': oID,
        'OM.tid':tID,
        'OM.pp':productCode,
        'OM.pu':productAmount,
        'OM.pp.2':itemGroupID,
        'OM.ppr':(productAmount*int(dPrice)),
        'OM.lvt':todaysDate,
        'OM.exVisitorID': exVisitorID,
        'OM.domain':domain
    }
    categoryView = {
        'OM.siteID':siteID,
        'OM.cookieID':cookieID,
        'OM.oid': oID,
        'OM.clist':categoryCode[-1].lstrip() if len(categoryCode) > 1 else categoryCode,
        'CategoryName':categoryName.split('>')[-1].lstrip() if len(categoryName.split('>')) > 1 else categoryName,
        'CategoryPath':categoryName,
        'OM.lvt':todaysDate,
        'OM.exVisitorID': exVisitorID,
        'OM.domain':domain
    }

    print('Object has been created.')

    pvUrl = 'https://lgr.visilabs.net/supporttest/om.gif'
    headers = {'content-type': 'Image/gif'}
                
    if dPrice == '0':
        if randomChoice == 'OM.pv':
            postRequest(pvUrl,productView)
        elif randomChoice == 'OM.clist':
            postRequest(pvUrl, categoryView)
    else:
        if randomChoice == 'OM.pv':
            postRequest(pvUrl,productView)
        elif randomChoice == 'OM.clist':
            postRequest(pvUrl,categoryView)
        elif randomChoice == 'OM.pp':
            postRequest(pvUrl,addToCart)
            postRequest(pvUrl,productPurchase)
        elif randomChoice == 'OM.pb':
            postRequest(pvUrl,addToCart)
    
    sleep(segunde)