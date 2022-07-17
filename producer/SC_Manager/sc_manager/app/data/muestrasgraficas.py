import pandas as pd
import matplotlib.pyplot as plt  
from pylab import*
from matplotlib import pyplot
import array as arr
from numpy import array
from numpy import *
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.cbook as cbook 
import matplotlib.image as image 
import matplotlib.patches as patches

d3=[]
d4=[]
d5=[]

with open('ecg_data_3.csv','r') as reader:
	valores=reader.read().splitlines()
	for l in valores:
		s=l.split(',')
		#print(s)
		d3.append(s[1])

with open('ecg_data_4.csv','r') as reader4:
	valores4=reader4.read().splitlines()
	for l4 in valores4:
		s4=l4.split(',')
		#print(s)
		d4.append(s4[1])

with open('ecg_data_5.csv','r') as reader5:
	valores5=reader5.read().splitlines()
	for l5 in valores5:
		s5=l5.split(',')
		#print(s)
		d5.append(s5[1])


plt.figure(1)
host = host_subplot(111)
host.set_ylim(-0.5,1)
p1=host.plot(d3,color='b')
plt.title("ecg_data_3")  
host.legend()

plt.figure(2)
host = host_subplot(111)
host.set_ylim(-0.5,1)
p1=host.plot(d4,color='b')
plt.title("ecg_data_4")  
host.legend()

plt.figure(3)
host = host_subplot(111)
host.set_ylim(-0.5,1)
p1=host.plot(d5,color='b')
plt.title("ecg_data_5")  
host.legend()

plt.draw()
plt.show()
