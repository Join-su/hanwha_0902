import streamlit as st

# 이름을 입력받아 버튼을 누르면 인사말 출력
name = st.text_input("이름을 입력하세요")

if st.button("인사하기"):
    st.write(f"안녕하세요, {name}님!")
