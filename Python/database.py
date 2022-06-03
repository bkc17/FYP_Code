import firebase_admin
from firebase_admin import db, storage
import random
import time

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
	"databaseURL":"https://fyp-anemometer-default-rtdb.firebaseio.com",
  "storageBucket": "fyp-anemometer.appspot.com"
	})

#Initial setting of data
data = {
  "data_full":
  {
    "vdd": [0,0,0,0,0,0,0,0,0,0],
    "temp": [0,0,0,0,0,0,0,0,0,0],
    "rot_speed": [0,0,0,0,0,0,0,0,0,0],
    "grad": [0,0,0,0,0,0,0,0,0,0]
  },
  "data_current":
  {
    "vdd": 0,
    "temp": 0,
    "rot_speed": 0,
    "grad": 0
  }
}

ref = db.reference("/")
store = storage.bucket()

store = store.blob("final_results.csv")
store.upload_from_filename("final_results.csv")
ref.set(data)

# #updating data
data["data_full"]["vdd"] = [1,0,0,0,0,0,0,0,0,0]
data["data_full"]["temp"] = [2,0,0,0,0,0,0,0,0,0]
data["data_full"]["rot_speed"] = [3,0,0,0,0,0,0,0,0,0]
data["data_full"]["grad"] = [4,0,0,0,0,0,0,0,0,0]
while(True):

  data["data_current"]["vdd"] = random.randint(0,5)
  data["data_current"]["temp"] = random.randint(0,5)
  data["data_current"]["rot_speed"] = random.randint(0,5)
  data["data_current"]["grad"] = random.randint(0,5)
  ref.update(data)
  time.sleep(1)