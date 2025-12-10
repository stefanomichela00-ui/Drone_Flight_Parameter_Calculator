import csv
from math import pi, sqrt
from datetime import datetime


def main():

    current_date_str = datetime.now().strftime("%d%m%Y")
    print("\nIf you have a configuration file for the drone, put in the root folder, otherwise insert the parameters manually.")
    configFiles = input("Do you have a configuration file for the drone? (y/n)")
    if configFiles == 'y':
        fileName = input("File name (es. config.csv):") 
        print("\n" )
    
        try:
                params = read_csv_config(fileName)

                mass = params.get("mass")
                battVoltage = params.get("battVoltage")
                battCapacity = params.get("battCapacity")
                numMotors = params.get("numMotors")
                speedConstant = params.get("speedConstant")
                propDiameter = params.get("propDiameter")
                propPitch = params.get("propPitch")

                print(f"Drone parameters correctly loaded from {fileName}")

        except FileNotFoundError:
            print(f"Configuration file not found")
            return
        except Exception as e:
            print(f"Error in configuration file: {e}")
            return
            
    else :
        print("Insert manually the drone parameters:")
        mass = get_float("Mass(kg):")
        battVoltage = get_float("Battery Voltage:")
        battCapacity = get_float("Battery Capacity (mAh):")
        numMotors = get_float("Number of Motors:")
        speedConstant = get_float("Motor Speed Constant (RPM/V):")
        propDiameter = get_float("Propeller Diameter (m):")
        propPitch = get_float("Propeller Pitch (m):")

    hoveringThrust = calculate_hovering_thrust(mass, numMotors)
    totalCurrentDraw = calculate_current_consumption(hoveringThrust, propDiameter,speedConstant, I_noload=1.5,TTR=10)
    flightTime = calculate_flight_time(battCapacity,totalCurrentDraw)

    results_data = {
        "mass_kg": mass,
        "battVoltage_V": battVoltage,
        "battCapacity_mAh": battCapacity,
        "numMotors": numMotors,
        "speedConstant_KV": speedConstant,
        "propDiameter_m": propDiameter,
        "propPitch_m": propPitch,
        
        "hoveringThrust_N": hoveringThrust,
        "totalCurrentDraw_A": totalCurrentDraw,
        "flightTime_min": flightTime
    }

    save_csv_results(f"results\droneAnalysis_{current_date_str}.csv", results_data)

    print("\n -- Basic Drone Flight Parameters --")
    print(f"Hovering thrust: {hoveringThrust} N")
    print(f"Total current draw: {totalCurrentDraw} A")
    print(f"Estimated flight time: {flightTime} minutes")
    print("\n")
    

## --- Functions ---

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            pass

def calculate_hovering_thrust(mass, numMotors):
        # Required thrust of the total drone to hover
        g = 9.81  # Acceleration due to gravity (m/s^2)
        totalThrust = mass * g  # Total thrust required (N)
        return totalThrust

def calculate_flight_time(battCapacity, totalCurrentDraw):
        # Flight time estimation (minutes)
        sf = 0.85  # Safety factor to account for unusable battery capacity
        flightTime = (battCapacity/1000 * sf / totalCurrentDraw) * 60  # Convert hours to minutes
        return flightTime

def calculate_current_consumption(totalThrust, propDiameter,speedConstant,I_noload,TTR):
        from math import sqrt
        rho = 1.225  # Air density at sea level (kg/m^3)
        pi = 3.1416
        mechPower = 1.55*sqrt(totalThrust**3/(2*rho*pi*(propDiameter/2)**2))
        Kt = 60/(2*pi*speedConstant)  # Torque constant (Nm/A)
        motorTorque = totalThrust/TTR # TTR = Trust to Torque Ratio
        currentDraw = motorTorque/Kt + I_noload  # Total current draw (A)
        return currentDraw

def read_csv_config(file_name):
    params = {}
    try:
        with open(file_name, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                for key, value in row.items():

                    try:
                        params[key] = float(value)
                    except ValueError:
                        print(f"Warning: Parametro CSV '{key}' con valore non numerico: '{value}'.")
                        params[key] = None 
                return params 
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file {file_name} not found.")


def save_csv_results(file_name, data):
    fieldnames = list(data.keys())
    try:
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(data)
        print(f"Results saved to {file_name}")
    except Exception as e:
        print(f"Error saving results to {file_name}: {e}")


# --- Launch the program ---
if __name__ == "__main__":
     main()