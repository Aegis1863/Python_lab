import random
b=['林忠','张艺','罗勖','周凌','徐佳','谭红']
a=range(1,len(b)+1)
c=random.sample(a,len(a))
d=random.sample(b,len(a))
lst={}
for i in range(len(d)):
    lst[c[i]]=d[i]
print(lst)
