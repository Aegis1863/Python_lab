import pandas as pd
# 设置数据
y = pd.DataFrame([28,34,44,48,58])
x = pd.DataFrame([30,40,50,60,70])
# 求系数
beta2 = float((len(y)*(x*y).sum(0) - y.sum(0)*x.sum(0))/(len(x)*(x**2).sum(0) - (x.sum(0)**2)))
beta1 = float(y.mean() - beta2*x.mean())
yi = lambda xi : beta1 + beta2*xi # 临时方程
# 求R方
yh = [yi(i) for i in x[0]]
ym = float(y.mean())
R2 = sum([(i - ym)**2 for i in yh])/sum([(i - ym)**2 for i in y[0]])
# 输出
print('-->  一元线性回归  <--')
print('β1 = %.3f'%beta1)
print('β2 = %.3f'%beta2)
print('R^2 = %.3f'%R2)
print('hYi = {:.3f} + {:.3f}*Xi'.format(beta1,beta2))
