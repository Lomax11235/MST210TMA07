import matplotlib.pyplot as plt
from matplotlib.figure import figaspect
from math import ceil
import csv

v_0=31.2928 #70 mph
a_0=-1 #accerlation
T=0.7 # Thinking time
t_c=0.3 # Time interval
lines_to_ignore=20 # Lines get very close, so we need to ingore the last 20-30 m
m_max = ceil(T/t_c) # Number of lines without breaking
n_max = ceil(-v_0/(a_0*t_c)) # Number of lined with breaking
lines=[] # Arry to store data
line_no =0 #line count for data output

#Plot config
w, h = figaspect(1/6)
fig, ax = plt.subplots(figsize=(w,h))
ax.xaxis.labelpad = -10
ax.get_yaxis().set_visible(False)
ax.set_ylim([0.75, 2.5])
plt.xlabel('Distance/m')

#Calc thinking lines
for m in range(0,m_max):
    x=m*t_c*v_0 # Line distance
    
    if m ==0:
        lines.append([line_no,'Thinking',x,0])#Add to data output, no spacing for first line
        plt.plot([x,x],[1,2],'b', label='thinking')#Add line to plot with legend
    else:
        lines.append([line_no,'Thinking',x,x-lines[line_no-1][2]])#Add to data output
        plt.plot([x,x],[1,2],'b')#Add line to plot with

    line_no+=1
x_m_max= x # Total thinking distance


#Calc breaking lines
for n in range(1,n_max-lines_to_ignore):
    x=((v_0+n*t_c*a_0)**2-v_0**2)/(2*a_0)+x_m_max# Line distance

    if n ==1:
        plt.plot([x,x],[1,2],'r',label='breaking')#Add line to plot with legend
    else:
        plt.plot([x,x],[1,2],'r')#Add line to plot with
    lines.append([line_no,'Breaking',x,x-lines[line_no-1][2]])#Add to data output
    line_no+=1


#Add juntion
x=(-v_0**2)/(2*a_0)+x_m_max
plt.plot([x,x],[1,2],'g', label='junction') #Junction

#Writee data to CSV file
f = open('data.csv', 'w')
writer = csv.writer(f)
headers = ['line','state' ,'distance','spacing'] # headers
with open(r'data.csv', 'w',newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(["velocity (v_0)m/s",v_0])
    writer.writerow(["acceleration (a_0)m/s^2",a_0])
    writer.writerow(["Thinking time (T) s",T])
    writer.writerow(["Time interval (t_c)s",t_c])
    writer.writerow(["lines ignored",lines_to_ignore])
    writer.writerow(["m_max",m_max])
    writer.writerow(["n_max",n_max])
    writer.writerow([])
    writer.writerow(headers)#write headers

    for line in lines:
        writer.writerow(line)#write line date
f.close # Make sure the CSV is closed

#Plot the graph
plt.legend(loc='upper center',ncol=3)#Add legend
plt.savefig('viz.png', format='png', dpi=1200)#Save image
plt.show()#Show the plot
