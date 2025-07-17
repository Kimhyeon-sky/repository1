import streamlit as st
import pandas as pd

# 데이터 로드 (EUC-KR)
df = pd.read_csv("202505_202505_주민등록인구및세대현황_월간.csv", encoding='euc-kr')

# 쉼표 제거, 숫자형 변환
df['2025년05월_총인구수'] = df['2025년05월_총인구수'].str.replace(',', '').astype(int)
df['2025년05월_세대수'] = df['2025년05월_세대수'].str.replace(',', '').astype(int)
df['2025년05월_세대당 인구'] = df['2025년05월_세대당 인구'].astype(float)

# 상위 5개 행정구역 (총인구수 기준)
top5 = df.sort_values(by='2025년05월_총인구수', ascending=False).head(5)

# Streamlit
st.title("2025년 5월 기준 주민등록 세대당 인구수 현황")
st.write("### 📊 원본 데이터 (상위 5개 행정구역)")
st.dataframe(top5)

# 시각화용 데이터 준비
plot_data = top5.set_index('행정구역')['2025년05월_세대당 인구']

# 선 그래프 출력 (Streamlit 기본)
st.write("### 📈 상위 5개 행정구역 세대당 인구수")
st.line_chart(plot_data)

st.caption("출처: 2025년 5월 주민등록인구 및 세대현황")
