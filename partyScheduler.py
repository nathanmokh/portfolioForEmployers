brothersList = []
currentSchedule = []
import random
import operator
import tkinter as tk
import csv
from tkinter import filedialog

class Brother(object):
    name = ''
    pc = 0

    def __init__(self, name, pc):
        self.name = name
        self.pc = pc

    def __repr__(self):
        return self.name

def pcParser(pc):
    if pc.lower() == 'alpha':
        pc = 1
    elif pc.lower() == 'beta':
        pc = 2
    elif pc.lower() == 'gamma':
        pc = 3
    elif pc.lower() == 'delta':
        pc = 4
    elif pc.lower() == 'epsilon':
        pc = 5
    elif pc.lower() == 'zeta':
        pc = 6
    elif pc.lower() == 'eta':
        pc = 7
    elif pc.lower() == 'theta':
        pc = 8
    elif pc.lower() == 'iota':
        pc = 9
    elif pc.lower() == 'kappa':
        pc = 10
    else:
        pc = 10
    return pc

def getBrother():
    """Input brother object into global brothersList"""
    name = input('Brother Last name: ')
    pc = input('Brother pledge class: ')
    pc = pcParser(pc)
    global brothersList
    brothersList += [Brother(name, pc)]
    return  brothersList

def getBrotherCSV(name, pc):
    """Use for CSV Data imports"""
    global brothersList
    pc = pcParser(pc)
    brothersList += [Brother(name, pc)]
    
    
                          
def genGrid(m, n):
    """Creates mxn grid, m being row and n being cols"""
    array = [[0 for i in range(n)] for j in range(m)]
    return array

def formatSchedule(schedule):
    """Make schedule into grid format for user readibility"""
    ret = ''
    for x in schedule:
        ret += str(x) + '\n'
    return ret

def getShifts(brothersList):
    """Pass in available brothers in list and time slots"""
    timeSlots = int(input('Enter amount of timeslots: '))
    positions = int(input('Enter number of positions: '))
    newList = brothersList
    newList = sorted(newList, key = operator.attrgetter('pc'))
    schedule = genGrid(timeSlots, positions)
    currentRow = 0
    breakOut = True
    while len(newList) != 0 and breakOut:
        job = random.randint(0,positions - 1)
        if schedule[currentRow][job] == 0:
            schedule[currentRow][job] = newList.pop(0)
        elif 0 not in schedule[currentRow]:
            currentRow += 1
        elif len(newList) == 0:
            break
        counter = 0
        for x in schedule:
            if 0 not in x:
                counter += 1
            if counter == len(schedule):
                breakOut = False
                break
        
    return schedule

def main():
    print('Welcome to LloydLogistics\n')
    while(True):
        print('1: Enter an available brother to the list')
        print('2: View the list')
        print('3: Generate a schedule from the current list')
        print('4: Remove a brother from the list')
        print('5: Randomly select a brother from the entire list')
        print('6: Randomly select a brother from a certain pledge class')
        print('7: Get count of brothers in list')
        print('8: Load brothers from CSV')
        print('9: View current saved schedule')
        print('10: Write current schedule to CSV')
        print('1913: Quit the program\n')
        decision = input('Enter a command: ')

        if decision == '1':
            getBrother()
            print('Brother added to list\n')
            
        elif decision == '2':
            print('Current List:')
            print(brothersList)
            
        elif decision == '3':
            global currentSchedule
            gen = getShifts(brothersList)
            print(formatSchedule(gen))
            save = input('Would you like to save this schedule? (y/n): ')
            if save.lower() == 'y' or save.lower() == 'yes':
                for i in gen:
                    currentSchedule += [i]
                print('schedule saved.')
            else:
                print('Schedule not saved.')
                    
            
        elif decision == '4' and len(brothersList) > 0:
            print(brothersList)
            toRemove = input('Enter last name of brother to remove (case sensitive of initial input): ')
            nameList = []
            for brother in brothersList:
                nameList += [brother.name]
            if toRemove not in nameList:
                print('Brother is not in list')
                continue
            for i in range(len(nameList)):
                if nameList[i] == toRemove:
                    break
            del brothersList[i]
            print(nameList[i] + ' removed from list.')
                
        elif decision == '5' and len(brothersList) > 0:
            toDecide = random.randint(0,len(brothersList) - 1)

            print('Generated brother:\n' + brothersList[toDecide].name)
        elif decision == '6' and len(brothersList) > 0:
            choice = input('Enter pledge class: ')
            choice = pcParser(choice)
            if str(choice) not in '0123456789':
                print('No brother in list with given pledge class')
                continue
            choiceList = []
            for brother in brothersList:
                if brother.pc == choice:
                    choiceList += [brother]
            decide = random.randint(0,len(choiceList) - 1)
            print('Generated brother:\n' + choiceList[decide].name)
        elif decision == '7':
            print('Amount of brothers in list: ' + str(len(brothersList)))
        elif decision == '8':
            root = tk.Tk()
            root.withdraw()
            filePath = filedialog.askopenfilename()
            if filePath[-4:] != '.csv':
                print('Not a CSV file, load cancelled')
                print('You tried to load: ' + filePath)
                continue
            with open(filePath) as csvDataFile:
                csvReader = csv.reader(csvDataFile)
                for row in csvReader:
                    getBrotherCSV(row[0], row[1])
            print('Loaded list of brothers: ' + str(brothersList))
            print('\n')
        elif decision == '9':
            print('Current schedule:')
            print(formatSchedule(currentSchedule))
        elif decision == '10':
            csvfile = input('What would you like to name the file? ')
            with open(csvfile, 'w') as output:
                writer = csv.writer(output)
                writer.writerows(currentSchedule)
        elif decision == '1913' or decision.lower() == 'quit' or decision.lower() == 'q':
            print('WHAT YEAR???')
            break
        else:
            print('Not a command or you need to add to the list, please try again')
        
