
import csv
import random
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import math
from operator import itemgetter
import sys
import matplotlib.pyplot as plt


    #To get a row in pandas: dataset.iloc[rowIndex]
    #dataset.iloc[:,0] # first column of data frame
    
    
def readCsvPanda(filename):
    """Read a CSV in pandas"""
    data = pd.read_csv(filename, header = None)
    return data

    

def readCsvHeader(filename):
    data = pd.read_csv(filename)
    return data


def getMaxList(dataset):
    """Reads a dataset and gives the max values for each column"""
    maxList = []
    for col in dataset:
        maxList.append(max(dataset[col]))
    return maxList

def getMinList(dataset):
    """Reads a dataset and gives the min values for each column"""
    minList = []
    for col in dataset:
        minList.append(min(dataset[col]))
    return minList

def generateRandomK(dataset):
    """Generate a random k center from a dataset with same dimensionality"""
    large = getMaxList(dataset)
    small = getMinList(dataset)
    ret = []
    for num in range(len(large)):
        ret.append(random.uniform(small[num], large[num]))
    return ret

def normalize(dataset):
    """Normalize a dataset"""
    #Normalize data, code used from https://www.kaggle.com/parasjindal96/how-to-normalize-dataframe-pandas
    dataNorm = ((dataset-dataset.min())/(dataset.max()-dataset.min()))
    return dataNorm

def reduceDimensions(dataset, dimensions):
    #Based on code from https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
    """Takes a dataset and reduces the number of dimensions to the second argument"""
    pca = PCA(n_components = dimensions)
    principalComponents = pca.fit_transform(dataset)
    ret = pd.DataFrame(data = principalComponents, columns = ['dimension1', 'dimension2'])
    return ret

def findHospitalsChurn(dataset, centers):
    dataset = cleanChurn('churn.csv').values.tolist()
    hospitalChoices = []
    #Iterate over all rows in dataset
    numCols = len(dataset[0])
    numRows = len(dataset)
    #calculate distances and labels
    for r in range(numRows):
        minDistance = 1000
        #closestK = 0
        for j in range(len(centers)):
            inside = 0
            for c in range(numCols):
                if np.isnan(centers[j][c]):
                    centers[j][c] = random.random()
                inside += (centers[j][c] - dataset[r][c])**2
            calcDistance = math.sqrt(inside)
            if calcDistance < minDistance:
                minDistance = calcDistance
                closestK = j
        hospitalChoices.append([closestK, minDistance])
    groupByCluster = {}
    for i in range(len(centers)):
        groupByCluster[i] = []
    for i in range(len(hospitalChoices)):
        if hospitalChoices[i][0] not in groupByCluster:
            groupByCluster[hospitalChoices[i][0]] = [[hospitalChoices[i], i]]
        else:
            groupByCluster[hospitalChoices[i][0]].append([hospitalChoices[i], i])
    return groupByCluster

def findHospitals(dataset, centers):
    """Takes a dataset and a set of centers and outputs a dictionary matching points to centers"""
    dataset = readCsvPanda(dataset)
    dataset = normalize(dataset)
    hospitalChoices = []
    #Iterate over all rows in dataset
    numCols = len(dataset.iloc[0])
    numRows = len(dataset.iloc[:,0])
    #calculate distances and labels
    for r in range(numRows):
        minDistance = 1000
        for j in range(len(centers)):
            inside = 0
            for c in range(numCols):
                inside += (centers[j][c] - dataset.iloc[r][c])**2
            calcDistance = math.sqrt(inside)
            if calcDistance < minDistance:
                minDistance = calcDistance
                closestK = j
        hospitalChoices.append([closestK, minDistance])
    groupByCluster = {}
    for i in range(len(centers)):
        groupByCluster[i] = []
    for i in range(len(hospitalChoices)):
        if hospitalChoices[i][0] not in groupByCluster:
            groupByCluster[hospitalChoices[i][0]] = [[hospitalChoices[i], i]]
        else:
            groupByCluster[hospitalChoices[i][0]].append([hospitalChoices[i], i])
    return groupByCluster

def findHospitalsWithoutDistance(dataset, centers):
    """Takes a dataset and a set of centers and outputs a dictionary matching points to centers"""
    dataset = readCsvPanda(dataset)
    dataset = normalize(dataset)
    hospitalChoices = []
    #Iterate over all rows in dataset
    numCols = len(dataset.iloc[0])
    numRows = len(dataset.iloc[:,0])
    #calculate distances and labels
    for r in range(numRows):
        minDistance = 1000
        for j in range(len(centers)):
            inside = 0
            for c in range(numCols):
                inside += (centers[j][c] - dataset.iloc[r][c])**2
            calcDistance = math.sqrt(inside)
            if calcDistance < minDistance:
                minDistance = calcDistance
                closestK = j
        hospitalChoices.append([closestK])
    groupByCluster = {}
    for i in range(len(hospitalChoices)):
        if hospitalChoices[i][0] not in groupByCluster:
            groupByCluster[hospitalChoices[i][0]] = [[hospitalChoices[i], i]]
        else:
            groupByCluster[hospitalChoices[i][0]].append([hospitalChoices[i], i])
    return groupByCluster
    
def nextIteration(dataset, groupByCluster, oldSet):
    newKset = []
    for center in groupByCluster:
        lst = []
        for data in groupByCluster[center]:
            #data[1] is the row in the data
            lst.append(data[1])
        #compute new centroid from list of rows
        clusterData = []
        for row in lst:
            clusterData.append(dataset.iloc[row])
        newData = [0] * len(clusterData[0])
        for row in clusterData:
            for i in range(len(row)):
                newData[i] += row[i]
        for i in range(len(newData)):
            newData[i] = newData[i]/len(clusterData)
        newKset.append(newData)
    return newKset

def findHospitalsWithoutDistanceAgain(dataset, centers):
    """Takes a dataset and a set of centers and outputs a dictionary matching points to centers"""
    filename = dataset
    dataset = readCsvPanda(dataset)
    if filename == 'churn.csv':
        dataset = dataset.values.tolist()
        for r in range(len(dataset)):
            for c in range(len(dataset[0])):
                dataset[r][c] = fixData(dataset[r][c])
    else:
        dataset = normalize(dataset)
        dataset = dataset.values.tolist()
    
    hospitalChoices = []
    #Iterate over all rows in dataset
    numCols = len(dataset[0])
    numRows = len(dataset)
    #calculate distances and labels
    for r in range(numRows):
        minDistance = 10000000
        for j in range(len(centers)):
            inside = 0
            for c in range(numCols):
                #getting nan values
                if np.isnan(centers[j][c]):
                    centers[j][c] = random.random()
                inside += (centers[j][c] - dataset[r][c])**2
                #print(centers[j][c])
            calcDistance = math.sqrt(inside)
            #print(calcDistance)
            if calcDistance < minDistance:
                minDistance = calcDistance
                closestK = j
        hospitalChoices.append([closestK])
    groupByCluster = {}
    for i in range(len(hospitalChoices)):
        if hospitalChoices[i][0] not in groupByCluster:
            groupByCluster[hospitalChoices[i][0]] = [[hospitalChoices[i], i]]
        else:
            groupByCluster[hospitalChoices[i][0]].append([hospitalChoices[i], i])
    return groupByCluster

def getNextCenter(dataset, lastCenter):
    """Gets the next center for k-means++"""
    hospitalChoices = []
    centroid = [lastCenter]
    for r in range(len(dataset.iloc[:,0])):
        maxDistance = -1
        for j in range(len(centroid)):
            inside = 0
            for c in range(len(dataset.iloc[0])):
                inside += (centroid[j][c] - dataset.iloc[r][c])**2
            calcDistance = math.sqrt(inside)
            if calcDistance > maxDistance:
                maxDistance = calcDistance
                #farthestK = j
            #new center will return index and distance
        hospitalChoices.append([r, maxDistance])
    farthestPoint = [0, -1]
    for point in hospitalChoices:
        if point[1] > farthestPoint[1]:
            farthestPoint = point
    return dataset.iloc[r].tolist()
        
def output(groupByCluster):
    """Format the output as specified in the project specifications"""
    first = []
    for key in groupByCluster:
        for elem in groupByCluster[key]:
            first.append(elem)
    first = sorted(first, key=itemgetter(1))
    second = []
    for elem in first:
        second.append(elem[0][0])
    return second

def fixData(data):
    if data == 'Male':
        return 10
    elif data == 'Female':
        return 20
    elif data == 'Yes':
        return 1
    elif data == 'No':
        return 0
    elif data == 'Fiber optic':
        return 30
    elif data == 'DSL':
        return 25
    elif data == 'No internet service':
        return 20
    elif data == 'Month-to-month':
        return 10
    elif data == 'One year':
        return 20
    elif data == 'Two year':
        return 30
    elif data == 'Credit card (automatic)':
        return 50
    elif data == 'Electronic check':
        return 30
    elif data == 'Mailed check':
        return 20
    elif data == 'Bank transfer (automatic)':
        return 40
    #check
    elif data == 'SeniorCitizen':
        return 0
    #check
    elif data == 'Partner':
        return 0
    #check
    elif data == 'Dependents':
        return 0
    #check
    elif data == 'tenure':
        return 0
    elif data == 'PhoneService':
        return 0
    elif data == 'No phone service':
        return 20
    elif data == 'OnlineSecurity':
        return 0
    elif data == 'OnlineBackup':
        return 0
    elif data == 'DeviceProtection':
        return 0
    elif data == 'TechSupport':
        return 0
    elif data == 'StreamingTV':
        return 0
    elif data == 'StreamingMovies':
        return 0
    elif data == 'Contract':
        return 0
    elif data == 'customerID':
        return 0
    elif data == 'gender':
        return 0
    elif data == 'MultipleLines':
        return 0
    elif data == 'InternetService':
        return 0
    elif data == 'PaperlessBilling':
        return 0
    elif data == 'PaymentMethod':
        return 0
    elif data == 'MonthlyCharges':
        return 0
    elif data == 'TotalCharges':
        return 0
    
    else:
        if '-' in data:
            return 0
        if data == ' ':
            return 0
        
        return float(data)
    
def cleanChurn(filename):
    dataset = readCsvPanda(filename)
    dataset = dataset.values.tolist()
    numRows = len(dataset)
    numCols = len(dataset[0])
    for r in range(numRows):
        for c in range(numCols):              
            dataset[r][c] = fixData(dataset[r][c])    
    return pd.DataFrame(dataset)

def kmeans(filename, k, init = 'random'):
    """main kmeans algorithm"""
    dataset = readCsvPanda(filename)
    #if filename == 'churn.csv':
    #    dataset = cleanChurn(filename)
    dataset = normalize(dataset)
    #take this out after PCA analysis
    if init == 'random':
        #generate k random centoids
        randomCentoids = []
        dataset = removeNans(dataset.values.tolist())
        dataset = pd.DataFrame(dataset)
        for i in range(k):
            randomCentoids.append(generateRandomK(dataset))
        #return randomCentoids
    elif init == 'k-means++':
        betterCentoids = []
        dataset = removeNans(dataset.values.tolist())
        dataset = pd.DataFrame(dataset)
        betterCentoids.append(generateRandomK(dataset))
        lstForm = removeNans(dataset.values.tolist())
        while(len(betterCentoids) < k):
            distanceList = []
            rowList = []
            totalDistance = 0
            #if filename == 'churn.csv':
            #    distances = findHospitalsChurn(filename, [betterCentoids[-1]])
            #else:
            distances = findHospitals(filename, [betterCentoids[-1]])
            for key in distances:
                for point in distances[key]:
                    totalDistance += point[0][1]
                    distanceList.append(point[0][1])
                    rowList.append(point[1])
            for i in range(len(distanceList)):
                distanceList[i] = distanceList[i]/totalDistance
            decision = np.random.choice(np.arange(0, len(distanceList)), p = distanceList)
            betterCentoids.append(lstForm[rowList[decision]])
        randomCentoids = betterCentoids
    print('first ' + str(k) + ' centroids generated')
    dataset = dataset.values.tolist()
    #hospitalChoices[w][k][n] means wine w (at row w) is assigned to centroid k and has distance n
    hospitalChoices = []
    #Iterate over all rows in dataset
    numCols = len(dataset[0])
    numRows = len(dataset)
    #calculate distances and labels
    for r in range(numRows):
        minDistance = 1000
        for j in range(len(randomCentoids)):
            inside = 0
            for c in range(numCols):
                inside += (randomCentoids[j][c] - dataset[r][c])**2
            calcDistance = math.sqrt(inside)
            if calcDistance < minDistance:
                minDistance = calcDistance
                closestK = j
        hospitalChoices.append([closestK, minDistance])
    groupByCluster = {}
    for i in range(k):
        groupByCluster[i] = []
    for i in range(len(hospitalChoices)):
        if hospitalChoices[i][0] not in groupByCluster:
            groupByCluster[hospitalChoices[i][0]] = [[hospitalChoices[i], i]]
        else:
            groupByCluster[hospitalChoices[i][0]].append([hospitalChoices[i], i])
    oldKset = randomCentoids
    #start loop here, this is where the comparison should take place
    print('Entering convergence loop...')
    while True:
        newKset = []
        rows = []
        for cluster in groupByCluster:
            for data in groupByCluster[cluster]:
                rows.append(data[1])
            #rows is now populated with cluster k's data rows
            kData = []
            for row in rows:
                kData.append(dataset[row])
            newK = [0] * len(dataset[0])
            for r in range(len(kData)):
                for c in range(len(kData[0])):
                    newK[c] += kData[r][c]
            for i in range(len(newK)):
                if len(kData) != 0:
                    newK[i] = newK[i] / len(kData)
            newKset.append(newK)
        roundedNewKset = []
        roundedOldKset = []
        for item in newKset:
            roundedNewKset.append([round(x, 4) for x in item]) 
        for item in oldKset:
            roundedOldKset.append([round(x, 4) for x in item])

        if roundedNewKset == roundedOldKset:
            print('Success! Convergence loop terminated')
            print('Cluster id for each row of data:')
            #uncomment line for optimalK experiment:
            #return findHospitals(filename, newKset)
            return output(findHospitalsWithoutDistanceAgain(filename, newKset))
        else:
            oldKset = []
            for kmeanData in newKset:
                oldKset.append(kmeanData) 
            oldClusterLengths = []
            for cluster in groupByCluster:
                oldClusterLengths.append(len(groupByCluster[cluster]))
            #if filename == 'churn.csv':
            #    groupByCluster = findHospitalsChurn(filename, newKset)
            #else:    
            groupByCluster = findHospitals(filename, newKset)
            newClusterLengths = []
            for cluster in groupByCluster:
                newClusterLengths.append(len(groupByCluster[cluster]))
            if oldClusterLengths == newClusterLengths:
                print('Success! Convergence loop terminated')
                print('Cluster id for each row of data:')
                #uncomment line for optimalK experiment:
                #return findHospitals(filename, newKset)
                return output(findHospitalsWithoutDistanceAgain(filename, newKset))
        
def checkDistribution(result):
    ret = {}
    for cluster in result:
        if cluster not in ret:
            ret[cluster] = 1
        else:
            ret[cluster] += 1
    return ret

def removeNans(lst):
    for r in range(len(lst)):
        for c in range(len(lst[0])):
            if np.isnan(lst[r][c]):
                lst[r][c] = 0
    return lst

def doPCA(dataset):
    clusterList = kmeans('2d.csv', 2)
    dataset = readCsvPanda('2d.csv').values.tolist()
    X = []
    Y = []
    for data in dataset:
        X.append(data[0])
        Y.append(data[1])
    for i in range(len(X)):
        if clusterList[i] == 1:
            plt.scatter(X[i], Y[i], c = 'red')
        else:
            plt.scatter(X[i], Y[i], c = 'blue')
    plt.show()
    
def findOptimalK(lowerBound, upperBound, kmeanspp = False):
    """Uses a modified version of my original k-means algorithm, I'll comment the modifications out and label"""
    errorSums = []
    xAxis = []
    if not kmeanspp:
        for k in range(lowerBound, upperBound + 1):
            xAxis.append(k)
            errorSum = 0
            result = kmeans('wine.csv', k)
            for key in result:
                for elem in result[key]:
                    errorSum += elem[0][1]
            errorSums.append(errorSum)
    else:
        for k in range(lowerBound, upperBound + 1):
            xAxis.append(k)
            errorSum = 0
            result = kmeans('wine.csv', k, 'k-means++')
            for key in result:
                for elem in result[key]:
                    errorSum += elem[0][1]
            errorSums.append(errorSum)
        
    plt.plot(xAxis, errorSums)
    
        
                    
            

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        k = int(sys.argv[2])
        init = sys.argv[3]
        result = kmeans(filename, k, init)
        print(result)
        with open('output.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            for num in result:
                writer.writerow([num])
    