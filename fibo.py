n=13
dp=[-1]*n
# dp[0]=0
def fibo(n,dp): 
    print(dp)
    if n ==0:
        return 0
    if n==1 :
        return 1
    if dp[n]!=-1:
        return dp[n]
    ans=fibo(n-1,dp)+fibo(n-2,dp)
    dp[n]=ans
    return ans
print(fibo(n-1,dp))
