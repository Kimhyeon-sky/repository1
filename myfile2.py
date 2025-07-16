import streamlit as st
import pandas as pd

# CSV 파일 경로 (수동으로 지정, 사용자 업로드 없이 실행)
FILE_PATH = './202505_202505_연령별인구현황_월간.csv'

# 데이터 불러오기
df = pd.read_csv(FILE_PATH, encoding='euc-kr')

# 컬럼 중 '2025년05월_계_' 로 시작하는 것만 필터링
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_')]

# 컬럼 이름을 연령 숫자만 남기도록 변경
new_age_columns = [col.replace('2025년05월_계_', '').replace('세', '').strip() for col in age_columns]

# 필요한 열만 사용 ('행정구역', '총인구수', 나이별 인구수)
df_filtered = df[['행정구역(동읍면)별(1)', '총인구수'] + age_columns]
df_filtered.columns = ['행정구역', '총인구수'] + new_age_columns

# 총인구수 쉼표 제거 및 숫자형 변환
df_filtered['총인구수'] = df_filtered['총인구수'].str.replace(',', '', regex=False).astype(int)

# 총인구수 기준 상위 5개 지역 추출
top5 = df_filtered.sort_values(by='총인구수', ascending=False).head(5)

# Streamlit UI
st.title('2025년 5월 기준 연령별 인구 현황 (상위 5개 행정구역)')
st.write('### 원본 데이터 (상위 5개 행정구역)')
st.dataframe(top5)

# 연령별 인구 데이터 준비 (행정구역을 열, 연령을 인덱스)
age_data = top5.set_index('행정구역')[new_age_columns].T
age_data.index = age_data.index.astype(int)

st.write('### 연령별 인구 분포 (선 그래프)')
st.line_chart(age_data)

st.caption('데이터 출처: 2025년 5월 연령별 인구 현황')
