import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="생산자물가지수(PPI) 시각화", layout="wide")

st.title("📈 2025년 생산자물가지수(PPI) 시각화")
st.markdown("2025년 상반기 생산자물가지수를 항목별로 시각화합니다.")

# 1. CSV 업로드
uploaded_file = st.file_uploader("📁 생산자물가지수 CSV 파일을 업로드하세요", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding='utf-8')

    # 2. 월 컬럼만 추출
    months = [col for col in df.columns if col.startswith("2025.")]
    
    # 3. 중복 제거한 계정코드 항목들
    unique_items = df['계정코드별'].unique().tolist()
    selected_items = st.multiselect("✅ 시각화할 항목을 선택하세요", unique_items, default=unique_items[:5])

    # 4. Plotly 시각화
    fig = go.Figure()

    for _, row in df.iterrows():
        if row['계정코드별'] in selected_items:
            fig.add_trace(go.Scatter(
                x=months,
                y=row[months],
                mode='lines+markers',
                name=row['계정코드별']
            ))

    fig.update_layout(
        title="2025년 상반기 생산자물가지수(PPI) 추이",
        xaxis_title="월",
        yaxis_title="지수 (2020=100 기준)",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("⬅ 좌측에서 CSV 파일을 업로드하면 시각화가 표시됩니다.")
