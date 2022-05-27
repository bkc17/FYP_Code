import firebase_admin
from firebase_admin import db

firebaseConfig = {
  "apiKey": "AIzaSyAFXhfS_8Hqe6yf8fih8ggvKXHL7FCg91A",
  "authDomain": "fyp-anemometer.firebaseapp.com",
  "databaseURL": "https://fyp-anemometer-default-rtdb.firebaseio.com",
  "projectId": "fyp-anemometer",
  "storageBucket": "fyp-anemometer.appspot.com",
  "messagingSenderId": "1093257041401",
  "appId": "1:1093257041401:web:c9a9002e995102d14a9928",
  "measurementId": "G-RH7J9M07RB"
}

cred_obj = firebase_admin.credentials.Certificate('ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':"https://fyp-anemometer-default-rtdb.firebaseio.com"
	})

#Initial setting of data
data = {
  "vdd": [0,0,0,0,0,0,0,0,0,0],
  "temp": [0,0,0,0,0,0,0,0,0,0],
  "rot_speed": [0,0,0,0,0,0,0,0,0,0],
  "grad": [0,0,0,0,0,0,0,0,0,0]
}

ref = db.reference("/")
ref.set(data)

#updating data
data["vdd"] = [1,0,0,0,0,0,0,0,0,0]
data["temp"] = [2,0,0,0,0,0,0,0,0,0]
data["rot_speed"] = [3,0,0,0,0,0,0,0,0,0]
data["grad"] = [4,0,0,0,0,0,0,0,0,0]

ref.update(data)