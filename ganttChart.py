#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Gantt.py
Date: 6/25/2017
Author: Wayne Snyder
Purpose: This is code supplied with the final homework in CS 237;
         it will display various charts after a simulation
         of an MM1 queueing simulation. 
"""


import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import math
import random
import pandas as pd

def round4(x):
    return round(x+0.00000000001,4)


# A task is list [arrival time, service request, cpu start time]

# We assume in this simulation that no tasks arrive at the same time, and are 
# presented in order. 
# Last component is initialized as 0, to be filled in during simulation


# Here are four example schedules, without statistics filled in

ex0 = [[0,1,0], [2,2,0], [3,1,0], [4,3,0], [5,5,0]]

ex1 = [[0, 1.0, 0], [0.5, 0.3, 0], [1.4, 1, 0], [1.9, 0.25, 0], [2.0, 0.5, 0]]

ex2 = [[0,2.1,0], [1.9,2.34,0], [3.56,4.1,0], [4.12,3.4,0], [5.2,2.43,0]]

ex3 = [[0,2,0], [1.1,3,0], [3.4,4,0], [3.45,3,0], [5,3.23,0],[6.2,2.9,0],[6.4,2.32,0], [9.99,1.2,0], [10.3,3.4,0], [12.8,3.9,0], [15.2,3.4,0],
       [15.67,2.43,0],[17.01,2.8,0],[18.8,2.2,0],[20.1,2.99,0],[21.7,5.34,0],[24.4,2.2,0]]



# Simulation will fill in last component in task (starting time in cpu); here are the results
# of my simulations, which will serve to demonstrate the code in this file

finished0 = [[0, 1, 0], [2, 2, 2], [3, 1, 4], [4, 3, 5], [5, 5, 8]]
finished1 = [[0, 1.0, 0], [0.5, 0.3, 1.0], [1.4, 1, 1.4], [1.9, 0.25, 2.4], 
             [2.0, 0.5, 2.65]]
finished2 = [[0, 2.1, 0], [1.9, 2.34, 2.1], [3.56, 4.1, 4.44], 
             [4.12, 3.4, 8.54], [5.2, 2.43, 11.94]]
finished3 =  [[0, 2, 0], [1.1, 3, 2], [3.4, 4, 5], [3.45, 3, 9], [5, 3.23, 12], 
              [6.2, 2.9, 15.23], [6.4, 2.32, 18.13], [9.99, 1.2, 20.45], 
              [10.3, 3.4, 21.65], [12.8, 3.9, 25.05], [15.2, 3.4, 28.95], 
              [15.67, 2.43, 32.35], [17.01, 2.8, 34.78], [18.8, 2.2, 37.58], 
              [20.1, 2.99, 39.78], [21.7, 5.34, 42.77], [24.4, 2.2, 48.11]]

def displayResults(task): 
          
    # Print GANTT Chart
    
    fig = plt.figure(figsize=(15,10))
    fig.subplots_adjust(hspace=.5)
    ax1 = fig.add_subplot(311)       
    plt.yticks(range(len(task)))    
    plt.ylim((-0.5,len(task)))
    plt.title('GANTT Chart')
    plt.ylabel('Task Number')
    plt.xlabel('Time Slot')    
      
    for k in range(len(task)):
        plt.hlines(k, task[k][0], task[k][2], color='C0',linestyle='dotted',linewidth=4)
        plt.hlines(k, task[k][2], task[k][1]+task[k][2], color='C0',linestyle='solid',linewidth=4)         
    
    # Now figure out CPU utilization in each time slot

    # first figure out all possible cpu event times
    
    bins = []
    
    for k in range(len(task)):
        bins.append(task[k][2])
        bins.append(task[k][1]+task[k][2])
       
    bins = list(set(bins))
    bins.sort()
    
    X = []
    for i in range(len(task)):
        X.append(task[i][2]) 
   
    # Display CPU Utilization Chart
    
    fig.add_subplot(312,sharex=ax1)
    plt.hist(X,bins,ec='k')    
    plt.title('CPU Utilization')    
    plt.ylabel('Usage')
    plt.xlabel('Time Slot')    
    plt.ylim((0,1.25))
   
    # Calculate Queue Length Distribution
    
    bins = []
    
    for k in range(len(task)):
        bins.append(task[k][0])
        bins.append(task[k][2])
       
    bins = list(set(bins))
    bins.sort()
    
    X = []
    for k in range(len(bins)):
        for i in range(len(task)):
            if(task[i][0] <= bins[k] < task[i][2]):
                X.append(bins[k])     
   
    fig.add_subplot(313,sharex=ax1) 
    plt.hist(X,bins,ec='k')
    plt.title('Queue Length over Time')
    plt.ylabel('Length of Queue')
    plt.xlabel('Time Slot')
    plt.show()
        

print("\nSimulation Example 0\n")
print("Task list input to simulation: " + str(ex0)+'\n')
print("Task list output from simulation: " + str(finished0)+'\n')
displayResults(finished0)
 
print("\nSimulation Example 1\n")
print("Task list input to simulation: " + str(ex1)+'\n')
print("Task list output from simulation: " + str(finished1)+'\n')
displayResults(finished1)
 
print("\nSimulation Example 2\n")
print("Task list input to simulation: " + str(ex2)+'\n')
print("Task list output from simulation: " + str(finished2)+'\n')
displayResults(finished2)
 
print("\nSimulation Example 3\n")
print("Task list input to simulation: " + str(ex3)+'\n')
print("Task list output from simulation: " + str(finished3)+'\n')
displayResults(finished3) 