def getonline(code):
    '''
    从数据接口拿数据

    Parameters
    ----------
    code : 字符串
        股票代码+.sz或者sh

    Returns
    -------
    None.

    '''
    try:
        import tushare as ts
        token='d0a0cd40d9e2e7cb3ac55abdd4c90aa6e5455a5ca6d98122b8b8a206'
        pro = ts.pro_api(token)
        df = pro.query('daily',ts_code=code, start_date='20191201', end_date='20200924')
        df.to_csv('练习数据库.csv')#保存数据库
        print('>>新数据已保存')
    except:
        print('>>取得数据失败')


def mc():
    import pandas as pd
    import numpy as np
    from numpy import random
    import matplotlib.pyplot as plt
    data = pd.read_csv('练习数据库.csv')
    sigma = (data['pct_chg']/100).std() # 波动率
    n = 296 # 历史价格时间长度
    dt = 1/n # 单位时间
    sigs = sigma*np.sqrt(dt) # 漂移项
    mu = (data['pct_chg']/100).mean() # 期望收益率
    drt = mu*dt # 扰动项
    pe = data['close'].iloc[0]
    # 初始化
    pt = [] # 全部模拟的容器
    # 蒙特卡洛模拟
    for i in range(1000): # 控制次数
        pn = pe # 初始化股价
        p = [] # 单次模拟情况
        p.append(pe) # 计入初始股价
        for days in range(1,365): # 控制天数
            pn = pn+pn*(drt+random.normal(drt,sigs)) # 产生新股价
            if pn < 0.1:
               pn = p[-1] # 确保股价大于等于一毛钱
            p.append(pn)
        pt.append(p)
    pt = pd.DataFrame(pt).T
    simulations = pt.iloc[-1]

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.subplot(1,2,1)
    plt.plot(pt)
    plt.title('中科曙光-蒙特卡罗赌狗法-股价模拟')
    plt.xlabel('时间/天')
    plt.ylabel('价格/元')

    plt.subplot(1,2,2)
    q = np.percentile(simulations, 1) # 1%分位数位置
    plt.figtext(0.85, 0.8, "起始价: %.2f" % data['close'].iloc[0])
    plt.figtext(0.85, 0.7, "最终平均价: %.2f" % simulations.mean())
    plt.figtext(0.85, 0.6, "风险价值VaR(0.99): %.2f" % (data['close'].iloc[0] - q))
    plt.figtext(0.85, 0.5, "置信区间q(0.99): %.2f" % q)
    plt.axvline(x=q, linewidth=4, color='r') # 置信区间位置

    plt.title('中科曙光-蒙特卡罗赌狗法-价格分布直方图')
    plt.xlabel('价格区间')
    plt.ylabel('出现频率')
    plt.hist(simulations,bins=200)
    plt.show()

mc()
