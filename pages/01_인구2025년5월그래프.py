import streamlit as st
import pandas as pd
import folium
from folium import Map, CircleMarker
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import re
import time

st.title("2025년 5월 기준 연령별 인구 현황 - 지도 시각화")

# 데이터 불러오기
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 괄호 안 숫자 제거 (행정구역)
def clean_region_name(name):
    return re.sub(r"\(.*?\)", "", name).strip()

df['행정구역'] = df['행정구역'].apply(clean_region_name)

# 총인구수 숫자 변환
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

# 상위 5개 지역 추출
top5_df = df.sort_values(by='총인구수', ascending=False).head(5)

# 지오코딩 (위경도 변환)
geolocator = Nominatim(user_agent="population-map")
def geocode_address(addr):
    try:
        location = geolocator.geocode(f"{addr}, 대한민국")
        if location:
            return (location.latitude, location.longitude)
    except:
        return None
    return None

with st.spinner('행정구역 위치 찾는 중... (조금 기다려주세요)'):
    time.sleep(1)
    top5_df['위도경도'] = top5_df['행정구역'].apply(geocode_address)

# 지도 만들기
m = Map(location=[36.5, 127.8], zoom_start=7)

# 원 그리기 (핑크색, 반투명)
for _, row in top5_df.iterrows():
    if row['위도경도'] is not None:
        lat, lon = row['위도경도']
        CircleMarker(
            location=[lat, lon],
            radius=row['총인구수'] / 20000,  # 인구수에 따라 크기 조절
            color='pink',
            fill=True,
            fill_color='pink',
            fill_opacity=0.4,
            tooltip=f"{row['행정구역']} (인구 {row['총인구수']:,}명)"
        ).add_to(m)

# Streamlit에서 folium 보여주기
st.subheader("📍 상위 5개 행정구역 인구 분포 (지도)")
st_data = st_folium(m, width=700, height=500)
