import streamlit as st
import random
import time

st.set_page_config(page_title="가위바위보 게임", page_icon="✊", layout="centered")

st.title("🎮 가위바위보 게임!")
st.markdown("#### ✂️🪨📄 당신의 선택은?")

choices = {"가위": "✌️", "바위": "✊", "보": "🖐️"}
user_choice = st.radio("선택하세요:", list(choices.keys()), horizontal=True)
computer_choice = random.choice(list(choices.keys()))

if st.button("대결 시작! ⚔️"):
    with st.spinner("결과를 확인하는 중..."):
        time.sleep(1.2)  # 약간의 긴장감 연출

    st.subheader("✨ 결과 ✨")
    st.write(f"당신: {choices[user_choice]}")
    st.write(f"컴퓨터: {choices[computer_choice]}")

    if user_choice == computer_choice:
        st.markdown("🌫️ **무승부!** 서로 같은 선택을 했어요!")
        st.info("다시 한 번 도전해볼까요?")
    elif (user_choice == "가위" and computer_choice == "보") or \
         (user_choice == "바위" and computer_choice == "가위") or \
         (user_choice == "보" and computer_choice == "바위"):
        st.balloons()
        st.success("🎉 승리! 축하합니다!")
    else:
        st.markdown("⚡ **패배...!** 컴퓨터가 이겼어요!")
        st.error("😢 너무 아쉬워요. 다음엔 꼭 이겨봐요!")


