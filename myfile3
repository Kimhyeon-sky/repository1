import streamlit as st
import pandas as pd

# CSV 파일 불러오기 (EUC-KR 인코딩)
file_path = '202505_202505_연령별인구현황_월간.csv'
df = pd.read_csv(file_path, encoding='euc-kr')

# '2025년05월_계_'로 시작하는 열명에서 연령 숫자만 추출
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_')]
new_age_columns = [col.replace('2025년05월_계_', '').replace('세', '').strip() for col in age_columns]
df_age = df[['행정구역(동읍면)별(1)', '총인구수']] + df[age_columns]
df_age.columns = ['행정구역', '총인구수'] + new_age_columns

# 총인구수 기준 상위 5개 행정구역 추출
df_age['총인구수'] = df_age['총인구수'].str.replace(',', '').astype(int)
top5_regions = df_age.sort_values(by='총인구수', ascending=False).head(5)

# Streamlit 앱 구성
st.title('2025년 5월 기준 연령별 인구 현황 (상위 5개 행정구역)')
st.write('**원본 데이터 (상위 5개 행정구역)**')
st.dataframe(top5_regions)

# 연령별 인구 데이터 준비
age_columns = new_age_columns
top5_regions_long = top5_regions.set_index('행정구역')[age_columns].T
top5_regions_long.index = top5_regions_long.index.astype(int)

# 선 그래프 그리기
st.write('**연령별 인구 분포 (선 그래프)**')
st.line_chart(top5_regions_long)

st.caption('데이터 출처: 2025년 5월 연령별 인구 현황')
