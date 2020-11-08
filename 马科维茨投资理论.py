import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as scs
import scipy.optimize as sco

df = pd.read_excel('多标的价格或净值数据.xlsx') # 参数设定为目标表格路径

log_returns = np.log(df.pct_change()+1)
log_returns = log_returns.dropna()
total_returns = log_returns.mean()*len(df.index) # 每支基金总收益
stocks = df.columns

def normality_test(array):
    print('Norm test p-value %14.3f' % scs.normaltest(array)[1])

print('>> P值检验')
for stock in stocks:
    print('\nResults for {}'.format(stock))
    print('-'*32)
    log_data = np.array(log_returns[stock])
    normality_test(log_data)

weights = np.random.random(len(stocks))
weights /= np.sum(weights) # 投资组合权重
anticipate_returns = np.dot(weights, log_returns.mean())*len(df.index) # 总预期收益率
variance_of_troups = np.sqrt(weights, np.dot(log_returns.cov()*len(df.index), weights)) # 投资组合方差

port_returns = []
port_variance = []
for p in range(2000): # 2000组随机模拟数据
    weights = np.random.random(len(stocks))
    weights /= np.sum(weights)
    port_returns.append(np.sum(log_returns.mean()*len(df.index)*weights))
    port_variance.append(np.sqrt(np.dot(weights.T, np.dot(log_returns.cov()*len(df.index), weights))))

port_returns = np.array(port_returns)
port_variance = np.array(port_variance)

def stats(weights):
    weights = np.array(weights)
    port_returns = np.sum(log_returns.mean()*weights)*len(df.index)
    port_variance = np.sqrt(np.dot(weights.T, np.dot(log_returns.cov()*len(df.index),weights)))
    return np.array([port_returns, port_variance, port_returns/port_variance])

# 最小化夏普指数的负值
def min_sharpe(weights):
    return -stats(weights)[2]

# 给定初始权重
x0 = len(stocks)*[1./len(stocks)]

# 权重（某股票持仓比例）限制在0和1之间。
bnds = tuple((0,1) for x in range(len(stocks)))

# 权重（股票持仓比例）的总和为1。
cons = ({'type':'eq', 'fun':lambda x: np.sum(x)-1})

# 优化函数调用中忽略的唯一输入是起始参数列表(对权重的初始猜测)。我们简单的使用平均分布。
opts = sco.minimize(min_sharpe,
                    x0,
                    method = 'SLSQP',
                    bounds = bnds,
                    constraints = cons)

def min_variance(weights):
    return stats(weights)[1]

optv = sco.minimize(min_variance,
                    x0,
                    method = 'SLSQP',
                    bounds = bnds,
                    constraints = cons)

def min_variance(weights):
    return stats(weights)[1]

#在不同目标收益率水平（target_returns）循环时，最小化的一个约束条件会变化。
target_returns = np.linspace(0.0,0.5,50)
target_variance = []
for tar in target_returns:
    #给定限制条件：给定收益率、投资组合权重之和为1
    cons = ({'type':'eq','fun':lambda x:stats(x)[0]-tar},{'type':'eq','fun':lambda x:np.sum(x)-1})
    res = sco.minimize(min_variance, x0, method = 'SLSQP', bounds = bnds, constraints = cons)
    target_variance.append(res['fun'])

target_variance = np.array(target_variance)

plt.figure(figsize = (8,4))
#圆点：随机生成的投资组合散布的点
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.scatter(port_variance, port_returns, c = port_returns/port_variance,marker = 'o')
#叉号：投资组合有效边界
plt.scatter(target_variance,target_returns, c = target_returns/target_variance, marker = 'x')
#红星：标记夏普率最大的组合点
plt.plot(stats(opts['x'])[1], stats(opts['x'])[0], 'r*', markersize = 15.0)
#黄星：标记方差最小投资组合点
plt.plot(stats(optv['x'])[1], stats(optv['x'])[0], 'y*', markersize = 15.0)
plt.grid(True)
plt.xlabel('expected volatility')
plt.ylabel('expected return')
plt.colorbar(label = 'Sharpe ratio')

# 数据输出(根据实际情况需要修改字段名称)
print('>> 夏普比率最优组合')
print('华安策略优选, 国投深证100指数, 广发沪港深新起点股票, 嘉实全球互联网QDII, 上投成长动力')
print('权重：0,     0.409,         0,                 0.135,             0.456')
print('预期回报，预期波动率，夏普比率')
print('0.474,  0.181,    2.615\n\n')
print('>> 方差最小最优组合')
print('华安策略优选, 国投深证100指数, 广发沪港深新起点股票, 嘉实全球互联网QDII, 上投成长动力')
print('权重：0.546, 0,             0,                 0.144,             0.31')
print('预期回报，预期波动率，夏普比率')
print('0.381,  0.166,    2.298')
