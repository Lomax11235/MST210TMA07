#rev 7 2023-02-28
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
#set if first line or the junction is the dataum
distance_from_junction = False
fw=0.5 # front wheel to bumper
wb=1.5#Wheele Base
# Take into accout fw to bonnect and wb wheel base
include_car_dimentions =True 
if include_car_dimentions :
    out_offset=8
else:
    out_offset=-2

    
def time(x): # Function to calcualte t from x
    if x>x_m_max:
        x=x-x_m_max
        v = sqrt(abs(v_0**2+2*x*a_0))
        return (v-v_0)/a_0 + t_T
    else:
        return x/v_0

#Parameters
m_max = ceil(T/t_c) # Number of lines without breaking
n_max = ceil(-v_0/(a_0*t_c)) # Number of lined with breaking
 # Total thinking distance
t_T=(m_max)*t_c # Total thinking time
x_m_max= t_T*v_0
#Total distance from line 0 to the junction
x_max = (m_max) *t_c *v_0 + v_0*t_c*n_max+0.5*a_0*(t_c*n_max)**2 
# The time taken to get to v_target including thinking time
t_target = (v_target-v_0)/a_0 + T
L_target= ceil(t_target/t_c) # The line at which the target is reached

lines_to_ignore= m_max+n_max- L_target # the number of line to discard
lines=[] # Arry to store data
line_no =0 #line count for data output
v_arr=[]
x_arr = []
t_arr = []
#Plot config
w, h = figaspect(1/5)
fig, ax = plt.subplots(figsize=(w,h))
ax.xaxis.labelpad = 0
ax.get_yaxis().set_visible(False)
ax.set_ylim([-0.25, 1.25])
plt.xlabel('Distance/(m)')


x=0
#Calc thinking lines
if T>0:
    for m in range(0,m_max+1):
        x=m*t_c*v_0 # Line distance
        t=m*t_c
        v_arr.append(v_0)
        x_arr.append(x)
        t_arr.append(t)
        if m ==0:
            #Add to data output, no spacing for first line
            lines.append([str(line_no)+" (T)",
                          t,
                          v_0,
                          x,
                          x_max-x,
                         0,
                         time(x+fw),
                         time(x+fw+wb)])
            
            #Add line to plot with legend
            ax.plot([x,x],[0,1],'navy', label='thinking line')
            if include_car_dimentions :
                ax.plot([x+wb+fw,x+wb+fw],[0.75,1],'red' ,label='rear axle click')
                ax.plot([x+fw,x+fw],[0,0.25],'green' ,label='front axle click')
        else:
            
            lines.append([str(line_no)+" (T)",
                          t,
                          v_0,
                          x,
                          x_max-x,
                         x-prev_x,
                         time(x+fw),
                         time(x+fw+wb)])
            #Add to data output
            ax.plot([x,x],[0,1],'navy')
            if include_car_dimentions :
                ax.plot([x+wb,x+wb],[0.75,1],'red')
                ax.plot([x+fw,x+fw],[0,0.25],'green')

        line_no+=1
        prev_x = x


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
            #Add line to plot with legend
            ax.plot([x,x],[0,1],'darkcyan',label='breaking line')
            if include_car_dimentions :  
                ax.plot([x+wb,x+wb],[0.75,1],'red')
                ax.plot([x+fw,x+fw],[0.0,0.25],'green')
        else:
            #Add line to plot   
            ax.plot([x,x],[0,1],'darkcyan')
            if include_car_dimentions :           
                ax.plot([x+wb,x+wb],[0.75,1],'red')
                ax.plot([x+fw,x+fw],[0,0.25],'green')
    if n>0:
        #Add to data output
        lines.append([str(line_no)+" (B)",
                          t,
                          v_0,
                          x,
                          x_max-x,
                         x-prev_x,
                         time(x+fw),
                         time(x+fw+wb)])
            
    else:
        lines.append([str(line_no)+" (B)",
                          t,
                          v_0,
                          x,
                          x_max-x,
                         0,
                         time(x+fw),
                         time(x+fw+wb)])
            #
    prev_x = x    
    line_no+=1


    


#Add juntion
ax.plot([x_max,x_max],[0,1],'dimgrey', label='junction') #Junction
#Write data to CSV file
f = open('data.csv', 'w')
writer = csv.writer(f)
headers = ['line',
           'time s',
           'velocity m/s',
            'distance from line 0 m',
           'distance from junction m',
           'spacing m',
           'time for 1st click s',
           'time for 2nd click s' ]
#Remove last to headers is no car dimentions used
headers=headers[:out_offset] 

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
        #Truncate lines if nessesary
        line=line[:out_offset] 
        writer.writerow(line)#write line date 
f.close # Make sure the CSV is closed

#Make latex table for the report
f = open('latex.tex', 'w')

headers = ['line',
           'time /s',
           r'velocity /ms\textsuperscript{-1}',
            'dist. from line 0 /m',
           'dist. from junction /m',
           'spacing /m',
           '1st click /s',
           '2nd click /s' ] 
    
headers=headers[:out_offset] 
writer = csv.writer(f)
with open(r'latex.tex', 'w',newline='', encoding='UTF8') as f:
    writer = csv.writer(f, delimiter ='&',quoting=csv.QUOTE_MINIMAL)

    if include_car_dimentions :
        writer.writerow([r'\newpage\begin{landscape}\small{\begin{longtable}{c|c|c|c|c|c|c|c}'])
        writer.writerow([r'\caption{Stopping lines for '+
                     '$v_0={0}$, $a_0={1}$,$T={2}$ and $t_c={3}$, dist. bumper to axle ${4}$m, wheelbase ${5}$m'
                     .format(v_0,a_0,T,t_c,fw,wb)
                     +r'}\\'])
    else:
        writer.writerow([r'\newpage\begin{landscape}\small{\begin{longtable}{c|c|c|c|c|c}'])
        writer.writerow([r'\caption{Stopping lines for '+
                     '$v_0={0}$, $a_0={1}$,$T={2}$ and $t_c={3}$'
                     .format(v_0,a_0,T,t_c)
                     +r'}\\'])
    headers[-1]=headers[-1] +r"\\\hline"
    writer.writerow(headers)#write headers
    for line in lines:
        #Truncate lines if nessesary
        line=line[:out_offset] 
        for i in range(2,len(line)):
          
            line[i]='{:0.4f}'.format(line[i])
         
        line[-1]=line[-1] + r" \\"
        writer.writerow(line)#write line date
    writer.writerow([r'\end{longtable}}\end{landscape}'])
f.close # Make sure the CSV is closed

#plot velocity graph with differnt y-axis
ax2 = ax.twinx()
ax2.plot(x_arr,v_arr,'firebrick',label='velocity')
ax2.set_ylabel('velcoity/(m/s)', color='firebrick')
ax2.legend(loc='upper right',ncol=1)



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
    y_from_line_0_lables.append("{:0.1f}".format(x_max-x))
    y_from_juntion_lables.append("{:0.1f}".format(x))
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
#dummy plot to get padding correct for time axis
ax3.plot([0,y_max],[10,10],'dimgrey', label='junction') 

ax.legend(loc='lower left',ncol=5)#Add legend for lines plot







plt.savefig('viz.png', format='png', dpi=1200)#Save image

