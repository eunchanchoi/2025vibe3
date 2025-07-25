import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 불러오기
df = pd.read_csv("생산자물가지수_기본분류__20250725131239.csv", encoding="euc-kr")

# 데이터 전처리
df = df.melt(id_vars=['계정코드별'], var_name='월', value_name='지수')
df = df.drop_duplicates()

# 지수를 숫자로 변환 (문자열인 경우를 대비)
df['지수'] = pd.to_numeric(df['지수'], errors='coerce')

# Streamlit 앱 제목
st.title("📊 생산자물가지수 막대그래프")

# 계정코드별 선택 옵션
categories = df['계정코드별'].unique()
selected_categories = st.multiselect("📌 계정코드별 선택", categories, default=[categories[0]])

# 선택한 카테고리만 필터링
filtered_df = df[df['계정코드별'].isin(selected_categories)]

# Plotly 막대 그래프 생성 (text 직접 지정)
fig = px.bar(
    filtered_df,
    x='월',
    y='지수',
    color='계정코드별',
    barmode='group',
    text=filtered_df['지수'].round(2),  # 숫자 그대로 보여주기
    title="생산자물가지수 추이 (막대그래프)"
)

fig.update_traces(textposition='outside')  # 막대 위에 숫자 표시
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)
