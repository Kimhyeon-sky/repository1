import streamlit as st
import pandas as pd

# CSV 로드 (EUC-KR 인코딩)
df = pd.read_csv("202505_202505_주민등록인구및세대현황_월간 (1).csv", encoding='euc-kr')
df.columns = df.columns.str.strip()

# 쉼표 제거, 숫자 변환
cols_to_numeric = [
    '2025년05월_총인구수',
    '2025년05월_세대수',
    '2025년05월_남자 인구수',
    '2025년05월_여자 인구수'
]
for col in cols_to_numeric:
    df[col] = df[col].str.replace(',', '').astype(int)

df['2025년05월_남여 비율'] = df['2025년05월_남여 비율'].astype(float)

# 총 인구수 기준 상위 5개 지역
top5 = df.sort_values(by='2025년05월_총인구수', ascending=False).head(5)

# Streamlit 화면 구성
st.title("2025년 5월 주민등록 인구 현황 (남자, 여자, 성비)")
st.write("### 📊 원본 데이터 (상위 5개 행정구역)")
st.dataframe(top5)

# 1️⃣ 남자 인구수
st.write("### 👦 상위 5개 행정구역 남자 인구수")
st.line_chart(top5.set_index('행정구역')['2025년05월_남자 인구수'])

# 2️⃣ 여자 인구수
st.write("### 👩 상위 5개 행정구역 여자 인구수")
st.line_chart(top5.set_index('행정구역')['2025년05월_여자 인구수'])

# 3️⃣ 남녀 비율
st.write("### ⚖️ 상위 5개 행정구역 남녀 성비 (여자 100명당 남자 수)")
st.line_chart(top5.set_index('행정구역')['2025년05월_남여 비율'])

st.caption("출처: 2025년 5월 주민등록인구 및 세대현황")
