
#rev 5 2023-02-27
#tested in python 3.11

import matplotlib.pyplot as plt
from matplotlib.figure import figaspect
from math import ceil,sqrt
import csv

#variables
v_0=31.29#70 mph 31.2928
a_0=-1.14 #accerlation
T=0.67 # Thinking time
t_c=0.25 # Time interval
v_target=10 # targer v for last line
distance_from_junction = False#set if first line or the junction is the dataum


#Parameters
m_max = ceil(T/t_c) # Number of lines without breaking
n_max = ceil(-v_0/(a_0*t_c)) # Number of lined with breaking

x_max = (m_max-1) *t_c *v_0 + v_0*t_c*n_max+0.5*a_0*(t_c*n_max)**2 #Total distance from line 0 to the junction

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
            lines.append([line_no,"{:0.5f}".format(t),"{:0.5f}".format(v_0),'Thinking',"{:0.5f}".format(x),"{:0.5f}".format(x_max),"{:0.5f}".format(0)])#Add to data output, no spacing for first line
            ax.plot([x,x],[0,1],'navy', label='thinking')#Add line to plot with legend
        else:
            
            lines.append([line_no,"{:0.5f}".format(t),"{:0.5f}".format(v_0),'thinking',"{:0.5f}".format(x),"{:0.5f}".format(x_max-x),"{:0.5f}".format(x-prev_x)])#Add to data output
            ax.plot([x,x],[0,1],'navy')#Add line to plot with

        line_no+=1
        prev_x = x
    x_m_max= x # Total thinking distance
    t_T=m_max*t_c # Total thinking time


    n_start= 1
else:
    n_start= 0
    x_m_max= 0 # Total thinking distance
    t_T=0 # Total thinking time


#Calc breaking lines
for n in range(n_start,n_max+1):
   
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
        lines.append([line_no,"{:0.5f}".format(t),"{:0.5f}".format(v),'Breaking',"{:0.5f}".format(x),"{:0.5f}".format(x_max-x),"{:0.5f}".format(x-prev_x)])#Add to data output
    else:
        lines.append([line_no,"{:0.5f}".format(t),"{:0.5f}".format(v_0),'breaking',"{:0.5f}".format(x),"{:0.5f}".format(x_max),"{:0.5f}".format(0)])#Add to data output
    prev_x = x    
    line_no+=1

#Add juntion

ax.plot([x_max,x_max],[0,1],'dimgrey', label='junction') #Junction

#Writee data to CSV file
f = open('data.csv', 'w')
writer = csv.writer(f)
headers = ['line','t','v','state' ,'distance from line 0','distance from junction','spacing'] # headers
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
    writer.writerow(['x_max',n_max])
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
y_ticks=[] # x values for second x axis
y_time_lables=[] # t values for second x axis
y_from_line_0_lables=[] #Reverse lables
y_from_juntion_lables=[] #forwards lables
y_max =x_arr[-1]
no_of_ticks =15

for i in range (0,no_of_ticks +1): # Make ticks for time axis
    x=i*y_max/no_of_ticks
    y_ticks.append(x)
    y_from_line_0_lables.append("{:0.0f}".format(x_max-x))
    y_from_juntion_lables.append("{:0.0f}".format(x))
    y_time_lables.append("{:0.1f}".format(time(x)))
ax.set_xticks(y_ticks)

if distance_from_junction: #set if first line or the junction is the dataum
    ax.set_xticklabels(y_from_juntion_lables)
else:
    ax.set_xticklabels(y_from_line_0_lables)

#Add time axis
ax3 = ax.twiny()
ax3.set_xticks(y_ticks)
ax3.set_xticklabels(y_time_lables)
ax3.set_xlabel('time/(s)')
ax3.xaxis.labelpad = -30
ax3.plot([0,y_max],[10,10],'dimgrey', label='junction') #dummy plot to get padding correct for time axis

ax.legend(loc='lower left',ncol=3)#Add legend for lines plot
plt.savefig('viz.png', format='png', dpi=1200)#Save image
plt.show()#Show the plot
