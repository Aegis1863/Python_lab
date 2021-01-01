import random
b=['bob','john','luo','jane','jack','ana']
a=range(1,len(b)+1)
c=random.sample(a,len(a))
d=random.sample(b,len(a))
lst={}
for i in range(len(d)):
    lst[c[i]]=d[i]
print(lst)
