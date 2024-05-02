#parse the data.txt file and obtain the imu data

import re
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

"""
Data format:
ax 0.0     ay 0.0     az 0.0     gx 0.0     gy 0.0     gz 0.0     Temperature 0.0

"""

def parse_data(file):
    with open(file, 'r') as f:
            data = f.readlines()
    
    ax = []
    ay = []
    az = []
    gx = []
    gy = []
    gz = []
    temperature = []
    
    for line in data:
        try : 
            line = line.split()
            ax.append(float(line[1]))
            ay.append(float(line[3]))
            az.append(float(line[5]))
            gx.append(float(line[7]))
            gy.append(float(line[9]))
            gz.append(float(line[11]))
            temperature.append(float(line[13]))
        except:
            print('Error parsing line:', line)
        
    return ax, ay, az, gx, gy, gz, temperature

#parse the data
ax, ay, az, gx, gy, gz, temperature = parse_data('data.txt')

#plot the data with subplots
fig, axs = plt.subplots(3, 2, figsize=(15, 10))
fig.suptitle('IMU Data')
axs[0, 0].plot(ax, label='ax')
axs[0, 0].set_title('ax')
axs[0, 1].plot(ay, label='ay')
axs[0, 1].set_title('ay')
axs[1, 0].plot(az, label='az')
axs[1, 0].set_title('az')
axs[1, 1].plot(gx, label='gx')
axs[1, 1].set_title('gx')
axs[2, 0].plot(gy, label='gy')
axs[2, 0].set_title('gy')
axs[2, 1].plot(gz, label='gz')
axs[2, 1].set_title('gz')
plt.show()

#plot the temperature
plt.plot(temperature, label='temperature')
plt.title('Temperature')
plt.show()




    
            