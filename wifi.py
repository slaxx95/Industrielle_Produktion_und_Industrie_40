import ntptime
import network

def connect_wifi():
    WIFI_SSID = "Berlin"
    WIFI_PW = "probeeins"

    wlan = network.WLAN(network.STA_IF)

    if not wlan.isconnected():
        wlan.active(True)
        print("connecting to network", WIFI_SSID)
        wlan.connect(WIFI_SSID, WIFI_PW)
        while not wlan.isconnected():
            pass

    print("connected to", wlan.ifconfig())

def synchronize_rtc():
    ntptime.settime()