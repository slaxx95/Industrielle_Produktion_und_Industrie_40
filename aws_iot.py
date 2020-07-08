from umqtt.robust import MQTTClient

CERT_FILE = "/5b137848c4-certificate.pem.der"
KEY_FILE = "/5b137848c4-private.pem.der"

MQTT_CLIENT_ID = "my_d1_mini"
MQTT_HOST = "a2b9lgqkceki2t-ats.iot.eu-central-1.amazonaws.com"
MQTT_PORT = 8883


def connect():
    try:
        with open(KEY_FILE, "r") as f:
            key = f.read()

        print("Got Key")

        with open(CERT_FILE, "r") as f:
            cert = f.read()

        print("Got Cert")

        mqtt_client = MQTTClient(client_id=MQTT_CLIENT_ID, server=MQTT_HOST, port=MQTT_PORT, keepalive=5000, ssl=True,
                                 ssl_params={"cert": cert, "key": key, "server_side": False})
        mqtt_client.connect()
        print('MQTT Connected')

        return mqtt_client

    except Exception as e:
        print('Cannot connect MQTT: ' + str(e))
        raise

def current_datetime():
    tm = time.time()+7200
    ts = time.localtime(tm)
    return '{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}'.format(ts[0], ts[1], ts[2], ts[3], ts[4], ts[5])


