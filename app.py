import streamlit as st
import random

st.set_page_config(page_title="구구단 퀴즈", layout="centered")

# 세션 상태 초기화
def init_state():
    if 'current_q' not in st.session_state:
        st.session_state.current_q = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'questions' not in st.session_state:
        st.session_state.questions = generate_questions()
    if 'answered' not in st.session_state:
        st.session_state.answered = False
    if 'feedback' not in st.session_state:
        st.session_state.feedback = ""

def generate_questions(n=10):
    questions = []
    for _ in range(n):
        a = random.randint(2, 9)
        b = random.randint(1, 9)
        correct = a * b
        choices = random.sample([correct] + random.sample(range(2, 82), 5), 3)
        if correct not in choices:
            choices[random.randint(0, 2)] = correct
        random.shuffle(choices)
        questions.append({
            'question': f"{a} × {b} = ?",
            'answer': correct,
            'choices': choices
        })
    return questions

# 앱 실행 초기화
init_state()

st.title("🧮 구구단 퀴즈")

if st.session_state.current_q < 10:
    q = st.session_state.questions[st.session_state.current_q]
    st.header(f"문제 {st.session_state.current_q + 1}")
    st.subheader(q['question'])

    for choice in q['choices']:
        if st.button(str(choice), key=f"{st.session_state.current_q}_{choice}"):
            if not st.session_state.answered:
                if choice == q['answer']:
                    st.session_state.feedback = "🎉 정답입니다! 축하합니다! 🎊"
                    st.session_state.score += 1
                else:
                    st.session_state.feedback = "❌ 틀렸어요! 다시 도전해보세요! 💪"
                st.session_state.answered = True

    if st.session_state.answered:
        st.markdown(f"**{st.session_state.feedback}**")
        if st.button("다음 문제로 ▶"):
            st.session_state.current_q += 1
            st.session_state.answered = False
            st.session_state.feedback = ""

else:
    st.success(f"🎉 퀴즈 완료! 총 {st.session_state.score}/10 문제를 맞혔어요!")
    st.balloons()
    st.markdown("### 👍 수고 많았어요! 계속 도전해요!")
    if st.button("🔄 다시 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_state()
