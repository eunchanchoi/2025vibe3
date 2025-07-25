import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="소비자물가지수 시각화", layout="wide")

st.title("📊 2025년 지출목적별 소비자물가지수 시각화")
st.markdown("2025년 상반기 지출 목적별 CPI(소비자물가지수)를 시각화합니다.")

# 1. CSV 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (예: 소비자물가지수 데이터)", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding='utf-8')

    # 2. '전국' 데이터만 사용
    df_national = df[df['시도별'] == '전국'].copy()

    # 3. 월별 컬럼 추출
    date_columns = [col for col in df_national.columns if col.startswith("2025.")]
    
    # 4. 지출 항목 선택
    categories = df_national['지출목적별'].tolist()
    selected_categories = st.multiselect("📌 시각화할 지출 항목을 선택하세요", categories, default=categories[:5])

    # 5. Plotly 시각화
    fig = go.Figure()

    for _, row in df_national.iterrows():
        if row['지출목적별'] in selected_categories:
            fig.add_trace(go.Scatter(
                x=date_columns,
                y=row[date_columns],
                mode='lines+markers',
                name=row['지출목적별']
            ))

    fig.update_layout(
        title="2025년 상반기 지출목적별 소비자물가지수 추이",
        xaxis_title="월",
        yaxis_title="소비자물가지수 (2020=100 기준)",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("📁 좌측에서 CSV 파일을 업로드해주세요.")
