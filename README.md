  <h1>RS485 read China MPPT Solar Controller Charger</h1>

  <p>This project interfaces with a China MPPT Solar Controller Charger using RS485 communication.</p>


  <p align="center">
      <img width="50%" src="https://github.com/christian1980nrw/RS485-read-China-MPPT-Charger/blob/main/product-picture.jpg"> 
  </p>

  <h2>Overview</h2>

  <p>This charger is user-friendly, but caution is advised with pre-defined profiles like Lifepo4 16S; it's advisable to use user-defined voltages suitable for your battery.</p>

  <h2>Quick Links</h2>

  <ul>
    <li><a href="https://www.alibaba.com/product-detail/12V-24V-36V-48V-60V-72V_1600249401981.html">Alibaba Product Page</a></li>
    <li><a href="https://de.aliexpress.com/item/1005006435255704.html">AliExpress Product Page 1</a></li>
    <li><a href="https://de.aliexpress.com/item/1005004417934706.html">AliExpress Product Page 2</a></li>
    <li><a href="https://www.aliexpress.us/item/1005005150575666.html">AliExpress Product Page 3</a></li>
  </ul>

  <h2>Prerequisites</h2>

  <ul>
    <li>Python 3.x</li>
    <li>pyserial library</li>
  </ul>

  <h2>Installation</h2>

  <p>Install the required Python libraries:</p>

  <pre><code>pip install pyserial
</code></pre>

  <h2>RS485 Serial Port Configuration</h2>

  <ul>
    <li>Baud rate: 2400</li>
    <li>Check bit: NONE</li>
    <li>Data bit: 8</li>
    <li>Stop bit: 1</li>
  </ul>

  <p>Replace <code>/dev/ttyUSB2</code> in the script with the appropriate serial port for your system. To find the port reboot, plug out and plugin your adapter and enter this command:</p>

  <pre><code>dmesg | grep ttyUSB</code></pre>

  <p>Connect cables using a RJ12 6P6C terminal adapter. I had success with a FT232-Chip RS485 adapter. See <a href="https://github.com/christian1980nrw/RS485-read-China-MPPT-Charger/blob/main/RS485-connection.jpg">RS485 Connection</a> for details.</p>

<ul>
  <li><a href="https://de.aliexpress.com/item/1005005816164732.html">AliExpress Product Page 1</a></li>
  <li><a href="https://de.aliexpress.com/item/32850797209.html">AliExpress Product Page 2</a></li>
</ul>

  <h3>Query MPPT Charger</h3>

  <p>Ensure permission for serial port:</p>

  <pre><code>sudo chmod 666 /dev/ttyUSB2</code></pre>

  <p>Run Python script to query charger:</p>

  <pre><code>sudo python3 query-mppt-charger.py to test if your charger is answering</code></pre>

  <h3>Example Output</h3>

  <pre><code>root@raspberrypi4:~# python3 /data/query-charger.py
  MPPT Charger Data:
  address: 1
  device_type: 1
  dc_output_status: 0
  excessive_internal_temperature: False
  high_battery_temperature: False
  dc_output_overcurrent: False
  pv_overvoltage: False
  pv_voltage_too_low: False
  charging_voltage_too_high: False
  fast_charging: False
  uniformly_charging: False
  float_charge: False
  max_power_point_tracking: False
  standby: True
  charging_voltage_percentage: 91
  system_charging_voltage_percentage: 0
  battery_type: 4
  system_set_equalization_voltage: 54.7
  system_set_float_voltage: 54.5
  system_set_discharge_limit_voltage: 45.6
  system_charging_current_limit: 60.0
  photovoltaic_input_voltage: 0.0
  charging_voltage: 53.7
  charging_current: 0.0
  charging_power: 0.0
  battery_voltage: 53.7
  dc_output_current: 0.0
  module_temperature: 29
  external_battery_temperature: 25
  total_energy_generated: 75.016
</code></pre>

  <p>or read with mbpoll:</p>

  <pre><code>$ mbpoll /dev/ttyUSB2 -m rtu -b 2400 -P none -d 8 -s 1 -v -a 1 -r 1 -t4:int16 -c20 -1
  debug enabled
  iGetIntList(1)
  Integer found: 1
  iCount=1
  iGetIntList(1)
  Integer found: 1
  iCount=1
  Set function=4
  Set format=int16
  Set number of values=20
  Set device=/dev/ttyUSB0
  mbpoll 1.0-0 - FieldTalk(tm) Modbus(R) Master Simulator
  Copyright (c) 2015-2023 Pascal JEAN, https://github.com/epsilonrt/mbpoll
  This program comes with ABSOLUTELY NO WARRANTY.
  This is free software, and you are welcome to redistribute it
  under certain conditions; type 'mbpoll -w' for details.

  Opening /dev/ttyUSB0 at 2400 bauds (N, 8, 1)
  Set response timeout to 1 sec, 0 us
  Protocol configuration: Modbus RTU
  Slave configuration...: address = [1]
                          start reference = 1, count = 20
  Communication.........: /dev/ttyUSB0,       2400-8N1 
                          t/o 1.00 s, poll rate 1000 ms
  Data type.............: 16-bit register, output (holding) register table

  -- Polling slave 1...
  [01][03][00][00][00][14][45][C5]
  Waiting for a confirmation...
  <01><03><28><00><01><00><01><00><01><02><10><00><45><00><00><00><04><02><3A><02><36><01><E0><02><BC><06><BC><02><1C><00><3E><02><1C><00><00><00><2C><00><00><00><0F><A2><A2><FF><E5>
  [1]:    1
  [2]:    1
  [3]:    1
  [4]:    528
  [5]:    69
  [6]:    0
  [7]:    4
  [8]:    570
  [9]:    566
  [10]:   480
  [11]:   700
  [12]:   1724
  [13]:   540
  [14]:   62
  [15]:   540
  [16]:   0
  [17]:   44
  [18]:   0
  [19]:   15
  [20]:   -23902</code></pre>
