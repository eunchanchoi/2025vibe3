import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 불러오기
df = pd.read_csv("생산자물가지수_기본분류__20250725131239.csv", encoding="euc-kr")

# 데이터 전처리
df = df.melt(id_vars=['계정코드별'], var_name='월', value_name='지수')
df = df.drop_duplicates()

# Streamlit 앱 구성
st.title("📊 생산자물가지수 막대그래프")

# 분류 선택
categories = df['계정코드별'].unique()
selected_categories = st.multiselect("📌 계정코드별 선택", categories, default=[categories[0]])

# 선택된 데이터 필터링
filtered_df = df[df['계정코드별'].isin(selected_categories)]

# Plotly 막대 그래프
fig = px.bar(
    filtered_df,
    x='월',
    y='지수',
    color='계정코드별',
    barmode='group',
    title="생산자물가지수 추이 (막대그래프)",
    text_auto='.2s'
)

st.plotly_chart(fig, use_container_width=True)
