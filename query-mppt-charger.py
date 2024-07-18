import serial
import struct
import time
import subprocess

# Configuration for the serial port
SERIAL_PORT = '/dev/ttyUSB2'  # Replace with your serial port
BAUD_RATE = 2400
TIMEOUT = 1

# Command to query the MPPT charger (function code 0x03, start address 0x0000, length 0x0014)
QUERY_COMMAND = bytes.fromhex('01030000001445C5')

# Function to parse the response from the MPPT charger
def parse_response(response):
    if len(response) < 45:
        raise ValueError(f"Response length is shorter than expected. Length received: {len(response)}")

    parsed_data = {}
    parsed_data['address'] = struct.unpack('>H', response[3:5])[0]
    parsed_data['device_type'] = struct.unpack('>H', response[5:7])[0]
    parsed_data['dc_output_status'] = struct.unpack('>H', response[7:9])[0]
    
    logo = struct.unpack('>H', response[9:11])[0]
    parsed_data['excessive_internal_temperature'] = bool(logo & 0b0000000000000001)
    parsed_data['high_battery_temperature'] = bool(logo & 0b0000000000000010)
    parsed_data['dc_output_overcurrent'] = bool(logo & 0b0000000000000100)
    parsed_data['pv_overvoltage'] = bool(logo & 0b0000000000001000)
    parsed_data['pv_voltage_too_low'] = bool(logo & 0b0000000000010000)
    parsed_data['charging_voltage_too_high'] = bool(logo & 0b0000000000100000)
    parsed_data['fast_charging'] = bool(logo & 0b0000000001000000)
    parsed_data['uniformly_charging'] = bool(logo & 0b0000000010000000)
    parsed_data['float_charge'] = bool(logo & 0b0000000100000000)
    parsed_data['max_power_point_tracking'] = bool(logo & 0b0000001000000000)
    parsed_data['standby'] = bool(logo & 0b1000000000000000)
    
    parsed_data['charging_voltage_percentage'] = struct.unpack('>H', response[11:13])[0]
    parsed_data['system_charging_voltage_percentage'] = struct.unpack('>H', response[13:15])[0]
    parsed_data['battery_type'] = struct.unpack('>H', response[15:17])[0]
    parsed_data['system_set_equalization_voltage'] = struct.unpack('>H', response[17:19])[0] / 10
    parsed_data['system_set_float_voltage'] = struct.unpack('>H', response[19:21])[0] / 10
    parsed_data['system_set_discharge_limit_voltage'] = struct.unpack('>H', response[21:23])[0] / 10
    parsed_data['system_charging_current_limit'] = struct.unpack('>H', response[23:25])[0] / 10
    parsed_data['photovoltaic_input_voltage'] = struct.unpack('>H', response[25:27])[0] / 10
    parsed_data['charging_voltage'] = struct.unpack('>H', response[27:29])[0] / 10
    parsed_data['charging_current'] = struct.unpack('>H', response[29:31])[0] / 10
    parsed_data['charging_power'] = struct.unpack('>H', response[27:29])[0] / 10 * struct.unpack('>H', response[29:31])[0] / 10
    parsed_data['battery_voltage'] = struct.unpack('>H', response[31:33])[0] / 10
    parsed_data['dc_output_current'] = struct.unpack('>H', response[33:35])[0] / 10
    parsed_data['module_temperature'] = struct.unpack('>H', response[35:37])[0]
    parsed_data['external_battery_temperature'] = struct.unpack('>H', response[37:39])[0]

    # Electricity generation is a 4-byte value split across two registers
    total_energy_bytes = response[39:43]
    parsed_data['total_energy_generated'] = struct.unpack('>I', total_energy_bytes)[0] / 1000

    return parsed_data

# Function to query the MPPT charger
def query_mppt_charger():
    # Wait for the system to be started
    time.sleep(5)

    # Stop serial communication on the specified port (Victron Venus OS specific)
    subprocess.call(['/opt/victronenergy/serial-starter/stop-tty.sh', SERIAL_PORT])

    # Wait for the serial communication to stop
    time.sleep(2)

    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT) as ser:
        for _ in range(3):  # Try 3 times to get a valid response
            ser.write(QUERY_COMMAND)
            response = ser.read(45)
            if len(response) == 45:
                return parse_response(response)
            else:
                print("No response received, retrying...")
                print(f"Raw response: {response}")
                time.sleep(1)
        raise ValueError("No valid response received from MPPT charger after 3 attempts.")

if __name__ == "__main__":
    try:
        data = query_mppt_charger()
        print("MPPT Charger Data:")
        for key, value in data.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Error querying MPPT charger: {e}")
