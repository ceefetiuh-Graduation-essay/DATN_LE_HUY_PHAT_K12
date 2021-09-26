from lora import Lora
import serial
import paho.mqtt.client as mqtt
import time
hostname = "m16.cloudmqtt.com"
portname = 10823
user = "qozkcyle"
passwd = "2cL7j6TDnqrF"

ser = serial.Serial(
        port = '/dev/ttyAMA0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 2
    )
lora = Lora(ser)

def on_connect(client, userdata, flags, rc):
    client.subscribe("cALL") 

def on_subscribe(client, userdata, mid, granted_qos):
    pass

#==================================================================================# MESSAGE DATA
def on_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode('utf-8')
    )
    #print(data)
    try:
        if(data['topic'] == "cALL"): 
            if data['payload']=="cALL":
                lora.lorasend(b"5")
                datarc=lora.lorareceive().strip()
                client.publish(topic="Status", payload=datarc)   
    except:
        pass

#==================================================================================# 
if __name__ == "__main__":
    try:
        client = mqtt.Client(protocol=mqtt.MQTTv311)
        client.username_pw_set(username=user, password=passwd)
        client.on_connect = on_connect
        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.connect(host= hostname, port=portname) # HOST MQTT BROKER, PORT
        client.loop_forever()
    except:
        pass