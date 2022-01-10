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
    charCodes = {x: "" for x in charProbability}

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
    print(charCodes)
    leftDict, rightDict = divide(charProbability)
    for key, value in  leftDict.items():
        charCodes[key] += str(0)
    for key, value in  rightDict.items():
        charCodes[key] += str(1)

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

def get_encoded_keys(codes : dict):
    result = list()
    for key in codes.keys():
        result.append(key.encode())
    return result

def number_to_bitstr(value: int, str_len: int):
    binstr: str = "{0:08b}".format(value)[-str_len:]
    if len(binstr) < str_len:
        binstr = '0'*(str_len-len(binstr)) + binstr
    return binstr

def get_header(codes : dict):
    encoded_keys = get_encoded_keys(codes)
    unique_chars_bitstr = number_to_bitstr(len(codes), 8)
    result = unique_chars_bitstr
    for code in codes.items():
        code_bitstr = number_to_bitstr(ord(code[0]), 8*2)
        code_length = number_to_bitstr(len(code[1]), 6)
        result += code_bitstr + code_length + code[1]
    return result

def get_bitarray_dict(codes : dict):
    result = {}
    for code in codes.items():
        result[code[0]] = bitarray(code[1])
    return result

def generate_compressed_file(codes : dict, read_path, result_path):
    header = bitarray(get_header(codes))
    codes_with_bits = get_bitarray_dict(codes)
    with open(read_path, 'r') as read_file:
        with open(result_path, 'ab') as result_file:
            lines = read_file.readlines()
            header.tofile(result_file)
            for line in lines:
                encoded_line = bitarray()
                encoded_line.encode(codes_with_bits, line)
                encoded_line.tofile(result_file)

def decode():
    pass

def main():
    #testDict = {'a' : 0.25, 'b' : 0.20, 'c' : 0.15, 'd' : 0.15, 'e' : 0.10, 'f' : 0.10, 'g' : 0.05}
    #codes = findCodes(testDict)

    file = readFile("lalka.txt")
    print(file)

    prob = probability(file)
    print(prob)

    codes = findCodes(prob)
    print(codes)

    generate_compressed_file(codes, 'lalka.txt', 'result.bin')

if __name__ == "__main__":
    main()