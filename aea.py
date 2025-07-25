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

# 📘 요약 설명 추가
with st.expander("📘 생산자물가지수(PPI)란?"):
    st.markdown("""
    **생산자물가지수(PPI)**는 국내 생산자가 상품이나 서비스를 도매업자 등에게 판매할 때 받는 **출고가격의 평균적인 변동을 나타내는 지표**입니다.

    이 지수는 일반적으로 **특정 기준연도(예: 2020년)의 가격 수준을 100으로 설정**하고, 그 이후의 가격 변동을 상대적으로 보여줍니다.  
    예를 들어 PPI가 120이라면, 기준연도 대비 생산자 가격이 **약 20% 상승**한 것입니다.

    PPI는 소비자 입장이 아닌 **생산자 입장에서 본 물가지표**로, 인플레이션 예측이나 금리 결정 등 다양한 경제정책에 활용됩니다.

    따라서 생산자물가지수는 단순한 숫자가 아닌, **경제 흐름을 읽는 중요한 신호**입니다.
    """)

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
