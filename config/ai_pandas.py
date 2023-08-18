import pandas as pd

# 創建示範數據
data = {
    '姓名': ['Alice', 'Bob', 'Charlie', 'David', 'Emily'],
    '年齡': [25, 30, 35, 40, 28],
    '城市': ['台北', '紐約', '倫敦', '東京', '洛杉磯'],
    '職業': ['工程師', '教師', '銀行家', '設計師', '作家']
}

# 創建DataFrame
df = pd.DataFrame(data)

# 顯示DataFrame
print("原始數據：")
print(df)
print()

# 選擇某些欄位
selected_columns = df[['姓名', '年齡']]
print("選擇姓名和年齡欄位：")
print(selected_columns)
print()

# 過濾數據
filtered_data = df[df['年齡'] > 30]
print("年齡大於30的數據：")
print(filtered_data)
print()

# 新增欄位
df['婚姻狀況'] = ['已婚', '未婚', '已婚', '未婚', '已婚']
print("新增婚姻狀況欄位後的數據：")
print(df)
print()

# 簡單統計
average_age = df['年齡'].mean()
print("平均年齡：", average_age)

oldest_person = df['年齡'].max()
print("最大年齡：", oldest_person)

youngest_person = df['年齡'].min()
print("最小年齡：", youngest_person)