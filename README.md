# FMU Expansion Programming Workspace (Prototype)

This repository contains all source code used in my senior project, in which I designed and developed a custom PCB called **FMU-Expansion**. The purpose of this board is to allow the **Jetson Orin Nano** to function as a **Flight Management Unit (FMU)** in robotics or drone applications.

The board integrates essential SMT components such as:

- **Magnetometer**
- **IMU**
- **Barometer**
- **PCA9685** (I2C-to-PWM generator to add PWM channels)
- **Inverting buffer** (for UART to SBUS conversion)
- **Status LEDs**: `ACT`, `ERR`, `PWR`
- **GPIO header** (for expansion and interfacing)

PCB files are available at:  
👉 [FMU-expansion-from-Jetson_Orin_Nano](https://github.com/Fiat-Anw/FMU-expansion-from-Jetson_Orin_Nano.git)

---

## 📁 Repository Structure

```bash
FMU-expansion-programming_ws/
├── Device_Tree/       # Device tree overlay sources for GPIO activation
├── Test/              # Test code for each component on the FMU-expansion board
└── README.md          # Project documentation
```

## 🧠 Project Author
**Kanisorn Ananwattanawit (Fiat-Anw)**  
GitHub: [Fiat-Anw](https://github.com/Fiat-Anw)

## 📂 Device_Tree — GPIO Overlay Configuration
This folder contains .dts files used to configure Jetson Orin Nano's GPIO pins to interface with components on the FMU-expansion board. Each folder targets a specific hardware configuration (e.g., I2C, UART, LED).

⚙️ How to Use (.dtbo) Overlays

```bash
1) Build the overlay from .dts file:
dtc -I dts -O dtb -o <file_name>.dtbo <file_name>.dts

2) Copy the compiled .dtbo to the boot directory:
sudo cp <file_name>.dtbo /boot

3) Configure GPIO pins using Jetson-IO:
sudo /opt/nvidia/jetson-io/jetson-io.py
```
Follow this video tutorial for detailed steps:
📺 https://www.youtube.com/watch?v=a8espzPAzu4&t=452s

## 🔬 Test — Hardware Functionality Testing
This folder contains example code to verify the operation of each component on the FMU-expansion board.

### 📦 baro/
- BMP581.py – Reads data from the BMP581 barometer.
- BMP581_DRIVER.py – Driver module for BMP581 sensor; handles initialization and communication routines.

### 💡 status_led/
- Contains .dts files for LED control overlay.
- Three Python scripts for testing status LEDs: ACT, ERR, and PWR.

### 📡 rc_in/
- Example code to read SBUS signals via UART from an RC receiver.
- Decodes the SBUS data into individual channel PWM values.

### ⚙️ i2c_pwm/
- Code for controlling servos or motors via PCA9685 (I2C-controlled PWM generator).
- RC_Motor.py:
  - Receives SBUS input from an RC receiver.
  - Decodes SBUS to PWM channels.
  - Sends PWM output to motors using PCA9685.
