#simulation to analyze probability of events in the game pokemon (for fun)
import random
import numpy
def round4(x):
    return round(float(x)+0.00000000001,4)
def simulateShiny():
    #probability is 1 in 8192
    counter = 0
    attempt = 0
    while(attempt != 900):
        attempt = random.randint(1,1892)
        counter += 1
    return counter

def getShinyData(n):
    #n is the amount of attempts, if you want a relatively accurate number in a small amount of time us n = 10000, n = 1000000 will get the most accurate results
    results = [0] * n
    for x in range(n):
        results[x] = simulateShiny()
    maxAttempts = max(results)
    average = numpy.mean(results)
    minimum = min(results)
    print('Average amount of attempts for shiny out of ' + str(n) + ' attempts: ' + str(numpy.mean(results)))
    print('Maximum amount of attempts for shiny out of ' + str(n) + ' attempts: ' + str(maxAttempts))
    print('Minimum amount of attempts for shiny out of ' + str(n) + ' attempts: ' + str(minimum))
    
def binomialShiny():
    #simulates a single encounter
    if random.randint(1,8192) == 69:
        return True
    else:
        return False
    
def simulateGame(encounters):
    #more effecient simulation, can do n = 1000000 much quicker
    #encounters is the total amount of pokemon encounters in a single playthrough of the game
    results = [0] * encounters
    for x in range(encounters):
        if binomialShiny():
            results[x] += 1
    encounterPercent = sum(results) / encounters
    print('Total number of shiny encounters: ' + str(sum(results)) + ' out of ' + str(encounters) + ' total encounters')
    print(str(round4(encounterPercent)) + '% of encounters were shiny pokemon')
    
