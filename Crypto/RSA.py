def CPPDiv(a,b):
    return int(a/b)

def CPPMod(a,b):
    quotient = CPPDiv(a,b)
    return a-b*quotient

def ExGCD(a,b,x,y): # Return GCD,x,y
    if b==0: return a, 1, 0
    d, y, x = ExGCD(b, CPPMod(a,b), y ,x)
    y -= CPPDiv(a,b)*x
    return d, x, y

def ExGCD_Cal(a,b):
    return ExGCD(abs(a),abs(b),0,0)[1:]

def QuickPow(a,b,MOD):
    if b==0: return 1
    result = QuickPow(a,b//2,MOD) % MOD
    result *= result
    if b&1==1: result *= a
    result %= MOD
    return result

def solveRSAd(n,phi,e):
    u, v = ExGCD_Cal(e, phi)
    if v>0:
        u += phi
        v = e-v
    return u

def Main():
    p = int(input("Prime p:"))
    q = int(input("Prime q:"))
    phi = (p-1)*(q-1)
    n = p * q
    print("Mod N: %d" % n)
    e = int(input("Public Key e:"))
    d = solveRSAd(n, phi, e)
    print("Private Key d: %s" % d)
    c = int(input("Cipher c:"))
    m = pow(c,d,n)
    print("Plain m: %s" % str(hex(m)))
    

if __name__ == '__main__':
    Main()
	# Have Bug with it
