import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 불러오기
df = pd.read_csv("생산자물가지수_기본분류__20250725131239.csv", encoding="euc-kr")

# 데이터 전처리
df = df.melt(id_vars=['계정코드별'], var_name='월', value_name='지수')
df = df.drop_duplicates()

# 지수 숫자형 변환
df['지수'] = pd.to_numeric(df['지수'], errors='coerce')

# '2025.01' -> '01' 형태로 가공
df['월'] = df['월'].str.split('.').str[1]

# Streamlit UI
st.title("📊 생산자물가지수 시각화")

# 계정코드별 선택
categories = df['계정코드별'].unique()
selected_categories = st.multiselect("📌 계정코드별 선택", categories, default=[categories[0]])

# 선택 필터링
filtered_df = df[df['계정코드별'].isin(selected_categories)]

# ─────────────────────────────────────────────
# 📊 1. 막대 그래프
fig_bar = px.bar(
    filtered_df,
    x='월',
    y='지수',
    color='계정코드별',
    barmode='group',
    text=filtered_df['지수'].round(2),
    title="월별 생산자물가지수 (막대그래프)"
)
fig_bar.update_traces(textposition='outside')
fig_bar.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

# 그래프 출력
st.plotly_chart(fig_bar, use_container_width=True)

# ─────────────────────────────────────────────
# 📈 2. 선 그래프
fig_line = px.line(
    filtered_df,
    x='월',
    y='지수',
    color='계정코드별',
    markers=True,
    title="월별 생산자물가지수 (선그래프)"
)
fig_line.update_layout(yaxis_title="지수", xaxis_title="월")

# 그래프 출력
st.plotly_chart(fig_line, use_container_width=True)
