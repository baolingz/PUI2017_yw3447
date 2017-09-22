import os
import sys
import json
try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib

if not len(sys.argv) == 4:
    print ("Invalid number of arguments. Run as: python get_bus_info_yw3447.py yourMTAKey BusLine BusLine.csv")
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

try:
    with open(sys.argv[3], 'w') as fhandler:
        fhandler.writelines("Latitude,Longitude,Stop Name,Stop Status\n")
        for i in range(NumBus):
            Latitude = str(ActiveBus[i]['MonitoredVehicleJourney']['VehicleLocation']['Latitude'])
            Longitude = str(ActiveBus[i]['MonitoredVehicleJourney']['VehicleLocation']['Longitude'])
            if ActiveBus[i]['MonitoredVehicleJourney']['OnwardCalls'] == {}:
                StopPointName = "N/A"
                PresentableDistance = "N/A"
            else:
                StopPointName = ActiveBus[i]['MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][0]['StopPointName']
                PresentableDistance = ActiveBus[i]['MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][0]['Extensions']['Distances']['PresentableDistance']                
            fhandler.writelines(Latitude + ',' + Longitude + ',' + StopPointName + ',' + PresentableDistance + '\n')
except IOError as ex:
    print("Error performing I/O operations on the file: ",ex)
