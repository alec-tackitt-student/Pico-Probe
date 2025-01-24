import network
import socket
import time
from machine import Pin, I2C
from bmp280 import *
import gc
gc.collect()

ssid = 'CTC'  # Replace with your Wi-Fi SSID
password = ''  # Replace with your Wi-Fi password

led_onboard = Pin("LED", Pin.OUT)
i2c = I2C(0, sda = Pin(0), scl = Pin(1), freq = 1000000)
bmp = BMP280(i2c)

#Connect to WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid)
while wlan.isconnected() == False:
    led_onboard.value(1)
    print('Connecting...')
    time.sleep(1)
    led_onboard.value(0)
ip = wlan.ifconfig()[0]
print('Connection successful')
print(f'Connected on {ip}')
led_onboard.value(0)

def web_page():
    #Sensor Configuration
    bmp = BMP280(i2c)
    bmp.use_case(BMP280_CASE_WEATHER)    
    pres = bmp.pressure
    p_bar = pres/100000
    p_mmHg = pres/133.3224
    temp = bmp.temperature - 4
    temp_c2f= (temp * (9/5) + 32)
    temp_f= "{:.2f}".format(temp_c2f)
    pres_p = "{:.2f}".format(pres)
    pres_bar = "{:.2f}".format(p_bar)
    pres_hg = "{:.2f}".format(p_mmHg)
    time.sleep(1)
        
    #HTML CODE for Webserver 
    html = """<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="refresh" content="10">
  <title>Raspberry Pico W Web Server</title>
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
  <link rel="icon" href="data:,">
  <style>
    html {
      font-family: Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      text-align: center;
      background-color: #f4f4f9;
      margin: 0;
      padding: 0;
    }

    body {
      width: 100%;
      margin: 0;
    }

    .topnav { 
      width: 100%;
      background-color: #005f73;
      color: #ffffff;
      padding: 1rem 0;
      box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
    }

    .topnav h2 {
      margin: 0;
      font-size: 2rem;
      text-decoration: underline;
    }

    .content {
      width: 100%;
      padding: 2rem;
      box-sizing: border-box;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
    }

    .cards {
      display: grid;
      grid-gap: 1.5rem;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      justify-content: center;
    }

    .card {
      background-color: #fff;
      border-radius: 8px;
      box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.1);
      padding: 1.5rem;
      text-align: center;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .card:hover {
      transform: translateY(-5px);
      box-shadow: 3px 6px 16px rgba(0, 0, 0, 0.15);
    }

    .card h4 {
      margin: 0 0 0.5rem;
      font-size: 1.2rem;
    }

    .card p {
      margin: 0;
      font-size: 1.5rem;
      font-weight: bold;
    }

    .card.temperature {
      color: #544bd6;
    }

    .card.humidity {
      color: #17bebb;
    }

    .card.pressure {
      color: #d9415f;
    }

    .reading {
      font-size: 2rem;
    }
  </style>
</head>
<body>
  <div class="topnav">
    <h2>Door Pico Probe</h2>
  </div>
  <div class="content">
    <div class="cards">
      <div class="card temperature">
        <h4><i class="fas fa-thermometer-half"></i> Temp. Celsius</h4>
        <p><span class="reading">""" + str(temp) + """ &#8451;</span></p>
      </div>
      <div class="card temperature">
        <h4><i class="fas fa-thermometer-half"></i> Temp. Fahrenheit</h4>
        <p><span class="reading">""" + str(temp_f) + """ &#8457;</span></p>
      </div>
      <div class="card pressure">
        <h4><i class="fas fa-angle-double-down"></i> Pressure (Pa)</h4>
        <p><span class="reading">""" + str(pres_p) + """ Pa</span></p>
      </div>
      <div class="card pressure">
        <h4><i class="fas fa-angle-double-down"></i> Pressure (bar)</h4>
        <p><span class="reading">""" + str(pres_bar) + """ bar</span></p>
      </div>
      <div class="card pressure">
        <h4><i class="fas fa-angle-double-down"></i> Pressure (mmHg)</h4>
        <p><span class="reading">""" + str(pres_hg) + """ mmHg</span></p>
      </div>
    </div>
  </div>
</body>
</html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
    print('Content = %s' % request)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
  except OSError as e:
    conn.close()
    print('Connection closed')