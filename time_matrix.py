import pandas as pd
import numpy
import json
import csv
import requests 


access_path = '/home/eolus/Dropbox/610 Project Data'
file = access_path+'/location_data.csv'

# Pull API key from .txt file
with open(access_path+'/MapQuestAPI/MAPQUEST_API_KEY.txt', 'r') as f:
    APP_KEY = f.readline()

# Pull location data input from `CSV` to Pandas `DataFrame`
df = pd.read_csv(file, header = None)
df.columns = ['Locations', 'Address']
df["Latitude"] = ""
df["Longitude"] = ""

# Query position data with geoPy
from geopy.geocoders import Nominatim
geolocator = Nominatim()

for index, row in df.iterrows():
    address = row[1]
    location = geolocator.geocode(address)

    try:
        df.loc[index, 'Latitude'] = location.latitude
        df.loc[index, 'Longitude'] = location.longitude
    except Exception as e:
        if location is None:
            print('Error with address: {address}'.format(address = address))
        else:
            print(str(e))

print(df)


# Pull time matrix data
MAPQUEST_URL = 'http://open.mapquestapi.com/directions/v2/routematrix?key={appkey}'

def time_matrix(df):
    request_body = {
    'locations': 
    [
    {'latLng': 
        {
        'lat': df.loc[index, 'Latitude'], 
        'lng': df.loc[index, 'Longitude']
        }
    } 
    for index, row in df.iterrows()
    ], 
    'options': {'allToAll': 'true'}
    }
    
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    r = requests.post(MAPQUEST_URL.format(appkey=APP_KEY), data=json.dumps(request_body), headers=headers)

    if r.status_code != 200:
        # We didn't get a response from Mapquest
        return -1
    result = json.loads(r.content.decode())

    time = result['time']
    return time


time_matrix = time_matrix(df)
time_matrix_array = numpy.asarray(time_matrix)
print(time_matrix_array)

numpy.savetxt(access_path+'/time_matrix.csv', time_matrix_array, delimiter=",")
