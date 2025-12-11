# 🚁 Generic Multi-Rotor Flight Parameter Calculator

#### Video Demo: https://youtu.be/T8Pe6_jvSnI

#### Description:

This project implements a **Flight Parameter Calculator** designed to estimate key performance metrics for generic multi-rotor drones (e.g., quadcopters, hexacopters).

The tool allows to input core component specifications (mass, battery capacity, motor KV, propeller geometry) and uses established aerospace and electrical engineering formulas to predict hover performance.

### ⚙️ Engineering Model and Calculations

The program calculates the required electrical power and current draw based on the physical demands of maintaining a stable hover.

The core calculations involve the following steps:

1.  **Total Thrust:** Calculates the total thrust required to counteract gravity ($T_{total} = M_{kg} \cdot g$).
2.  **Current Draw ($I$):** Calculates the motor's current draw by relating the mechanical power to the torque and the motor's electrical constants ($KV$, $R_m$). This accounts for both the load current and the no-load current ($I_{no\_load}$), providing the current for a single motor:
    $$I_{motor} = \frac{\text{Torque}}{K_{t}} + I_{no\_load}$$

3.  **Flight Time:** Sums the current draw for all motors to find the total current consumption ($I_{total}$), which is then used to estimate the maximum flight time based on the battery's usable capacity (mAh).


