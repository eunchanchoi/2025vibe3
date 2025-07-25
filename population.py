import streamlit as st
import pandas as pd
import plotly.express as px

# 제목
st.title("📊 2025년 6월 시도별 남녀 총인구수 시각화")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 데이터 읽기
    df = pd.read_csv(uploaded_file, encoding='cp949')

    # 시도명만 추출
    df['시도'] = df['행정구역'].str.extract(r'([\uAC00-\uD7A3]+)')

    # 쉼표 제거 후 숫자형으로 변환
    df['2025년06월_남_총인구수'] = df['2025년06월_남_총인구수'].str.replace(',', '').astype(int)
    df['2025년06월_여_총인구수'] = df['2025년06월_여_총인구수'].str.replace(',', '').astype(int)

    # 총인구수 계산 및 정렬
    df['총인구수'] = df['2025년06월_남_총인구수'] + df['2025년06월_여_총인구수']
    df_sorted = df.sort_values(by='총인구수', ascending=False)

    # Plotly 그래프
    fig = px.bar(
        df_sorted,
        x='시도',
        y=['2025년06월_남_총인구수', '2025년06월_여_총인구수'],
        labels={'value': '인구수', 'variable': '성별'},
        title='2025년 6월 시도별 남녀 총인구수',
        barmode='group',
        color_discrete_map={
            '2025년06월_남_총인구수': 'blue',
            '2025년06월_여_총인구수': 'pink'
        }
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("왼쪽 사이드바 또는 위에서 CSV 파일을 업로드하세요.")
