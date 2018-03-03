#Nathan Mokhtarzadeh
#Simulates Queue-CPU utilization
#[Task arrival time, requested service time, time CPU serves task]
#Global variables:
ex0 = [[0,1,0], [2,2,0], [3,1,0], [4,3,0], [5,5,0]]
ex1 = [[0, 1.0, 0], [0.5, 0.3, 0], [1.4, 1, 0], [1.9, 0.25, 0], [2.0, 0.5, 0]]
ex3 = [[0,2,0], [1.1,3,0], [3.4,4,0], [3.45,3,0], [5,3.23,0],[6.2,2.9,0],[6.4,2.32,0], [9.99,1.2,0], [10.3,3.4,0], [12.8,3.9,0], [15.2,3.4,0],
       [15.67,2.43,0],[17.01,2.8,0],[18.8,2.2,0],[20.1,2.99,0],[21.7,5.34,0],[24.4,2.2,0]]
qLens = [0] * 100
prevClock = 0



import matplotlib.pyplot as plt
import random
import math
import numpy

prevClock = 0


def hist(P) :
    X = range(100)
    bins = [n - .5 for n in X]
    bins.append(max(X) + .5)
    plt.figure(figsize = (10,5))
    (a,b,y) = plt.hist(X,P, bins)
    plt.title("Basic Histogram")
    plt.ylabel("Frequency")
    plt.xlabel("Outcomes")
    plt.show()
    print("Frequencies: " + str(a))
    print("Bin boundaries: " + str(b))


def changeQ(L, clock):
    global prevClock
    if L < 100:
        qLens[L] += clock - prevClock
    prevClock = clock

def round4(x):
    return round(float(x)+0.00000000001,4)

def nextExponential(beta):
    numerator = -(math.log(random.random()))
    denominator = 1/beta
    return round4(numerator / denominator)

def createTaskArray(n, beta1, beta2):
    bigArray = [[0,0,0]] * n
    clock = 0
    for x in range(n):
        s = nextExponential(beta2)
        bigArray[x] = [clock, s, 0.0]
        t = nextExponential(beta1)
        clock += t
    return bigArray

def drawDistribution(X, P, title, CDF = False):
    bins = [n - .5 for n in X]
    bins.append(max(X) + .5)
    plt.figure(figsize = (10,5))
    if not CDF:
        (a,b,y) = plt.hist(X, bins, weights = P, normed = True)
        plt.title(title + " (PMF)")
        plt.xlabel("Outcomes")

    elif CDF:
        (a,b,y) = plt.hist(X, bins, weights = P, cumulative = True)
        plt.xlabel("Cumulative Distribution")
        plt.title(title + " (CDF)")
    plt.ylabel("Probability")
    plt.show()


def simulate(task):
    global qLens
    global prevClock
    qLens = [0] * 100
    prevClock = 0
    clock = 0
    state = 1
    finish = 0
    nxt = 0

    while (nxt < len(task) or state != 1):
        #print('clock: ' + str(clock) + "  state: " + str(state) + " finish: " + str(finish) + " nxt: " + str(nxt))
        if state == 1:
            #arrival
            
            clock = task[nxt][0]      # next event must be an arrival, but goes right to cpu
            cpu = nxt
            nxt += 1
            task[cpu][2] = round4(clock)
            finish = clock + task[cpu][1]
            
            state = 2
        elif state == 2:
            if(nxt >= len(task) or finish <= task[nxt][0]):# next event is finish
                clock = finish
                cpu = -1
                state = 1
            else:                           # next event is arrival
                clock = task[nxt][0]
                changeQ(nxt - cpu - 1, clock)
                nxt += 1
                state = 3
        elif(nxt >= len(task) or finish <= task[nxt][0]): # next event is finish
            
            clock = finish
            changeQ(nxt - cpu - 1, clock)
            cpu += 1
            task[cpu][2] = round4(clock)
            finish = clock + task[cpu][1]
            if nxt == cpu + 1:
                state = 2
            
            
        else:                                   # next event is arrival
            clock = task[nxt][0]
            changeQ(nxt - cpu - 1, clock)
            nxt += 1
            state = 3
        
    
    changeQ(0,clock)
    #Statistical Analysis:
    totalWaitTime = 0
    maxWaitTime = 0
    waitTimeArray = [0] * len(task)
    
    for x in range(len(task)):
        totalWaitTime += task[x][2] - task[x][0]
        waitTimeArray[x] = task[x][2] - task[x][0]
        if task[x][2] - task[x][0] > maxWaitTime:
            maxWaitTime = task[x][2] - task[x][0]
    
    
    interarrivalTimeArray = [0] * (len(task) - 1)
    meanWaitTime = numpy.mean(waitTimeArray)
    
    
    for x in range(len(task) - 1):
        interarrivalTimeArray[x] = task[x + 1][0] - task[x][0]
        
        
    meanInterarrivalTime = numpy.mean(interarrivalTimeArray)
    totalTime = task[-1][1] + task[-1][2]
    
    print('Total waiting time: ' + str(round4(totalWaitTime)) + ' seconds')
    print('Maximum waiting time: ' + str(round4(maxWaitTime)) + ' seconds')
    print('Mean waiting time: ' + str(round4(numpy.mean(waitTimeArray))) + ' seconds')
    
    totalExecutionTime = 0
    for x in range(len(task)):
        totalExecutionTime += task[x][1]
    serverUtilization = round4(totalExecutionTime / totalTime)
    
    print('Server utilization: ' + str(serverUtilization*100) + '%')
    print('Mean interarrival time: ' + str(meanInterarrivalTime) + ' seconds')
    print('Mean wait time / mean interarrival time: ' + str(round4(meanWaitTime / meanInterarrivalTime)))
    #print('clock: ' + str(clock) + "  state: " + str(state) + " finish: " + str(finish) + " nxt: " + str(nxt))
    print('Total time: ' + str(totalTime) + ' seconds')
    qLenProb = [x / totalTime for x in qLens]
    drawDistribution(range(len(qLenProb)),qLenProb, "Queue Length Distribution")
    meanQLength = numpy.mean(qLens)

    
    
    
    #return task
    

    
    
    
