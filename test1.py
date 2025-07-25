import streamlit as st
import random

st.set_page_config(page_title="가위바위보 게임", page_icon="✊", layout="centered")

st.title("🎮 가위바위보 게임!")
st.markdown("#### ✂️🪨📄 당신의 선택은?")

choices = {"가위": "✌️", "바위": "✊", "보": "🖐️"}
user_choice = st.radio("선택하세요:", list(choices.keys()), horizontal=True)
computer_choice = random.choice(list(choices.keys()))

if st.button("대결 시작! ⚔️"):
    st.write(f"당신: {choices[user_choice]}")
    st.write(f"컴퓨터: {choices[computer_choice]}")

    if user_choice == computer_choice:
        st.success("😐 무승부!")
    elif (user_choice == "가위" and computer_choice == "보") or \
         (user_choice == "바위" and computer_choice == "가위") or \
         (user_choice == "보" and computer_choice == "바위"):
        st.balloons()
        st.success("🎉 승리!")
    else:
        st.error("😭 패배... 다시 도전!")


