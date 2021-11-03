import math, sys

def readFile(filename):
    charCount = dict()
    charInf = dict()
    totalCount = 0
    with open(filename, encoding='utf-8') as f:
        while True:
            c = f.read(1)
            if not c:
                break
            totalCount += 1
            if c in charCount:
                charCount[c] += 1
            else:
                charCount[c] = 1

    charCount_sorted = {k: v for k, v in sorted(charCount.items(), key=lambda item: item[1], reverse=True)}
    
    for char, count in charCount_sorted.items():
        pe = count/totalCount
        charInf[char] = math.log2(1/pe)
    
    return charCount_sorted, charInf, totalCount

def entropy(dict, num):
    entropy = 0
    for key, value in dict.items():
        pe = value/num
        ie = math.log2(1/pe)
        entropy += pe * ie
    return entropy, ie

def main():
    for arg in sys.argv:
        charCount, charInf, num = readFile(arg)
        ent, ie = entropy(charCount, num)

        print(arg)
        print("Znak : liczba wystąpień : entropia")
        for key, value in charCount.items():
            print(str(key)+" : "+str(value)+" : "+str(charInf[key]))
        print("\nLiczba znaków: "+str(num))
        print("Entropia: "+str(ent))
        print("Ilość informacji: "+str(ie))
        print()

if __name__ == "__main__":
    main()