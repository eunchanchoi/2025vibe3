import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# CSV 파일 경로
csv_path = "202506_202506_연령별인구현황_월간_남녀구분 (1).csv"

# 데이터 불러오기
df = pd.read_csv(csv_path, encoding='cp949')

# 남녀 연령별 컬럼 추출
male_columns = [col for col in df.columns if '남_' in col and '세' in col]
female_columns = [col for col in df.columns if '여_' in col and '세' in col]
ages = [col.split('_')[-1].replace('세', '') for col in male_columns]

# 서울특별시 데이터만 필터링
seoul = df[df['행정구역'].str.contains('서울특별시')]

# 남녀 인구 추출 및 숫자형으로 변환
male_pop = seoul[male_columns].iloc[0].str.replace(',', '').astype(int).tolist()
female_pop = seoul[female_columns].iloc[0].str.replace(',', '').astype(int).tolist()

# 시각화를 위한 데이터프레임
age_df = pd.DataFrame({
    '연령': list(map(int, ages)),
    '남자': male_pop,
    '여자': female_pop
}).sort_values(by='연령')

# Streamlit 앱 UI
st.title("📊 서울특별시 연령별 인구 분포 (2025년 6월 기준)")
st.markdown("출처: 행정안전부 주민등록인구통계")

# Plotly 막대 그래프
fig = go.Figure()
fig.add_trace(go.Bar(x=age_df['연령'], y=age_df['남자'], name='남자', marker_color='royalblue'))
fig.add_trace(go.Bar(x=age_df['연령'], y=age_df['여자'], name='여자', marker_color='lightcoral'))

fig.update_layout(
    title="연령별 인구 수",
    xaxis_title="연령",
    yaxis_title="인구 수",
    barmode='group'
)

st.plotly_chart(fig, use_container_width=True)
