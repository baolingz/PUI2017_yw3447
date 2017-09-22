import os
import sys
import json
try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib

if not len(sys.argv) == 3:
    print ("Invalid number of arguments. Run as: python aSimplePythonScript.py yourMTAKey BusLine")
    sys.exit()

url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + \
    sys.argv[1] + \
    "&VehicleMonitoringDetailLevel=calls&LineRef=" + sys.argv[2]

response = urllib.urlopen(url)
data = response.read().decode("utf-8")
data = json.loads(data)

try:
    ActiveBus = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']
except:
    print(data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['ErrorCondition']['Description'])
    sys.exit()
    
NumBus = len(ActiveBus)

print('Bus Line : {}'.format(sys.argv[2]))
print('Number of Active Buses : {}'.format(NumBus))
for i in range(NumBus):
    location = ActiveBus[i]['MonitoredVehicleJourney']['VehicleLocation']
    print('Bus {} is at latitude {} and longitude {}'.format(i,location['Latitude'],location['Longitude']))
