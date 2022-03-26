from datetime import MINYEAR
import os
import json
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',          
    database='website', 
    user='root',        
    password='#Curtis0630') 

print(mydb)

mycursor = mydb.cursor()

# Test Database
# mycursor.execute("show databases")
# for x in mycursor:
#     print(x)

# print(mycursor)

with open('./data/taipei-attractions.json', 'r') as f:
    data = f.read()
# print(data)
# print(type(data))

dataJson = json.loads(data)
# print(dataJson['result']['results'][2])

attractionSpots=dataJson['result']['results']

print(len(attractionSpots))

for spot in attractionSpots:

    # print(spot)
    attractionSpotTransportInfo = spot['info']
    attractionSpotMRT = spot['MRT']
    attractionSpotTitle = spot['stitle']
    attractionSpotPostdate = spot['xpostDate']
    attractionSpotLongitude = spot['longitude']
    attractionSpotLatitude = spot['latitude']
    attractionSpotDescription = spot['xbody']
    attractionSpotAddress = spot['address']
    attractionSpotImage = spot['file']
    # attractionSpotCat1 = spot['CAT1']
    attractionSpotCat2 = spot['CAT2']
    attractionSpotID = spot['_id']
    attractionSpotImageList = attractionSpotImage.lower().split('.jpg')
    
    attractionSpotImageArray = []
    for item in attractionSpotImageList:
        if item != '':
            if ('.mp3' not in item) and ('.flv' not in item):
                item += '.jpg'
                attractionSpotImageArray.append(item)
    
    # print(attractionSpotImageArray)
    # print("\n")
    # print(attractionSpotID, attractionSpotMRT)

    mycursor.execute("SELECT spotId FROM attractionSpotList WHERE spotId = %s",(attractionSpotID,))
    myresult = mycursor.fetchall()
    # print(myresult)

    if len(myresult)==0:

        sql = "INSERT INTO attractionSpotList (spotId, spotName, spotCategory, spotDescription, spotAddress, spotTransport, spotMRT, spotLatitude, spotLongitude, spotImages) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (attractionSpotID, attractionSpotTitle, attractionSpotCat2, attractionSpotDescription, attractionSpotAddress, attractionSpotTransportInfo, attractionSpotMRT, attractionSpotLatitude, attractionSpotLongitude, str(attractionSpotImageArray))
        mycursor.execute(sql, val)

        mydb.commit()
        print(mycursor.rowcount, "record inserted.")

mydb.close()
                



