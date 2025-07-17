import pandas as pd

df = pd.read_csv('./202505_202505_연령별인구현황_월간.csv', encoding='euc-kr')
df.columns = df.columns.str.strip()  # 혹시 모를 공백 제거

print(df.columns.tolist())

