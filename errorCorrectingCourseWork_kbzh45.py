r = 0
v=[]
changes = 0
import random
def message(a):
    global r
    val = len(a)
    prel=[]
    l=[]
    r = 2
    done = False
    while done == False:
        temp = 2**r - 2*r - 1
        if temp>=val:
            k = temp + r
            done = True
        else:
            r += 1
    x = decimalToVector(val,r)
    m=[]
    for i in range(0,len(x)):
        m.append(x[i])
    for i in range(0,len(a)):
        m.append(a[i])
    while len(m) < k:
        m.append(0)
    return (m)



def hammingEncoder(m):
    global r
    G = hammingGeneratorMatrix(r)
    c=[]
    for i in range(0,len(G[0])):
        temp = 0
        for j in range(0,len(G)):
            temp+= m[j]*G[j][i]
        c.append(temp%2)

    return c
    
def BSC(c,p):
    global changes
    v = c
    changes = 0
    for i in range(0,len(v)):
        rand = random.random()        
        if rand < p:
            changes +=1
            if v[i]==0:
                v[i] = 1
            else:
                v[i] = 0
    return v

def hammingBruteForce(v):
    global r
    if len(v) != 2**r -1:
        return "Error: Incorrect Length"
    distance = len(v)+1
    i=0
    
    while distance > 1:
        m = decimalToVector(i,len(v)-r)
        mG = hammingEncoder(m)
        distance = d(v,mG)
        #print("m" + str(i) + " G = " + str(mG))
        #print ("d(v, m" + str(i) + " G) = " + str(distance))
        i+=1
    hatc = mG
    return hatc

def d(v,m):
    d = 0
    for j in range(0, len(v)):
        if v[j] != m[j]:
            d+=1
    return d

def parityMatrixTranspose():
    global r
    H = []
    i=0
    while (2**r-1 > 2**i):
        i+=1
    dim = i
    for j in range(1,2**r):
        H.append(decimalToVector(j,dim))
    Ht = []
    for a in range(0,len(H[0])):
        temp = []
        for b in range(0,len(H)):
            temp.append(H[b][a])
        Ht.append(temp)
    return Ht
        
            
def hammingLocalSearch(v):
    global r
    if len(v) != 2**r -1:
        return "Error: Incorrect Length"
    Ht=parityMatrixTranspose()
    vtemp = []
    for x in range(0,len(v)):
        vtemp.append(0)
    for i in range(0,len(v)+1):
        e=[]
        for j in range(0,len(v)):
            e.append(0)
            vtemp[j] = v[j]
        if i>=1:
            e[i-1]=1
        for k in range (0,len(v)):
            vtemp[k] = (v[k] + e[k])%2
        syndrome = []
        for l in range(0,len(Ht)):
            temp2 = 0
            for m in range(0,len(Ht[0])):
                temp2 += vtemp[m]*Ht[l][m]
            syndrome.append(temp2%2)
        #print("syndrome = " + str(syndrome))
        #print("v + e" + str(i) + " = " + str(vtemp))
        result = 0
        for n in range(0,len(syndrome)):
            if syndrome[n] == 0:
                result+=1
        if result == len(syndrome):
            return vtemp
        
def hammingSyndrome(v):
    global r
    if len(v) != 2**r -1:
        return "Error: Incorrect Length"
    Ht = parityMatrixTranspose()
    vtemp = []
    for x in range(0,len(v)):
        vtemp.append(v[x])
    syndrome = []
    for l in range(0,len(Ht)):
        temp2 = 0
        for m in range(0,len(Ht[0])):
            temp2 += vtemp[m]*Ht[l][m]
        syndrome.append(temp2%2)
    print("syndrome = " + str(syndrome))
    i=0
    for y in range(0,len(syndrome)):
        i+= 2**(y) * syndrome[len(syndrome)-1 - y]
    print("i = " + str(i))
    hatc = v
    if i == 0:
        return hatc
    else:
        hatc[i-1] = (hatc[i-1] +1)%2
        return hatc


def messageFromCodeword(c):
    global r
    if len(c) != 2**r -1:
        return "Error: Incorrect Length"
    m=[]
    for i in range(0,r):
        del c[2**(r-1-i) -1]
    m = c
    return m




def dataFromMessage(m):
    global r
    if len(m) != 2**r -r -1:
        return "Error: Incorrect Length"
    n=0
    for j in range(0,r):
        n+= 2**(j) * m[r-1 - j]
    a=[]
    if r+n > len(m):
        return "Error: impossible to recover raw data"
    for i in range(r,r+n):
        a.append(m[i])
    return a




def simulation(a,p):
    global changes
    print ("Raw Data")
    print ("a = " + str(a))
    print ()
    print ("Message")
    m = message(a)
    print("m = " +str(m))
    print ()
    print ("Codeword")
    c = hammingEncoder(m)
    print("c = " +str(c))
    print ()
    print ("Recieved Vector")
    v = BSC(c,p)
    print ("v = " +str(v))
    print()
    print("Decoding by brute force")
    hatc = hammingBruteForce(v)
    print("hatc = " +str(hatc))
    print()
    print("Decoding by local search")
    hatc = hammingLocalSearch(v)
    print("hatc = " +str(hatc))
    print()
    print("Decoding by syndrome")
    hatc = hammingSyndrome(v)
    print("hatc = " + str(hatc))
    print()
    print("Codeword")
    if hatc != "Error: Incorrect Length":
        print("hatc = " + str(hatc))
        print()
        print("Message")
        hatm = messageFromCodeword(hatc)
        print("hatm = " + str(hatm))
        print()
        if hatm !="Error: Incorrect Length":
            print("Raw data")
            hata = dataFromMessage(hatm)
            print("hata = " + str(hata))
            print()
            if changes <= 1:
                print("Success!")
            else:
                print("Failure!")
        else:
            print("An Error Occured")
    else:
        print("An Error Occured")
        print("Use an alternative raw data vector")













def hammingGeneratorMatrix(r):
    n = 2**r-1
    
    #construct permutation pi
    pi = []
    for i in range(r):
        pi.append(2**(r-i-1))
    for j in range(1,r):
        for k in range(2**j+1,2**(j+1)):
            pi.append(k)

    #construct rho = pi^(-1)
    rho = []
    for i in range(n):
        rho.append(pi.index(i+1))

    #construct H'
    H = []
    for i in range(r,n):
        H.append(decimalToVector(pi[i],r))

    #construct G'
    GG = [list(i) for i in zip(*H)]
    for i in range(n-r):
        GG.append(decimalToVector(2**(n-r-i-1),n-r))

    #apply rho to get Gtranpose
    G = []
    for i in range(n):
        G.append(GG[rho[i]])

    #transpose    
    G = [list(i) for i in zip(*G)]

    return G


def decimalToVector(n,r): 
    v = []
    for s in range(r):
        v.insert(0,n%2)
        n //= 2
    return v
