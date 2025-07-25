import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# 데이터 불러오기
df = pd.read_csv("202506_202506_연령별인구현황_월간_남녀구분 (1).csv", encoding="cp949")

# 전국 기준 데이터만 필터링
df_total = df[df["행정구역"].str.contains("전국")].copy()

# 연령별 컬럼 추출
male_cols = [col for col in df_total.columns if "남_" in col and "세" in col]
female_cols = [col for col in df_total.columns if "여_" in col and "세" in col]

# 연령 추출 (문자열에서 '0세', '1세', ... -> 숫자 추출)
ages = [col.split("_")[-1] for col in male_cols]
ages = [int(age.replace("세", "").replace("이상", "100")) for age in ages]

# 값 숫자로 변환
male_vals = df_total[male_cols].iloc[0].str.replace(",", "").astype(int).tolist()
female_vals = df_total[female_cols].iloc[0].str.replace(",", "").astype(int).tolist()

# Streamlit 앱 구성
st.title("👶👨‍🦳 2025년 6월 대한민국 연령별 인구 피라미드")
st.markdown("#### 출처: 통계청 / 단위: 명")

# Plotly 피라미드 차트
fig = go.Figure()

fig.add_trace(go.Bar(
    y=ages,
    x=[-val for val in male_vals],
    name="남성",
    orientation="h",
    marker=dict(color="cornflowerblue")
))

fig.add_trace(go.Bar(
    y=ages,
    x=female_vals,
    name="여성",
    orientation="h",
    marker=dict(color="lightcoral")
))

fig.update_layout(
    barmode='relative',
    xaxis=dict(
        title="인구 수",
        tickvals=[-1000000, -500000, 0, 500000, 1000000],
        ticktext=["100만", "50만", "0", "50만", "100만"]
    ),
    yaxis=dict(title="연령", autorange="reversed"),
    height=800,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)
