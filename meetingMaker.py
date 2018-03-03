class Account:
    def __init__(self, name, email, bestDays):
        self.name = name
        self.email = email
        self.bestDays = bestDays
        
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

def checkDaysValid(bestDays):
    """returns false if list contains anything besides monday tues..etc."""
    realDays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for day in bestDays:
        if day.lower() not in realDays:
            return False
    return True

def createAccount():
    """Create an instance of an account interactively"""
    name = input('Please enter your name: ')
    email = input('Please enter your email: ')
    while '@' not in email or 'gmail' not in email:
        email = input('email is not valid please try again: ')
    bestDays = input('What are your best days to meet? (use commas to separate) ')
    bestDays = [x.strip() for x in bestDays.split(',')]
    if not checkDaysValid(bestDays):
        while not checkDaysValid(bestDays):
            bestDays = input('Days are not valid please try again: ')
            bestDays = [x.strip() for x in bestDays.split(',')]
    
    print('Account created!')
    return Account(name, email, bestDays)

def findCommonDays(person1, person2):
    ret = []
    for day in person1.bestDays:
        if day in person2.bestDays:
            ret += [day]
    s = ''
    for day in ret:
        s += day + ', '
    s = s[:-2]
    
    #print(person1.name + ' and ' + person2.name + ' both have ' + s + ' free!')
    return ret


    
    
