import math, sys

def readFile(filename):
    charNums = dict()
    num = 0
    with open(filename, encoding='utf-8') as f:
        while True:
            c = f.read(1)
            if not c:
                break
            num += 1
            if c in charNums:
                charNums[c] += 1
            else:
                charNums[c] = 1

    return charNums, num

def entropy(dict, num):
    entropy = 0
    for key, value in dict.items():
        pe = value/num
        ie = math.log2(1/pe) * 8
        entropy += pe * ie
    return entropy, ie

def main():
    for arg in sys.argv:
        dict, num = readFile(arg)
        ent, ie = entropy(dict, num)

        print(arg)
        for key, value in dict.items():
            print(str(key)+" : "+str(value)+"\t:"+str())
        print("Liczba znaków: "+str(num))
        print("Entropia: "+str(ent))
        print("Ilość informacji: "+str(ie))
        print()

if __name__ == "__main__":
    main()