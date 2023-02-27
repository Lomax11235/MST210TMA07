
#rev 4 2023-02-26
#tested in python 3.11

import matplotlib.pyplot as plt
from matplotlib.figure import figaspect
from math import ceil,sqrt
import csv

#variables
v_0=31.29#70 mph 31.2928
a_0=-1.14 #accerlation
T=0.7 # Thinking time
t_c=0.25 # Time interval
v_target=10 # targer v for last line

#Parameters
m_max = ceil(T/t_c) # Number of lines without breaking
n_max = ceil(-v_0/(a_0*t_c)) # Number of lined with breaking
t_target = (v_target-v_0)/a_0 + T# The time taken to get to v_target including thinking time
L_target= ceil(t_target/t_c) # The line at which the target is reached
lines_to_ignore= m_max+n_max- L_target # the number of line to discard
lines=[] # Arry to store data
line_no =0 #line count for data output
v_arr=[]
x_arr = []
t_arr = []

#Plot config
w, h = figaspect(1/6)
fig, ax = plt.subplots(figsize=(w,h))
ax.xaxis.labelpad = -30
ax.get_yaxis().set_visible(False)
ax.set_ylim([-0.5, 1.5])
plt.xlabel('Distance/(m)')
x=0
#Calc thinking lines
if T>0:
    for m in range(0,m_max):
        x=m*t_c*v_0 # Line distance
        t=m*t_c
        v_arr.append(v_0)
        x_arr.append(x)
        t_arr.append(t)
        if m ==0:
            lines.append([line_no,t,v_0,'Thinking',x,0])#Add to data output, no spacing for first line
            ax.plot([x,x],[0,1],'navy', label='thinking')#Add line to plot with legend
        else:
            lines.append([line_no,t,v_0,'Thinking',x,x-lines[line_no-1][4]])#Add to data output
            ax.plot([x,x],[0,1],'navy')#Add line to plot with

        line_no+=1
    x_m_max= x # Total thinking distance
    t_T=m_max*t_c # Total thinking time


    n_start= 1
else:
    n_start= 0
    x_m_max= 0 # Total thinking distance
    t_T=0 # Total thinking time


#Calc breaking lines
for n in range(n_start,n_max):
   
    v= v_0+n*t_c*a_0
    x=(v**2-v_0**2)/(2*a_0)+x_m_max# Line distance
    t=t_T+n*t_c
    v_arr.append(v)
    x_arr.append(x)
    t_arr.append(t)
    if (n_max-n)>lines_to_ignore:
        if n ==1:
            ax.plot([x,x],[0,1],'darkcyan',label='breaking')#Add line to plot with legend
        else:
            ax.plot([x,x],[0,1],'darkcyan')#Add line to plot with
    if n>0:
        lines.append([line_no,t,v,'Breaking',x,x-lines[line_no-1][4]])#Add to data output
    else:
        lines.append([line_no,t,v,'Breaking',0])#Add to data output
        
    line_no+=1

#Add juntion
x=(-v_0**2)/(2*a_0)+x_m_max
ax.plot([x,x],[0,1],'dimgrey', label='junction') #Junction

#Writee data to CSV file
f = open('data.csv', 'w')
writer = csv.writer(f)
headers = ['line','t','v','state' ,'distance','spacing'] # headers
with open(r'data.csv', 'w',newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    #write variables
    writer.writerow([])
    writer.writerow(['variables'])
    writer.writerow(['velocity (v_0)m/s',v_0])
    writer.writerow(['acceleration (a_0)m/s^2',a_0])
    writer.writerow(['Thinking time (T) s',T])
    writer.writerow(['Time interval (t_c)s',t_c])
    writer.writerow(['v_target m/s',v_target])
    writer.writerow([])
    #write parameters
    writer.writerow(['parameters'])
    writer.writerow(['t_tartget s',t_target])
    writer.writerow(['lines ignored',lines_to_ignore])
    writer.writerow(['m_max',m_max])
    writer.writerow(['n_max',n_max])
    writer.writerow([])
    writer.writerow(headers)#write headers
    for line in lines:
        writer.writerow(line)#write line date
f.close # Make sure the CSV is closed

#plot velocity graph with differnt y-axis
ax2 = ax.twinx()
ax2.plot(x_arr,v_arr,'firebrick',label='velocity')
ax2.set_ylabel('velcoity/(m/s)', color='firebrick')
ax2.legend(loc='upper right',ncol=1)


def time(x): # Function to calcualte t from x
    if x>x_m_max:
        x=x-x_m_max
        v = sqrt(abs(v_0**2+2*x*a_0))
        return (v-v_0)/a_0 + t_T
    else:
        return x/v_0

#Get ticks for time axis
y1_ticks=[] # x values for second x axis
y3_ticks=[] # t values for second x axis

y1_max =x_arr[-1]
no_of_ticks =15

for i in range (0,no_of_ticks +1): # Make ticks for time axis
    x=i*y1_max/no_of_ticks
    y1_ticks.append(x)
    y3_ticks.append("{:0.1f}".format(time(x)))
ax.set_xticks(y1_ticks)

#Add time axis
ax3 = ax.twiny()
ax3.set_xticks(y1_ticks)
ax3.set_xticklabels(y3_ticks)
ax3.set_xlabel('time/(s)')
ax3.xaxis.labelpad = -30
ax3.plot([0,y1_max],[10,10],'dimgrey', label='junction') #dummy plot to get padding correct for time axis

ax.legend(loc='lower left',ncol=3)#Add legend for lines plot
plt.savefig('viz.png', format='png', dpi=1200)#Save image
plt.show()#Show the plot
