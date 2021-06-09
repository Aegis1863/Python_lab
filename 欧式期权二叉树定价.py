import math
import numpy as np

def CRR_european_option_value(S0, K, T, r, sigma, otype, M=4):
    '''
    Parameters
    ==========
    S0 : float
        0时刻市场价格\r
    K : float
        执行价格\r
    T : float
        总时长\r
    r : float
        无风险短期利率，常数\r
    sigma : float
        方差，波动率\r
    otype : string
        看涨 'call'、看跌 'put'\r
    M : int
        时间间隔数\r
    '''
    # 生成二叉树
    dt = T / M  # 时间间隔
    df = math.exp(-r * dt)  # 每期贴现率
    # 计算u，d，p
    u = math.exp(sigma * math.sqrt(dt))  # 上涨倍数
    d = 1 / u  # 下跌倍数
    q = (math.exp(r * dt) - d) / (u - d)  # 上涨概率
    # 初始化幂矩阵
    mu = np.arange(M + 1)
    mu = np.resize(mu, (M + 1, M + 1))  # 变成5*5矩阵
    md = np.transpose(mu) # 转置
    mu = u ** (mu - md)
    md = d ** md
    #得到各节点的股票价格
    S = S0 * mu * md
    # 得到叶子结点的期权价值
    if otype == 'call':  # 看涨期权
        V = np.maximum(S - K, 0)  # 内在价值
        new_V = np.float64(V>0)
    else:  # 看跌期权
        V = np.maximum(K - S, 0)  # 内在价值
        new_V = np.float64(V>0)

    #逐步向前加权平均并折现，得到期初期权价值
    for z in range(0, M):  # 向前迭代
        # 逐列更新期权价值，相当于二叉树中的逐层向前折算
        new_V[0:M - z, M - z - 1] = (q * new_V[0:M - z, M - z] + \
                                     (1 - q) * new_V[1:M - z + 1, M - z]) * df
    return [new_V[0, 0],new_V]
cal = []  # 价值列表
value = CRR_european_option_value(100, 99.9, 1, 0.05, 0.2, 'call', M=15)[0]
print('价值为：%.5f'%value)  # 输出价值均值