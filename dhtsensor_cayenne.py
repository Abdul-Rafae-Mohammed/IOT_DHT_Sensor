import paho.mqtt.client as mqtt
import time
import sys
import Adafruit_DHT

time.sleep(30) #Sleep to allow device to connect before starting MQTT

#Setting ClientId and Password to connect to the platform
mqttc = mqtt.Client(client_id="edae8080-2441-11e7-b191-752862caa9ce")
mqttc.username_pw_set("338c21c0-1b1e-11e7-abe0-73b922b9fe51", 
password="239444f12d517e4ea304a343fe0740c7ecbd73d5")

#Connecting to the Platform
mqttc.connect("mqtt.mydevices.com", port=1883, keepalive=60)
mqttc.loop_start()


#Path : "v1/username/things/clientid/data/3"
dht_Temp = "v1/338c21c0-1b1e-11e7-abe0-73b922b9fe51/things/edae8080-\
2441-11e7-b191-752862caa9ce/data/1"
dht_Humidity = "v1/338c21c0-1b1e-11e7-abe0-73b922b9fe51/things/edae8080-\
2441-11e7-b191-752862caa9ce/data/2"

while True:
    #Taking care of errors and exceptions
    try:
       #11 is the sensor type, 4 is the GPIO pin number
        humidity, temperature = Adafruit_DHT.read_retry(11, 4) 
        if temperature is not None:
            temperature = "temp,c=" + str(temperature)
            #Uploading the temperature data to the platform
            mqttc.publish(dht_Temp, payload=temperature, retain=True)
        if humidity is not None:
            humidity = "rel_hum,p=" + str(humidity)
            #Uploading the humidity data to the platform
            mqttc.publish(dht_Humidity, payload=humidity, retain=True)
        time.sleep(5)
    except (EOFError, SystemExit, KeyboardInterrupt):
        mqttc.disconnect()
        sys.exit()
