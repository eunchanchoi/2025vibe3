import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Streamlit 설정
st.set_page_config(page_title="연령별 인구 피라미드", layout="wide")

# 데이터 불러오기
df = pd.read_csv("202506_202506_연령별인구현황_월간_남녀구분 (1).csv", encoding="cp949")

# 전국 데이터만 필터링
df_total = df[df["행정구역"].str.contains("전국")].copy()

# 연령별 남성/여성 컬럼 추출
male_cols = [col for col in df_total.columns if "남_" in col and "세" in col]
female_cols = [col for col in df_total.columns if "여_" in col and "세" in col]

# 연령 라벨 추출 (문자 그대로 유지)
ages_str = [col.split("_")[-1] for col in male_cols]

# 인구 수 가져오기 및 숫자로 변환
male_vals = df_total[male_cols].iloc[0].str.replace(",", "").astype(int).tolist()
female_vals = df_total[female_cols].iloc[0].str.replace(",", "").astype(int).tolist()

# 정렬 기준 정의 (100세 이상은 가장 뒤로)
def age_sort_key(age_label):
    if "이상" in age_label:
        return 200
    else:
        return int(age_label.replace("세", ""))

# 정렬된 인덱스 생성
sorted_indices = sorted(range(len(ages_str)), key=lambda i: age_sort_key(ages_str[i]), reverse=True)

# 정렬된 데이터 만들기
ages_sorted = [ages_str[i] for i in sorted_indices]
male_vals_sorted = [male_vals[i] for i in sorted_indices]
female_vals_sorted = [female_vals[i] for i in sorted_indices]

# 제목 출력
st.title("👶👨‍🦳 2025년 6월 대한민국 연령별 인구 피라미드")
st.markdown("#### 출처: 통계청 / 단위: 명")

# Plotly 그래프
fig = go.Figure()

fig.add_trace(go.Bar(
    y=ages_sorted,
    x=[-val for val in male_vals_sorted],
    name="남성",
    orientation="h",
    marker=dict(color="cornflowerblue")
))

fig.add_trace(go.Bar(
    y=ages_sorted,
    x=female_vals_sorted,
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
    template="plotly_white",
    legend=dict(x=0.85, y=1)
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)
