import math, sys
from bitarray.util import ba2int, int2ba
from bitarray import bitarray
import time

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
    # print(charCodes)
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


    with open(read_path, 'r', encoding='utf-8') as read_file:
        with open(result_path, 'wb') as result_file:
            lines = read_file.read()
            encoded_file = bitarray()
            encoded_file.encode(codes_with_bits, lines)

            input_bitarray = bitarray()
            input_bitarray.extend(bitarray('000'))
            input_bitarray.extend(header)
            input_bitarray.extend(encoded_file)

            fill_size = input_bitarray.fill()
            for i in range(3):
                input_bitarray.pop(0)
            fill_size_bits = number_to_bitstr(fill_size, 3)
            new_input_bitarray = bitarray(fill_size_bits)
            new_input_bitarray.extend(input_bitarray)
            
            new_input_bitarray.tofile(result_file)

def generate_decompressed_file(read_path, result_path):
    input_bitarray = bitarray()
    with open(read_path, 'rb') as read_file:
       input_bitarray.fromfile(read_file)

    fill_size_string = ""
    for i in range(3):
        fill_size_string += str(int(input_bitarray.pop(0)))
    fill_size = int(fill_size_string, 2)
    for i in range(fill_size):
        input_bitarray.pop()

    unique_chars_string = ""
    for i in range(8):
        unique_chars_string += str(int(input_bitarray.pop(0)))

    unique_chars = ba2int(bitarray(unique_chars_string))
    char_codes_dict = dict()
    for i in range(unique_chars):
        char_string = ""
        for j in range(16):
            char_string += str(int(input_bitarray.pop(0)))
        char_bytes = int(char_string, 2).to_bytes(len(char_string) // 8, byteorder='big')
        char = chr(int.from_bytes(char_bytes, byteorder='big', signed=False))

        codelen_string = ""
        for j in range(6):
            codelen_string += str(int(input_bitarray.pop(0)))
        codelen_bits = bitarray(codelen_string)
        codelen = ba2int(codelen_bits)

        code_string = ""
        for j in range(codelen):
            code_string += str(int(input_bitarray.pop(0)))
        code = bitarray(code_string)

        char_codes_dict[char] = code

    decoded_text = ''.join(input_bitarray.iterdecode(char_codes_dict))

    with open(result_path, 'w', encoding='utf-8') as write_file:
        write_file.write(decoded_text)

def main():
    running = True
    path_question = 'Enter file name with extension: '
    print('==== SHANNON-FANO DATA COMPRESSION PROGRAM ====\n')
    while(running):
        answer = input('Do you want to compress or decompress file? (c/d): ')
        if (answer != 'c') and (answer != 'd'):
            print('Enter correct answer!\n')
        else:
            if answer == 'c':
                print('\n------------------------------------------------------\n')
                file_to_read_path = input(path_question)
                start = time.time()
                file = readFile(file_to_read_path)
                prob = probability(file)
                codes = findCodes(prob)
                filename = file_to_read_path.split('.')
                result_name = filename[0]+'.bin'
                generate_compressed_file(codes, file_to_read_path, result_name)
                stop = time.time()
                print (filename[0] + ' compressed sucessfully!')
                print('Compression duration: ' + str(stop-start) + ' s')
                print(result_name + ' has been created!')
                print('\n------------------------------------------------------\n')

            else:
                print('\n------------------------------------------------------\n')
                file_to_decompress_path = input(path_question)
                start = time.time()
                filename = file_to_decompress_path.split('.')
                result_name = filename[0]+'2.txt'
                generate_decompressed_file(file_to_decompress_path, result_name)
                stop = time.time()
                print (filename[0] + ' decompressed sucessfully!')
                print('Decompression duration: ' + str(stop-start) + ' s')
                print(result_name + ' has been created!')
                print('\n------------------------------------------------------\n')
            
            while True:
                answer = input('Do you want to close the program? (y/n): ')
                if answer == 'y':
                    running = False
                    break
                elif answer == 'n':
                    break
                else:
                    print('Enter correct answer!\n')



if __name__ == "__main__":
    main()