#parse the data.txt file and obtain the imu data

import re
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

"""
Data format:
ax 0.0     ay 0.0     az 0.0     gx 0.0     gy 0.0     gz 0.0     

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
            
        except:
            print('Error parsing line:', line)
        
    return ax, ay, az, gx, gy, gz

#parse the data
ax, ay, az, gx, gy, gz = parse_data('esra_normal_yuruyor.txt')

#plot the data with subplots
fig, axs = plt.subplots(3, 2, figsize=(15, 10))
fig.suptitle('IMU Data')
axs[0, 0].plot(ax[0:600], label='ax')
axs[0, 0].set_title('ax')
axs[0, 1].plot(ay[0:600], label='ay')
axs[0, 1].set_title('ay')
axs[1, 0].plot(az[0:600], label='az')
axs[1, 0].set_title('az')
axs[1, 1].plot(gx[0:600], label='gx')
axs[1, 1].set_title('gx')
axs[2, 0].plot(gy[0:600], label='gy')
axs[2, 0].set_title('gy')
axs[2, 1].plot(gz[0:600], label='gz')
axs[2, 1].set_title('gz')
plt.show()




    
            