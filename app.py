from flask import *
from flask import request
import json
import sys
import mysql.connector
import os

databaseName = os.environ['DATABASE_NAME']
databaseUser = os.environ['DATABASE_USER']
databaseCredential = os.environ['DATABASE_CREDENTIAL']


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True



cnx = mysql.connector.connect(host='localhost', database='{}'.format(databaseName), user='{}'.format(databaseUser), password='{}'.format(databaseCredential)) 
cursor = cnx.cursor()

# cursor.execute("SELECT spotId, spotName FROM attractionSpotList")
# # cursor.execute = "SELECT * FROM attractionSpotList"
# myresult = cursor.fetchall()
# print(myresult)


# mycursor.execute("select spotId from attractionSpotList")
# for x in mycursor:
#     print(x)

# mycursor.close()
# mydb.close()


# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

@app.route("/api/attractions")
def apiAttractions():
	page = int(request.args.get('page'))
	keyword = request.args.get('keyword')
	print(page,keyword)

	try:
		cursor.execute("SELECT COUNT(*) FROM attractionSpotList")
		amountOfSpots = cursor.fetchall()
		# print(type(amountOfSpots[0][0]),amountOfSpots[0][0])
		# print(type(page), page)


		# 0-11 (12n ~ 12n+11)
		# 12-23 
		# 24-35
		# 36-47
		# 48-59
		# 60

		queryStart = 12*page
		queryLength = 12

		if ((page*12)+12 < amountOfSpots[0][0]):
			page += 1  
		else:
			page = "NA"

		print(queryStart, queryLength)

		if (keyword!=None):
			print(queryStart, queryLength)
			# cursor.execute("SELECT spotId, spotName, spotCategory, spotDescription, spotAddress, spotTransport, spotMRT, spotLatitude, spotLongitude, spotImages FROM attractionSpotList WHERE spotName LIKE %s LIMIT %s, %s",("%"+keyword+"%",queryStart,queryEnd,))
			cursor.execute("SELECT spotId, spotName, spotCategory, spotDescription, spotAddress, spotTransport, spotMRT, spotLatitude, spotLongitude, spotImages FROM attractionSpotList WHERE spotName LIKE %s LIMIT  %s, %s",("%"+keyword+"%",queryStart,queryLength, ))
			myresult = cursor.fetchall()
			print(myresult)
		else:
			print("else")
			print(queryStart, queryLength)
			# cursor.execute("SELECT spotId, spotName, spotCategory, spotDescription, spotAddress, spotTransport, spotMRT, spotLatitude, spotLongitude, spotImages FROM attractionSpotList WHERE spotName LIKE %s LIMIT %s, %s",("%"+keyword+"%",queryStart,queryEnd,))
			cursor.execute("SELECT spotId, spotName, spotCategory, spotDescription, spotAddress, spotTransport, spotMRT, spotLatitude, spotLongitude, spotImages FROM attractionSpotList LIMIT %s,%s",(queryStart, queryLength,))
			myresult = cursor.fetchall()
			print(myresult)

		responseData={
			"nextPage": f"{page}", 
			"data":[]
		}
		for data in myresult:
			
			spotId = data[0]
			spotName = data[1]

			# print(data)
			# print(data[0])
			# print(data[1])     
			# print(type(data[1]))


		#print(page)

			spotInfo = {
					"id": f"{data[0]}",
					"name": f"{data[1]}",
					"category": f"{data[2]}",
					"description": f"{data[3]}",
					"address": f"{data[4]}",
					"transport": f"{data[5]}",
					"mrt": f"{data[6]}",
					"latitude": f"{data[7]}",
					"longitude": f"{data[8]}",
					"images": f"{data[9]}"
			}

			responseData['data'].append(spotInfo)
			# print(responseData)
			print('\n\n\n')
		print(responseData)

			
			# print(type(f"{spotName}"))
		
		# responseData = {}
		# responseJsonData = json.dumps(responseData)
		responseJsonData = jsonify(responseData)
		
		return responseJsonData
	except:
		errorMessage={
				"error": True,
				"message": "伺服器內部錯誤"
			}
		return errorMessage, 500, {'ContentType':'application/json'}

@app.route("/api/attraction/<id>")
def apiAttraction(id):
	print(id)
	
	responseData={
		"data":[]
	}
	
	try:
		cursor.execute("SELECT spotId, spotName, spotCategory, spotDescription, spotAddress, spotTransport, spotMRT, spotLatitude, spotLongitude, spotImages FROM attractionSpotList WHERE spotId=%s",(id, ))
		myresult = cursor.fetchall()
		# print(myresult)
		
		if (len(myresult)!=0):
			for data in myresult:
				
				spotInfo = {
						"id": f"{data[0]}",
						"name": f"{data[1]}",
						"category": f"{data[2]}",
						"description": f"{data[3]}",
						"address": f"{data[4]}",
						"transport": f"{data[5]}",
						"mrt": f"{data[6]}",
						"latitude": f"{data[7]}",
						"longitude": f"{data[8]}",
						"images": f"{data[9]}"
				}

				responseData['data'].append(spotInfo)
				# print(responseData)
				print('\n\n\n')
			print(responseData)
			responseJsonData = jsonify(responseData)
			return responseJsonData
		else:
			errorMessage={
				"error": True,
				"message": "景點編號不正確"
			}
			return errorMessage, 400, {'ContentType':'application/json'}
	except:
		errorMessage={
				"error": True,
				"message": "伺服器內部錯誤"
			}
		return errorMessage, 500, {'ContentType':'application/json'}

app.run(port=3000)
