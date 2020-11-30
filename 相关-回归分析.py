from sklearn import preprocessing # 利用sklearn的数据处理进行归一化
import pandas as pd
import statsmodels.formula.api as sm  #statsmodels.formula.api.ols 回归模型库

data = pd.DataFrame([])
df = pd.read_excel('上证指数.xlsx')
data['y'] = df['close']
data['x1'] = df['amount']

# 标准化
min_max_scaler = preprocessing.MinMaxScaler()
data2 = min_max_scaler.fit_transform(data)
data2 = pd.DataFrame(data2, columns=['y','x1']) # 必须要设定字段名称

model = sm.ols('y ~ x1', data2) # 这里没有写截距，截距是默认存在的
# model = sm.ols("y ~ -1 + x1 + x2", data) # 这里加上-1，表示不加截距

result = model.fit() # 回归拟合
print(result.summary())