def HPSqrt(a,b): #高精度开整数根，a为开几次根，b为要开根的数
    l=0
    r=1
    while(r**a<=b):
        l=r
        r=r*2  
    while(l+1<r):  
        mid=(l+r)//2
        if (mid**a<=b): l=mid
        else: r=mid
    if (l**a<=b): return l
    else: return r

def HPSolve12(a,b,c): #高精度解整数一元二次方程，解RSA用
    key=HPSqrt(2,b*b-4*a*c)
    return ((-b+key)//2//a,(-b-key)//2//a)

a=1
b=-2
c=1
print(HPSolve12(a,b,c)) #将方程整理成ax^2+bx+c=0的形式代入即可
