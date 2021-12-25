import math, sys
from bitarray import bitarray

def readFile(filename):
    """
    Args:
        filename (str): File name
    Returns:
        str: Content of the file
    """
    with open(filename, encoding='utf-8') as f:
        lines = f.read()
        return lines

def probability(file):
    """
    Args:
        file (str): File content
    Returns:
        dict: k - file characters, v - probabilities, sorted by values desc
    """
    totalCount = 0
    charCount = dict()
    for c in file:
        totalCount += 1
        if c in charCount:
            charCount[c] += 1
        else:
            charCount[c] = 1
    
    charProbability = dict()
    for char, count in charCount.items():
        charProbability[char] = count/totalCount

    charProbability_sorted  = {k: v for k, v in sorted(charProbability.items(), key=lambda item: item[1], reverse=True)}
    return charProbability_sorted

def findCodes(charProbability):
    """
    Args:
        charProbability (dict): k - file characters, v - probabilities, sorted by values desc
    Returns:
        dict: k - char, v - char codes
    """
    charCodes = {x: bitarray() for x in charProbability}

    buildCodes(charProbability, charCodes)
    return charCodes

def buildCodes(charProbability, charCodes):
    """
    Args:
        charProbability (dict): k - character, v - probabilities, sorted by values desc
        charCodes (dict): k - char, v - char code
    Returns:
        dict: k - char, v - char codes
    """
    leftDict, rightDict = divide(charProbability)
    for key, value in  leftDict.items():
        charCodes[key].append(0)
    for key, value in  rightDict.items():
        charCodes[key].append(1)

    if len(leftDict) > 1 or len(rightDict) > 1:
        if len(leftDict) > 1:
            charCodes = buildCodes(leftDict, charCodes)
        if len(rightDict) > 1:
            charCodes = buildCodes(rightDict, charCodes)
    else:
        return charCodes

def divide(myDict):
    """
    Args:
        myDict (dict): Dict to divide, k - file characters, v - probabilities, sorted by values desc
    Returns:
        leftDict: left part of dict
        rightDict: right part of dict
    """
    leftDict = dict()
    rightDict = dict(myDict)

    totalProbSum = sum(myDict.values())
    previousLeftSum = 0
    previousDiff = None
    leftDictElements = 0

    for key, value in myDict.items():
        leftSum = previousLeftSum + value
        rightSum = totalProbSum - leftSum
        diff = abs(leftSum-rightSum)
        if previousDiff == None or diff <= previousDiff:
            previousDiff = diff
            previousLeftSum = leftSum
            leftDictElements += 1
            leftDict[key] = value
            del rightDict[key]
        else:
            break
    
    return leftDict, rightDict

def encode():
    pass

def decode():
    pass

def main():
    #testDict = {'a' : 0.25, 'b' : 0.20, 'c' : 0.15, 'd' : 0.15, 'e' : 0.10, 'f' : 0.10, 'g' : 0.05}
    #codes = findCodes(testDict)

    file = readFile("abc.txt")
    print(file)

    prob = probability(file)
    print(prob)

    codes = findCodes(prob)
    print(codes)

if __name__ == "__main__":
    main()