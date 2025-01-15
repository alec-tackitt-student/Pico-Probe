import network
import socket
import time
from machine import Pin, I2C, deepsleep
from bmp280 import *

# Initialize onboard LED and I2C for BMP280
led_onboard = Pin("LED", Pin.OUT)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=50 * 1000)

# Initialize BMP280 sensor
bmp = BMP280(i2c)
bmp.use_case(BMP280_CASE_INDOOR)

# Wi-Fi Network Credentials
ssid = 'baradur24'  # Replace with your Wi-Fi SSID
password = '#Anfwtbtitft'  # Replace with your Wi-Fi password

# Connect to WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("Connecting to Wi-Fi...")
while not wlan.isconnected():
    led_onboard.value(1)
    time.sleep(1)
    print("Connecting...")

led_onboard.value(0)
ip = wlan.ifconfig()[0]
print("Connection successful")
print(f"Device IP: {ip}")

# Web Page Content
def web_page():
    # Read sensor data
    temp = bmp.temperature
    temp_c2f = (temp * (9 / 5) + 32)
    
    # Format readings
    temp_c = "{:.2f}".format(temp)
    temp_f = "{:.2f}".format(temp_c2f)
    
    # HTML page
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pico W - Temperature</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f4f4f9;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            .container {{
                margin: 50px auto;
                max-width: 400px;
                padding: 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }}
            h1 {{
                font-size: 2.5rem;
                color: #007acc;
            }}
            p {{
                font-size: 1.5rem;
                margin: 10px 0;
            }}
            .temp {{
                font-weight: bold;
                font-size: 2rem;
                color: #e63946;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Raspberry Pico W</h1>
            <p>Temperature in Celsius:</p>
            <p class="temp">{temp_c} °C</p>
            <p>Temperature in Fahrenheit:</p>
            <p class="temp">{temp_f} °F</p>
        </div>
    </body>
    </html>
    """
    return html

# Check if current time is within active period (7:30 AM to 3:00 PM weekdays)
def is_active_period():
    current_time = time.localtime()
    current_hour = current_time[3]
    current_minute = current_time[4]
    current_day = current_time[6]  # 0 = Sunday, 6 = Saturday

    # Check if it's weekend (Saturday or Sunday) or outside active hours (7:30 AM to 3:00 PM)
    # if current_day == 5 or current_day == 6:  # Weekend: Friday = 5, Saturday = 6
    #     return False
    # if current_hour < 7 or (current_hour == 7 and current_minute < 30) or current_hour >= 15:
    #     return False
    return True

# Web Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

print("Web server is running. Access it at http://{}/".format(ip))

# Sleep time between checks (in seconds)
sleep_interval = 600  # 10 minutes

while True:
    if not is_active_period():
        print("Entering dormant mode: Non-active period")
        led_onboard.value(0)  # Turn off LED to indicate dormancy
        deepsleep(sleep_interval * 1000)  # Sleep for 10 minutes (in milliseconds)
        continue

    try:
        conn, addr = s.accept()
        print('Connection from:', addr)
        request = conn.recv(1024)
        print("Request:", request)
        
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
        
        # Indicate activity with onboard LED
        led_onboard.toggle()
        
    except Exception as e:
        print("Error:", e)
        conn.close()

    # Sleep for a short time (10 seconds) before next request check
    time.sleep(10)
