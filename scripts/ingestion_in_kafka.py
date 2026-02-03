import time
import json
import requests
from kafka import KafkaProducer

API_KEY = "YOUR APY KEY" 
SATELLITE_ID_LIST = [
    25544, 28654, 33591, 32382,
    55500, 55501, 55502, 55503, 55504,
    58461, 58462, 58463, 58464, 58465,
    43013, 41240, 44387
]
KAFKA_TOPIC = 'satellite_stream'
KAFKA_SERVER = 'localhost:9092'


producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def get_satellite_data(sid):
    url = f"https://api.n2yo.com/rest/v1/satellite/positions/{sid}/44.42/26.10/0/1&apiKey={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f" Eroare HTTP {response.status_code} la ID {sid}. URL-ul poate fi gresit.")
            return None
        data = response.json()
        
        if 'error' in data:
            print(f" Eroare API N2YO: {data['error']}")
            return None

        if 'positions' in data and len(data['positions']) > 0:
            pos = data['positions'][0]
            return {
                "satid": data['info']['satid'],
                "satname": data['info']['satname'],
                "latitude": pos['satlatitude'],
                "longitude": pos['satlongitude'],
                "altitude": pos['sataltitude'],
                "timestamp": pos['timestamp']
            }
            
    except Exception as e:
        print(f" Eroare la ID {sid}: {e}")
    return None

print("Turning on ingestion engine.")

try:
    while True:
        print(f" Start ingestion: {time.strftime('%H:%M:%S')} ")
        
        for sid in SATELLITE_ID_LIST:
            sat_data = get_satellite_data(sid)
            if sat_data:
                producer.send(KAFKA_TOPIC, value=sat_data)
                print(f" Kafka: {sat_data['satname']} ({sat_data['satid']}) trimis.")
            
            time.sleep(1) 
        
        print(f"Done. Next check in 5 minutes.")
        time.sleep(300)
    
except KeyboardInterrupt:
    print("Ingestion off")
finally:
    producer.close()
