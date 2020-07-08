import wifi         
import aws_iot
import time
import json
import machine
from ADC_conversion import ADC_to_perc
from dht import DHT11

plant_1_hum_limit = 93                          # Bodenfeuchtigkeitsgrenzwert Pflanze 1
plant_2_hum_limit = 75                          # Bodenfeuchtigkeitsgrenzwert Pflanze 2

pot = machine.ADC(0)                            # Analoger Eingang

sensor1 = machine.Pin(16, machine.Pin.OUT)      # Bodenfeuchtigkeitssensor Pflanze 1 am Low Level Relais
sensor1.value(1)

sensor2 = machine.Pin(5, machine.Pin.OUT)       # Bodenfeuchtigkeitssensor Pflanze 2 am Low Level Relais
sensor2.value(1)

pump1 = machine.Pin(14, machine.Pin.OUT)        # Pumpe für Pflanze 1 am Low Level Relais
pump1.value(1)

pump2 = machine.Pin(12, machine.Pin.OUT)        # Pumpe für Pflanze 2 am Low Level Relais
pump2.value(1)

dht = DHT11(machine.Pin(2))                     # Temperatur- und Luftfeuchtigkeitssensor


def current_datetime():
    tm = time.time()+7200
    ts = time.localtime(tm)
    return '{}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}'.format(ts[0], ts[1], ts[2], ts[3], ts[4], ts[5])


def send_ground_data(ground_data, mqtt_client):
    datetime = current_datetime()
    message = {'Plant_1_Humidity': ground_data[0],
               'Plant_2_Humidity': ground_data[1],
               'Plant_1_Hum_Limit': ground_data[2],
               'Plant_2_Hum_Limit': ground_data[3],
               'timestamp': datetime}
    json_msg = json.dumps(message)
    try:
        mqtt_client.publish("ground_data", json_msg)
        print("Sent: " + json_msg)
    except Exception as e:
        print("Exception publish: " + str(e))


def send_env_data(env_data, mqtt_client):
    datetime = current_datetime()
    message = {'Air_Temperature': env_data[0],
               'Air_Humidity': env_data[1],
               'timestamp': datetime}
    json_msg = json.dumps(message)
    try:
        mqtt_client.publish("ground_data", json_msg)
        print("Sent: " + json_msg)
    except Exception as e:
        print("Exception publish: " + str(e))


if __name__ == "__main__":
    wifi.connect_wifi()
    wifi.synchronize_rtc()

    mqtt_client = aws_iot.connect()

    while True:
        # Messung der Bodenfeuchtigkeit von Pflanzen 1 und 2 ca. einmal stündlich
        # Gießen, wenn Grenzwert unterschritten ist.
        # Bodendaten zusammenfassen und an AWS schicken.
        # Lufttemperatur und -feuchtigkeit messen: 10 mal innerhalb einer Stunde.
        # Luftdaten zusammenfassen und an AWS schicken

        # Messung Sensor 1
        sensor1.value(0)
        print("Sensor 1 measuring...")
        time.sleep(10)
        sensor1_value_raw = pot.read()           # Analog-in hat Werte zwischen 0 (min) und 1023 (max)
        sensor1_value = round(ADC_to_perc(sensor1_value_raw), 1)
        sensor1.value(1)
        if sensor1_value < plant_1_hum_limit:
            pump1.value(0)
            time.sleep(1.5)
            pump1.value(1)
        print("Ground Humidity Plant 1: ", sensor1_value_raw, " = ", sensor1_value, "%")

        # Messung Sensor 2
        sensor2.value(0)
        print("Sensor 2 measuring...")
        time.sleep(10)
        sensor2_value_raw = pot.read()                 # Analog-in hat Werte zwischen 0 (min) und 1023 (max)
        sensor2_value = round(ADC_to_perc(sensor2_value_raw), 1)
        sensor2.value(1)
        if sensor2_value < plant_2_hum_limit:
            pump2.value(0)
            time.sleep(1.5)
            pump2.value(1)
        print("Ground Humidity Plant 2: ", sensor2_value_raw, " = ", sensor2_value, "%")

        # Zusammenfassung der Bodendaten und Versendung an AWS
        ground_data = [sensor1_value, sensor2_value, plant_1_hum_limit, plant_2_hum_limit]
        send_ground_data(ground_data, mqtt_client)
        print("Message with ground data sent to AWS.")

        # Luftmessung und Versendung an AWS
        t = 0
        while t < 6:                   # 6 Messungen über insg. eine Stunde
            dht.measure()
            temp_air = dht.temperature()
            hum_air = dht.humidity()
            env_data = [temp_air, hum_air]
            print("Environment: ", temp_air, "°C, ", hum_air, "% relative humidity")
            send_env_data(env_data, mqtt_client)
            print("Message with environment data sent to AWS.")
            time.sleep(600)
            t=t+1


        print("-------------------New Cycle----------------------")
