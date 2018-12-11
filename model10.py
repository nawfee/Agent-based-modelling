# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 14:24:25 2018

@author: gy18smn
"""

import matplotlib
matplotlib.use('TkAgg')
import tkinter
import random
import matplotlib.pyplot
import agentframework
import csv
import matplotlib.animation 
import matplotlib.backends.backend_tkagg
import requests
import bs4

#request agents from a html
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})
print(td_ys)
print(td_xs)

#Read the CSV code and make an environment list
with open('in.txt', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    environment = []  #environment list
    for row in reader:
        rowlist = []
        for value in row:
           rowlist.append(value)
        environment.append(rowlist)


##make a plot of the environment        
matplotlib.pyplot.imshow(environment)
matplotlib.pyplot.show()
            

#Make the agent list and set the iteration 
num_of_agents = 10
num_of_iterations = 100
neighbourhood=20
agents = []

# Add a figure with axis
fig = matplotlib.pyplot.figure(figsize=(7,7))
ax = fig.add_axes([0, 0, 1, 1]) #ax.set_autoscale_on(False)

#Give environment to the agents and list of agents to each agent
for i in range(num_of_agents):
    y = int(td_ys[i].text)  #initialise with data from web
    x = int(td_xs[i].text)
    agents.append(agentframework.Agent(environment, agents, y ,x))

carry_on = True

#chnage the frames as animation runs, frame_number represents the number of time animation goes on
def update(frame_number):
    
    
    fig.clear()
    global carry_on
    
#if it gets a random number mentioned it stops
    if random.random() < 0.1:
            carry_on = False
            print("stopping condition")
        
#Move the agent and let them eat from the environment and share with neighbours
    for j in range(num_of_iterations):
     for i in range(num_of_agents):
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)
        

#create plot of agents in the environment        
    matplotlib.pyplot.xlim(0, 99)
    matplotlib.pyplot.ylim(0, 99)
    matplotlib.pyplot.imshow(environment)
    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y)
        
def gen_function(b = [0]):
    a = 0
    global carry_on #Not actually needed as we're not assigning, but clearer
    while (a < 10) & (carry_on) :
        yield a			# Returns control and waits next call.
        a = a + 1
      
 #run the animation
def run():
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False) #set the animation function 
    canvas.show()
    run(animation)
    
 #creating a window    
root = tkinter.Tk()      #builds the main window  
root.wm_title("Model")   #setting title of the main window

canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root) #createing a matplotlib canvas within our window   
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1) #sets layout of the matplotlip canvas

#creating a menu bar in the new window
menu_bar = tkinter.Menu(root)  
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run Model", command=run)


    
tkinter.mainloop()