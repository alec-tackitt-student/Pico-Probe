# Raspberry Pi Pico W Temperature Monitor

## Overview
This project is a temperature monitoring system built using a Raspberry Pi Pico W and a BMP280-3.3 High-Precision Barometric Pressure Module. The project includes 3D-printed components for housing, MicroPython code for data handling, and detailed instructions for setup and use. The goal is to provide a way to view the tempature of the door, and the goal of this repository is to enable future maintenence and upgrades.

---

## Features
- **Real-Time Temperature Monitoring**: Measures and displays temperature using the BMP280 sensor.
- **Wireless Connectivity**: Leverages the Pico W’s Wi-Fi capabilities for remote access.
- **3D-Printed Enclosure**: A custom-designed housing to protect and organize the components.

---

## Hardware Components
1. **Raspberry Pi Pico W**: The microcontroller providing processing power and Wi-Fi capabilities.
2. **BMP280-3.3 Module**: A high-precision barometric pressure and temperature sensor.
3. **Power Supply**: USB power bank, built in wall plug for easy charging.
4. **3D-Printed Enclosure**: Custom design files included for organization and protection.
5. **Jumper Wires and Breadboard**: For prototyping and connecting components.

---

## Software Requirements
- **MicroPython Firmware**: Installed on the Pico W.
- **Thonny or other Python compatible IDE**: For coding and uploading scripts to the Pico W.
- **Git**: For managing the project repository.
- **3D Printing Software**: Such as Cura, for slicing the STL files.
---

## Project Setup

### 1. Hardware Assembly
- Connect the BMP280 module to the Pico W:
  - VCC to 3V3
  - GND to GND
  - SCL to GP5
  - SDA to GP4
- Secure the components in the 3D-printed enclosure.

### 2. Software Installation (if using VsCode)
- Flash MicroPython onto the Pico W using [this guide](https://micropython.org/download/). (should already be done)
- Install VsCode and the Raspberry Pi Pico Project extention. 
- Clone this repository and upload the MicroPython scripts to the Pico via the MicroPico extension.

---

## Using the Project
1. **Power On**: Connect the Pico W to a power source.
2. **Monitor Connection**: the light on the Pico will turn off when sucessfully connected to the CTC network, than you can access the dashboard via it's IP. You can also connect the Pi to a computer Via usb and use a serial monitor to monitor the Wi-Fi connection state.
3. **Monitor Data**: View the data from the PI to ensure accuracy.

---

## Updating the Project
To update the project:
1. Pull the latest code from this repository.
2. Flash the updated scripts to the Pico W.
3. Print any updated 3D models if necessary.

---

## Future Development
Potential enhancements include:
- Implementing some sort of DNS or constant way to access the dashboard.
- Extending functionality to log data over time.

---

## 3D Models
The STL files for the enclosure are located in the `3D_models/` directory. Use your preferred slicer software to prepare the files for printing. Ensure the settings match your 3D printer’s specifications.

---

## Repository Structure
  
```
├── TempProbe/           # Code Directory
│   ├── main.py          # Main MicroPython script
│   ├── BMP280.py        # Temp sensor library
├── 3D_models/
│   ├── Pico Probe v6.FBX   # Full assembley file for editing
│   ├── Pico Probe F360.f3z # Full assembley file for fusion 360
│   ├── Parts/              # Folder for individual models
├── README.md            # Project documentation
```
all files not mentioned are nessasary but should never need to be edited
## Contributing
Contributions are welcome! If you have ideas or improvements, feel free to create a pull request or branch or open an issue in the repository.

---

## License
idk, do what you want

