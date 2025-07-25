import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 파일 업로드
st.title("👥 인구 피라미드 시각화 (2025년 6월 기준)")
uploaded_file = st.file_uploader("💾 성별 연령별 인구 데이터 (.xlsx)를 업로드하세요", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df = df[df['행정구역'] == '전국']

    # 남성과 여성 연령별 열 추출
    male_cols = [col for col in df.columns if '남_' in col and col.split('_')[-1].isdigit()]
    female_cols = [col for col in df.columns if '여_' in col and col.split('_')[-1].isdigit()]
    ages = [col.split('_')[-1] for col in male_cols]

    male_pop = df[male_cols].values.flatten()
    female_pop = df[female_cols].values.flatten()

    male_pop = -male_pop  # 왼쪽에 보이도록 음수 처리

    # 피라미드 차트 생성
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=ages,
        x=male_pop,
        name='남성',
        orientation='h',
        marker=dict(color='royalblue')
    ))
    fig.add_trace(go.Bar(
        y=ages,
        x=female_pop,
        name='여성',
        orientation='h',
        marker=dict(color='lightpink')
    ))

    fig.update_layout(
        title='전국 성별 연령별 인구 피라미드 (2025년 6월)',
        barmode='overlay',
        bargap=0.1,
        xaxis=dict(title='인구 수', tickvals=[-2000000, -1000000, 0, 1000000, 2000000],
                   ticktext=['200만', '100만', '0', '100만', '200만']),
        yaxis=dict(title='연령'),
        template='plotly_white',
        height=800
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("엑셀 파일을 업로드해주세요 (.xlsx)")
