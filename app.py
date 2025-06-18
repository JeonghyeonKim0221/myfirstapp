import streamlit as st
import random
import time

# 페이지 기본 설정
st.set_page_config(
    page_title="구구단 퀴즈 팡팡!",
    page_icon="🎉"
)

def initialize_game():
    """
    게임 상태를 초기화하는 함수입니다.
    세션 상태에 현재 문제 번호, 게임 종료 여부를 설정하고 새 문제를 생성합니다.
    """
    st.session_state.question_number = 1
    st.session_state.game_over = False
    generate_new_question()

def generate_new_question():
    """
    새로운 구구단 문제와 보기 3개를 생성하는 함수입니다.
    2부터 9까지의 난수 두 개를 뽑아 문제를 만들고,
    정답 1개와 오답 2개를 생성하여 보기 리스트를 만듭니다.
    """
    # 2단부터 9단까지의 문제를 생성합니다.
    first_num = random.randint(2, 9)
    second_num = random.randint(2, 9)
    correct_answer = first_num * second_num
    
    # 정답과 겹치지 않는 오답 2개를 생성합니다.
    options = {correct_answer}
    while len(options) < 3:
        wrong_answer = random.randint(2, 81)
        if wrong_answer != correct_answer:
            options.add(wrong_answer)
            
    # 문제, 정답, 보기들을 세션 상태에 저장합니다.
    st.session_state.first_num = first_num
    st.session_state.second_num = second_num
    st.session_state.correct_answer = correct_answer
    # 보기 순서를 무작위로 섞습니다.
    st.session_state.options = random.sample(list(options), 3)

# --- 앱 UI 렌더링 시작 ---

# 세션 상태가 초기화되지 않았다면 게임을 초기화합니다.
if 'question_number' not in st.session_state:
    initialize_game()

# 앱 제목을 표시합니다.
st.title("🚀 구구단 퀴즈 팡팡! 🚀")

# 10문제를 모두 맞혔을 경우 (게임이 종료된 경우)
if st.session_state.game_over:
    st.balloons()
    st.success("🎉 모든 문제를 다 맞혔어요! 정말 대단해요! 🎉")
    st.info("새로운 퀴즈를 풀고 싶으면 아래 버튼을 눌러주세요.")
    
    # '다시 시작하기' 버튼을 누르면 게임을 초기화하고 앱을 새로고침합니다.
    if st.button("다시 시작하기"):
        initialize_game()
        st.rerun()
    
else:
    # 현재 문제 진행 상황을 표시합니다. (예: 문제 1 / 10)
    st.header(f"문제 {st.session_state.question_number} / 10")
    
    # 문제를 화면에 표시합니다.
    first_num = st.session_state.first_num
    second_num = st.session_state.second_num
    st.markdown(f"<h2 style='text-align: center; color: black;'>{first_num} X {second_num} = ?</h2>", unsafe_allow_html=True)
    
    st.write("") # 문제와 보기 사이에 여백을 줍니다.

    # 3개의 열을 만들어 보기 버튼을 나란히 표시합니다.
    cols = st.columns(3)
    for i, option in enumerate(st.session_state.options):
        with cols[i]:
            # 각 보기를 버튼으로 만듭니다.
            if st.button(str(option), key=f"option_{i}", use_container_width=True):
                # 사용자가 선택한 답이 정답일 경우
                if option == st.session_state.correct_answer:
                    # 다음 문제로 넘어갑니다.
                    st.session_state.question_number += 1
                    
                    # 정답 축하 메시지와 팡파레를 보여줍니다.
                    st.success("정답입니다! 🎈")
                    st.balloons()
                    time.sleep(1) # 1초간 팡파레를 보여줍니다.
                    
                    # 모든 문제를 다 풀었는지 확인합니다.
                    if st.session_state.question_number > 10:
                        st.session_state.game_over = True
                    else:
                        # 아직 문제가 남았다면 새 문제를 생성합니다.
                        generate_new_question()
                    
                    # 앱을 새로고침하여 다음 문제나 종료 화면을 보여줍니다.
                    st.rerun()
                        
                # 사용자가 선택한 답이 오답일 경우
                else:
                    st.error("아쉬워요! 다시 생각해볼까요? 🤔")
