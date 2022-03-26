from flask import *
from flask import request
import json
import mysql.connector
# from flask import Flask

cnx = mysql.connector.connect(host='localhost', database='website', user='root', password='#Curtis0630') 
cursor = cnx.cursor()
cursor.execute("SELECT * FROM attractionSpotList")

myresult = cursor.fetchall()
print(myresult)


