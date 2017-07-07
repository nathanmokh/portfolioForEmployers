#Work in progress, meant to be used with Spyder IPython console
import random
import matplotlib.pyplot as plt

def round4(x):
    return round(float(x)+0.00000000001,4)

def getLocation(location):
    options = {0 : 'go',
               1: 'community chest',
                   2: 'baltic',
                   3: 'income tax',
                   4: 'reading railroad',
                   5: 'oriental',
                   6: 'chance',
                   7: 'vermont',
                   8: 'connecticut',
                   9: 'jail',
                   10: 'st charles',
                   11: 'electric company',
                   12: 'states',
                   13: 'virginia',
                   14: 'pennsylvania railroad',
                   15: 'st james',
                   16: 'community chest',
                   17: 'tennessee',
                   18: 'new york',
                   19: 'free parking',
                   20: 'kentucky',
                   21: 'chance',
                   22: 'indiana',
                   23: 'illonois',
                   24: 'b and o railroad',
                   25: 'atlantic',
                   26: 'venitor',
                   27: 'water works',
                   28: 'marvin gardens',
                   29: 'go to jail',
                   30: 'pacific',
                   31: 'north carolina',
                   32: 'community chest',
                   33: 'pennsylvania',
                   34: 'short line',
                   35: 'chance',
                   36: 'park place',
                   37: 'luxury tax',
                   38: 'boardwalk',
                }



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
    
def seeDiceProbability():
    X = [a for a in range(2,13)]
    P = [0.0279, 0.0557, 0.0833, 0.111, 0.1383, 0.1667, 0.1391, 0.1109, 0.0835, 0.0557, 0.0278]
    
    drawDistribution(X,P, 'Probability of Dice Rolls')
    
def simulateDice(n):
    results = [0] * 11
    for x in range(n):
        result = random.randint(1,6) + random.randint(1,6)
        results[result - 2] += 1
    print('dice roll results: ' )
    print(results)
    prob = [0.0] * 11
    for x in range(len(results)):
        prob[x] = round4(results[x] / n)
    print('dice roll probabilities:')
    print(prob)
    X = [a for a in range(2,13)]
    P = prob
    drawDistribution(X, prob, 'Probability of Dice Rolls')
    
class Property:
    def __init__(self, title, color, price, status):
        #if status == False, property is unowned
        self.title = title
        self.color = color
        self.price = price
        self.status = False
        
    def __repr__(self):
        s = self.title + ': ' + str(self.color) + ' property. Costs ' + str(self.price) + ' dollars'
        return s

class Player:
    def __init__(self, name, location, money):
        self.name = name
        self.location = location
        self.money = money
        
    def __repr__(self):
        s = self.name + ' is at ' + getLocation(self.location) + ' and has ' + str(self.money) + ' dollars.'
        if (self.name == 'you'):
            s = self.name + ' are at ' + getLocation(self.location) + ' and have ' + str(self.money) + ' dollars.'
        return s

        
    
def locationStats(Player):
    
    print(Player.name + ' is currently at ' + getLocation(Player.location))
    print(Player.name + ' has a 17% chance of landing on ' + getLocation(Player.location + 6))
    print(Player.name + ' has a 14% chance of landing on ' + getLocation(Player.location + 5))
    print(Player.name + ' has a 14% chance of landing on ' + getLocation(Player.location + 7))
    print(Player.name + ' has an 11% chance of landing on ' + getLocation(Player.location + 8))
    
    
def main():
    name = input('Input player name: ')
    money = input('How much money does ' + name + ' have? ')
    location = 0
    player = Player(name, location, money)
    print()
    while(True):
        print(player)
        print()
        print('Enter 1 to see what spot you will most likely land on')
        print('Enter 2 to display the Probability Mass Function of each dice roll')
        print('Enter 3 when you are ready to roll')
        print('Enter 4 to simulate a dice roll')
        print('Enter q to quit')
        print()
        decision = input('What would you like to do? ')
        print()
        if decision == '1':
            print()
            locationStats(player)
            print()
        elif decision == '2':
            seeDiceProbability()
        elif decision == '3':
            result = input('What was the result? ')
            player.location += int(result) - 1

                
        elif decision == '4':
            roll = random.randint(1,6) + random.randint(1,6)
            if roll == 11 or roll == 8:
                print('You rolled an ' + str(roll))
            else:
                print('You rolled a '+ str(roll))
            print()
        elif decision == 'q':
            print('Quitting!')
            break
        else:
            print('Decision not recognized')
        
        
            
            
        
        
        
        
        
        
        
        
        
        
    
        