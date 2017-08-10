import matplotlib.pyplot as plt
from pylab import *
import matplotlib.animation as animation
from matplotlib import style

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    global labels
    graph_data = open('trend.csv', 'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines[1:]:
        if len(line) > 1:
            args = line.split(",")
            x = args[0]
            y = args[3]
            xs.append(x)
            ys.append(y)
    ax1.clear()
    ax1.plot(xs, ys)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
"""
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax2 = fig.add_subplot(1,1,1)
def animate(i):
    global labels
    graph_data = open('trend.csv', 'r').read()
    lines = graph_data.split('\n')
    mainxs = []
    mainys = []
    dhbxs = []
    dhbys = []
    for line in lines[1:]:
        if len(line) > 1:
            args = line.split(",")
            x = args[0]
            y = args[3]
            if (args[2]=="Main (kW)"):
                mainxs.append(x)
                mainys.append(y)
            elif (args[2] == "DHB (kW)"):
                dhbxs.append(x)
                dhbys.append(y)
    ax1.clear()
    ax1.plot(mainxs, mainys)
    ax2.clear()
    ax2.plot(dhbxs, dhbys)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
"""