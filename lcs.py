string="lcs"
def lcs(st1,st2,i,current,arr):
    if i==len(st1):
        # print(current)
        return arr
    if st1[i]==st2[i]:
        arr.append(current)
        return arr
    arr=lcs(st1,st2,i+1,current+string[i],arr)
    arr=lcs(st1,st2,i+1,current,arr)
    return arr
print(lcs(string,"lcds",0,"",[]))
# print(lcs("lcds",0,"",[]))   