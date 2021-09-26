import eventlet
from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify,
    json
)
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from lora import Lora
import serial

eventlet.monkey_patch()

ser = serial.Serial(
        port = '/dev/ttyAMA0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 2
    )

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'm16.cloudmqtt.com'
app.config['MQTT_BROKER_PORT'] = 10823
app.config['MQTT_USERNAME'] = 'qozkcyle'
app.config['MQTT_PASSWORD'] = '2cL7j6TDnqrF'
app.config['MQTT_REFRESH_TIME'] = 1.0

lora = Lora(ser)
mqtt = Mqtt(app)
socketio = SocketIO(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('Status')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    # emit a mqtt_message event to the socket containing the message data
    socketio.emit('mqtt_message', data=data)

@app.route('/', methods=['GET', 'POST'])
def index():
    lora.lorasend(b"5")
    first_status=lora.lorareceive()
    return render_template('receive.html', status=first_status)

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    pass

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000, use_reloader=False, debug=True)