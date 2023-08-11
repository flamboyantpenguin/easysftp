#DAWN Simple Binary Encryption System
#Version 1.0
#Made by DAWN/ペンギン
#Last Updated: 02-08-2023

def switch(data, key, level):


    def isPrime(num):
        for i in range(2, num):
            if i % num == 0:
                return False
        return True
    

    def binswap(k):
        r = ''
        l = list(k)
        for i in range(0, len(l)-1, 2): l[i+1], l[i] = l[i],l[i+1]
        for i in l: r+=i
        return r
    
    
    def reverse(s):
        r = ''
        l = list(s)
        for i in reversed(l): r+=i
        return r


    sData = ''
    key = reverse(key)
    key = binswap(key)


    match level:
        case 0:
            num = 0
            for i in data:
                if ord(key[num]) % 2 == 0:
                    sData+=str(int(not int(i)))
                else: 
                    sData+=i
                num+=1
                if num == len(key)-1: num = 0
        case 1:
            num = 0
            for i in data:
                if key[num].isalpha():
                    if ord(key[num]) % 2 != 0:
                        sData+=str(int(not int(i)))
                    else: 
                        sData+=i
                elif key[num].isalnum():
                    if ord(key[num]) % 2 == 0:
                        sData+=str(int(not int(i)))
                    else: 
                        sData+=i
                else: 
                    sData+=i
                num+=1
                if num == len(key)-1: num = 0
        case 2: 
            num = 0
            for i in data:
                if ord(key[num]) % 3 == 0:
                    if key[num].isdigit() and int(key[num]) % 2 == 0:
                        sData+=str(int(not int(i)))
                    else: 
                        sData+=i
                elif ord(key[num]) % 2 == 0:
                    if key[num].isdigit() and int(key[num]) % 4 == 0:
                        sData+=str(int(not int(i)))
                    else: 
                        sData+=i
                else: 
                    sData+=str(int(not int(i)))
                num+=1
                if num == len(key)-1: num = 0
    
    return sData